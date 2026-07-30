package main

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"sync"
	"time"

	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/temporal"
)

// ProviderError is an error raised by the provider's HTTP client, carrying the
// status and message the library would surface. A real SDK (openai, anthropic,
// net/http) returns something equivalent; the Activity reads Status and message
// off it rather than reconstructing them.
type ProviderError struct {
	Status  int
	Message string
}

func (e *ProviderError) Error() string { return e.Message }

// LLMRegistry is worker-local state injected into the activities: it records the
// provider Generate settled on per Workflow so RunTool can read it without
// threading it through Workflow arguments. Keyed by Workflow ID so concurrent
// executions do not collide, and safe only because every Activity of one execution
// runs on the same worker (use a worker-specific Task Queue to guarantee that). It
// is process-local and NOT durable — which is why the retry BUDGET travels through
// heartbeat details instead; this registry only shares a convenience hint. The
// mutex guards the map because the worker runs activities on concurrent goroutines.
type LLMRegistry struct {
	mu         sync.Mutex
	byWorkflow map[string]string
}

func NewLLMRegistry() *LLMRegistry {
	return &LLMRegistry{byWorkflow: map[string]string{}}
}

func (r *LLMRegistry) Set(workflowID, provider string) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.byWorkflow[workflowID] = provider
}

func (r *LLMRegistry) Get(workflowID string) string {
	r.mu.Lock()
	defer r.mu.Unlock()
	return r.byWorkflow[workflowID]
}

// Activities binds the activity methods to an injected LLMRegistry (dependency
// injection): worker.go constructs one registry and one Activities value, so
// Generate and RunTool share it through the receiver instead of a package global.
type Activities struct {
	registry *LLMRegistry
}

// mockStatuses gives each provider a scripted sequence of outcomes, indexed by
// how many times that provider has been called across the whole run. 0 =
// success; an HTTP status (429, 500, …) returns that error; Timeout makes the
// call hang past the Activity's start-to-close timeout so Temporal times the
// attempt out. Run with an empty prompt to see the 400 (invalid request) abort
// path. The scripted outcomes drive a three-turn agent loop:
//
//	turn 1: anthropic is rate limited (429) until its budget is spent, then fails
//	        over to openai, which answers for the first time.
//	turn 2: openai returns a server error (500) that spends its budget in one
//	        shot, then fails over to gemini, which answers.
//	turn 3: gemini's calls hang and time out; after two timeouts spend its
//	        budget it fails over to anthropic, which has recovered and answers.
var mockStatuses = map[string][]int{
	"anthropic": {429, 429, 429},       // three rate-limit responses in turn 1, then recovers
	"openai":    {0, 500},              // succeeds in turn 1, then a server error in turn 2
	"gemini":    {0, Timeout, Timeout}, // answers in turn 2, then two hangs in turn 3
}

// backoff is the per-status delay before Temporal retries the Activity (applied
// via NextRetryDelay).
var backoff = map[int]time.Duration{
	429: 2 * time.Second,
	500: 1 * time.Second,
	408: 1 * time.Second,
	503: 2 * time.Second,
}

// simulatedLatency is the per-call latency so each provider round-trip takes
// time, the way a real model call would. Keep it well under the start-to-close
// timeout.
const simulatedLatency = 2500 * time.Millisecond

// hungCall is how long a hung call sleeps — past the Generate Activity's
// start-to-close timeout — so Temporal kills the attempt with a timeout instead
// of ever returning. Real model calls stall the same way when a provider is
// degraded.
const hungCall = 20 * time.Second

// providerCallCount is a per-provider call counter kept in worker-process memory
// (like the heartbeat sample's static callIndex), so callProvider walks down
// each provider's scripted mockStatuses by itself. NOTE: process-local demo
// state — it does not survive a worker restart and is not safe across
// concurrent Workflow executions.
var providerCallCount = map[string]int{}

// respond simulates the model's reasoning: it inspects the prompt and either
// asks to run a tool or returns a final answer. This is what makes the Workflow
// loop — the model drives an agentic tool-calling cycle. An empty toolCall means
// a final answer.
func respond(prompt string) (text string, toolCall string) {
	if strings.Contains(prompt, "[calculator output]") {
		return "Durable execution keeps workflow state safe across failures — the answer is 42.", ""
	}
	if strings.Contains(prompt, "[search output]") {
		return "Got the figures; running the numbers.", "calculator"
	}
	return "I need to look that up first.", "search"
}

// callProvider stands in for the provider SDK: given the prompt, it waits for
// the simulated round-trip, then returns the model's response on success or a
// ProviderError carrying the HTTP status and message. It walks down the
// provider's scripted mockStatuses, counting calls itself.
func callProvider(ctx context.Context, provider, prompt string) (text string, toolCall string, err error) {
	index := providerCallCount[provider]
	providerCallCount[provider] = index + 1
	statuses := mockStatuses[provider]
	status := 0
	if index < len(statuses) {
		status = statuses[index]
	}

	// A scripted Timeout is a latency failure: the call hangs so long that the
	// Activity's start-to-close timeout fires and Temporal kills the attempt. The
	// Activity never returns a result from here — there is no error to surface,
	// which is why the retry has to detect the timeout from its own context (see
	// Generate).
	if status == Timeout {
		time.Sleep(hungCall)
	}

	time.Sleep(simulatedLatency)
	if status != 0 {
		return "", "", &ProviderError{Status: status, Message: fmt.Sprintf("%s responded HTTP %d", provider, status)}
	}
	text, toolCall = respond(prompt)
	return text, toolCall, nil
}

// pickProvider prefers the caller's default, then sweeps the remaining providers
// in preference order — starting from the default's position and wrapping around
// the list — skipping any that have spent their budget. This can be extended
// with more sophisticated rules.
func pickProvider(spent map[string]int, defaultProvider string, config FallbackConfig) string {
	start := 0
	for i, p := range config.Providers {
		if p == defaultProvider {
			start = i
			break
		}
	}
	n := len(config.Providers)
	order := make([]string, n)
	for i := 0; i < n; i++ {
		order[i] = config.Providers[(start+i)%n]
	}
	for _, provider := range order {
		if spent[provider] < config.Budget {
			return provider
		}
	}
	// Every provider is exhausted; stay on the last one and let Temporal's
	// MaximumAttempts stop the retries.
	return order[n-1]
}

// chargeTimeouts rebuilds the spent budget after `count` start-to-close timeouts.
// A timeout leaves no outcome to persist (the attempt was killed mid-call), so
// instead of storing a running count each attempt replays the timeouts the gap
// implies. Each one charges the Timeout cost against the provider pickProvider
// would have chosen; once a provider's spend reaches the budget the sweep fails
// over to the next one — even though no HTTP error was ever seen.
func chargeTimeouts(spent map[string]int, count int, defaultProvider string, config FallbackConfig) map[string]int {
	cost, ok := config.ErrorCost[Timeout]
	if !ok {
		cost = config.DefaultErrorCost
	}
	for i := 0; i < count; i++ {
		provider := pickProvider(spent, defaultProvider, config)
		spent[provider] += cost
	}
	return spent
}

// Generate calls one provider per invocation: 400 aborts, other errors are
// retryable so Temporal retries and the next attempt may switch providers. A
// hung call is left to breach the start-to-close timeout, which Temporal turns
// into a retry too. Returns the provider that answered so the caller can reuse it.
func (a *Activities) Generate(ctx context.Context, prompt, defaultProvider string, config FallbackConfig) (GenerateResult, error) {
	// A malformed request is an HTTP 400 that no provider will accept — abort.
	if strings.TrimSpace(prompt) == "" {
		return GenerateResult{}, temporal.NewNonRetryableApplicationError("empty prompt (HTTP 400)", "400", nil)
	}

	// Attempt is Temporal's built-in retry counter (1-based); heartbeat details
	// carry the spent budget and the last resolved attempt across retries.
	attempt := int(activity.GetInfo(ctx).Attempt)

	// Error state maintained across retries via heartbeat details.
	errorState := ErrorState{Spent: map[string]int{}}
	if activity.HasHeartbeatDetails(ctx) {
		_ = activity.GetHeartbeatDetails(ctx, &errorState)
		if errorState.Spent == nil {
			errorState.Spent = map[string]int{}
		}
	}

	// Any attempt since the last one that recorded an HTTP outcome was a timeout —
	// a hung call Temporal killed before it could heartbeat or return a result. The
	// activity context carries no "last failure", so infer those timeouts from the
	// attempt gap and replay them onto a working copy of the budget before picking.
	timeouts := attempt - 1 - errorState.LastResolvedAttempt
	if timeouts < 0 {
		timeouts = 0
	}
	spent := make(map[string]int, len(errorState.Spent))
	for k, v := range errorState.Spent {
		spent[k] = v
	}
	spent = chargeTimeouts(spent, timeouts, defaultProvider, config)

	// Decide which provider to call: the default until it has spent its budget (to
	// HTTP errors or timeouts), then the next provider in preference order.
	provider := pickProvider(spent, defaultProvider, config)

	// Publish the current provider so RunTool (same worker) can read it — a
	// convenience hint; the durable budget lives in heartbeat details.
	a.registry.Set(activity.GetInfo(ctx).WorkflowExecution.ID, provider)

	activity.GetLogger(ctx).Info("calling provider",
		"provider", provider, "attempt", attempt, "timeouts", timeouts, "spent", spent)

	text, toolCall, err := callProvider(ctx, provider, prompt)
	if err == nil {
		return GenerateResult{Provider: provider, Text: text, ToolCall: toolCall}, nil
	}

	var provErr *ProviderError
	if pe, ok := err.(*ProviderError); ok {
		provErr = pe
	} else {
		return GenerateResult{}, err
	}
	status := provErr.Status

	// 400 Bad Request is permanent — no provider will accept the request.
	if status == 400 {
		return GenerateResult{}, temporal.NewNonRetryableApplicationError(provErr.Message, "400", nil)
	}

	// Transient (429 / 500 / 503): spend this provider's budget by the error's
	// cost and record this as the last resolved attempt, so later retries count
	// only the timeouts that follow it. pickProvider keeps this provider until its
	// budget runs out, then switches.
	cost, ok := config.ErrorCost[status]
	if !ok {
		cost = config.DefaultErrorCost
	}
	spent[provider] += cost

	// Persist the running tally (including any replayed timeout failovers) so the
	// retried attempt resumes from here.
	activity.RecordHeartbeat(ctx, ErrorState{Spent: spent, LastResolvedAttempt: attempt})

	// Retryable: Temporal retries the Activity after the per-status backoff.
	delay, ok := backoff[status]
	if !ok {
		delay = 1 * time.Second
	}
	return GenerateResult{}, temporal.NewApplicationErrorWithOptions(
		provErr.Message+"; failing over", strconv.Itoa(status),
		temporal.ApplicationErrorOptions{NextRetryDelay: delay},
	)
}

// RunTool executes a tool the model asked for between turns (simulated here). It
// reads the current provider from the injected registry — state Generate wrote on
// this same worker.
func (a *Activities) RunTool(ctx context.Context, tool, question string) (string, error) {
	provider := a.registry.Get(activity.GetInfo(ctx).WorkflowExecution.ID)
	if provider == "" {
		provider = "unknown"
	}
	activity.GetLogger(ctx).Info("running tool", "tool", tool, "provider", provider)
	time.Sleep(500 * time.Millisecond)
	switch tool {
	case "search":
		return fmt.Sprintf(`top hit for "%s"`, question), nil
	case "calculator":
		return "42", nil
	default:
		return "", nil
	}
}
