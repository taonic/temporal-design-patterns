package main

import (
	"fmt"
	"time"

	"go.temporal.io/sdk/temporal"
	"go.temporal.io/sdk/workflow"
)

// ProviderFallbackWorkflow runs an agentic tool-calling loop. Each turn calls
// the model (Generate); if the model asks for a tool, the Workflow runs it and
// feeds the output into the next turn, until the model returns a final answer.
// The provider that answered is reused as the preferred provider for the next
// turn, so a healthy provider is not re-swept from the top of the preference
// list every time — only a fresh failure triggers another fallback sweep.
func ProviderFallbackWorkflow(ctx workflow.Context, question string) (string, error) {
	logger := workflow.GetLogger(ctx)

	// Default fallback policy: sweep the providers in preference order, giving
	// each a retry budget of 3 before failover. Each outcome spends against that
	// budget — a 429 (rate limited) is cheap to retry in place; a 500 (server
	// error) burns the whole budget at once; a Timeout costs 2, so a provider fails
	// over on its second timed-out call.
	config := FallbackConfig{
		Providers:        []string{"anthropic", "openai", "gemini"},
		Budget:           3,
		ErrorCost:        map[int]int{429: 1, 500: 3, Timeout: 2},
		DefaultErrorCost: 2,
	}

	preferredProvider := config.Providers[0]
	prompt := question

	// Nil receiver used only to reference the registered activity methods by name;
	// the SDK resolves the name from the method and never calls it on this value.
	var a *Activities

	for turn := 1; turn <= MaxTurns; turn++ {
		// Set the model-call options per turn so the Activity summary (shown in
		// the Temporal UI/CLI) names the provider this turn starts with. Generate
		// sweeps providers internally; MaximumAttempts caps the sweep at MaxSweeps
		// passes. A healthy call returns in a couple of seconds; a hung provider
		// call breaches StartToCloseTimeout and Temporal retries the Activity with a
		// timeout, which drives the timeout failover. HeartbeatTimeout sits above it
		// so the start-to-close timeout — not a missed heartbeat — is what trips a
		// hang.
		ao := workflow.ActivityOptions{
			StartToCloseTimeout: 6 * time.Second,
			HeartbeatTimeout:    20 * time.Second,
			RetryPolicy:         &temporal.RetryPolicy{MaximumAttempts: int32(MaxSweeps * len(config.Providers))},
			Summary:             fmt.Sprintf("generate (%s)", preferredProvider),
		}
		genCtx := workflow.WithActivityOptions(ctx, ao)

		var result GenerateResult
		if err := workflow.ExecuteActivity(genCtx, a.Generate, prompt, preferredProvider, config).Get(genCtx, &result); err != nil {
			return "", err
		}
		preferredProvider = result.Provider // stick with the provider that just worked
		logger.Info("turn answered", "turn", turn, "provider", result.Provider)

		if result.ToolCall == "" {
			return result.Text, nil // final answer — the agent is done
		}

		// The model requested a tool. Run it, then feed the output into the next turn.
		toolCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
			StartToCloseTimeout: 10 * time.Second,
		})
		var output string
		if err := workflow.ExecuteActivity(toolCtx, a.RunTool, result.ToolCall, question).Get(toolCtx, &output); err != nil {
			return "", err
		}
		prompt = fmt.Sprintf("[%s output] %s", result.ToolCall, output)
	}

	return "", temporal.NewNonRetryableApplicationError(
		fmt.Sprintf("agent did not finish within %d turns", MaxTurns), "AgentLoopExhausted", nil)
}
