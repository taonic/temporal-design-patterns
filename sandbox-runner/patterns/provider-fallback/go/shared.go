package main

const (
	// The Workflow and the sweeping Activity both run on this Task Queue.
	TaskQueue        = "provider-fallback-task-queue"
	WorkflowIDPrefix = "completion"

	// Maximum number of full passes over the provider list before giving up.
	MaxSweeps = 3

	// Maximum agent turns (model calls) before giving up on the tool-calling loop.
	MaxTurns = 6

	// Timeout is a sentinel used both as a scripted provider outcome (a hung call)
	// and as the ErrorCost key for a start-to-close timeout, so a timeout spends
	// the budget the same way an HTTP error does. Not a real HTTP status, hence the
	// negative value.
	Timeout = -1
)

// ErrorState is maintained ACROSS Activity retries via heartbeat details, so a
// retried attempt resumes the sweep where the previous one left off instead of
// restarting from the first provider.
type ErrorState struct {
	// Spent is the retry budget already spent per provider, accumulated across
	// retries.
	Spent map[string]int `json:"spent"`
	// LastResolvedAttempt is the attempt number that last recorded an HTTP outcome
	// (success or a spent budget). Any retry beyond this without advancing it was a
	// start-to-close timeout — a hung provider call Temporal killed before it could
	// record a result — so the gap between it and the current attempt counts the
	// timeouts.
	LastResolvedAttempt int `json:"lastResolvedAttempt"`
}

// FallbackConfig is the fallback policy passed into the Generate Activity: which
// providers to sweep in preference order, how much retry budget each one gets
// before failover, and what each outcome costs against that budget — the
// ErrorCost map is keyed by HTTP status and by Timeout, so a timed-out call
// spends budget like any other error.
type FallbackConfig struct {
	Providers        []string    `json:"providers"`
	Budget           int         `json:"budget"`
	ErrorCost        map[int]int `json:"errorCost"`
	DefaultErrorCost int         `json:"defaultErrorCost"`
}

// GenerateResult is what one model call returns: the provider that produced the
// response, the message text, and an optional tool the model wants to run next.
// An empty ToolCall means the model returned a final answer.
type GenerateResult struct {
	Provider string `json:"provider"`
	Text     string `json:"text"`
	ToolCall string `json:"toolCall,omitempty"`
}
