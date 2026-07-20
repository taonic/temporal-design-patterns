import io.temporal.activity.ActivityOptions;
import io.temporal.common.RetryOptions;
import io.temporal.failure.ApplicationFailure;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

import java.time.Duration;

@WorkflowInterface
public interface CompletionWorkflow {
    @WorkflowMethod
    String providerFallback(String question);

    // providerFallback runs an agentic tool-calling loop. Each turn calls the model
    // (generate); if the model asks for a tool, the Workflow runs it and feeds the
    // output into the next turn, until the model returns a final answer. The provider
    // that answered is reused as the preferred provider for the next turn, so a
    // healthy provider is not re-swept from the top of the preference list every time
    // — only a fresh failure triggers another fallback sweep.
    final class Impl implements CompletionWorkflow {
        // Default fallback policy: sweep the providers in preference order, giving
        // each a retry budget of 3 before failover. Each outcome spends against that
        // budget — a 429 (rate limited) is cheap to retry in place; a 500 (server
        // error) burns the whole budget at once; a TIMEOUT costs 2, so a provider
        // fails over on its second timed-out call.
        private static final Shared.FallbackConfig DEFAULT_CONFIG = new Shared.FallbackConfig(
                java.util.List.of("anthropic", "openai", "gemini"),
                3,
                java.util.Map.of(429, 1, 500, 3, Shared.TIMEOUT, 2),
                2);

        @Override
        public String providerFallback(String question) {
            Shared.FallbackConfig config = DEFAULT_CONFIG;
            String preferredProvider = config.providers().get(0);
            String prompt = question;

            // runTool is a plain Activity for the tools the agent invokes between
            // model calls.
            CompletionActivities toolStub = Workflow.newActivityStub(
                    CompletionActivities.class,
                    ActivityOptions.newBuilder()
                            .setStartToCloseTimeout(Duration.ofSeconds(10))
                            .build());

            for (int turn = 1; turn <= Shared.MAX_TURNS; turn++) {
                // Create the model-call stub per turn so its Activity summary (shown
                // in the Temporal UI/CLI) names the provider this turn starts with.
                // generate sweeps providers internally; maximumAttempts caps the sweep
                // at MAX_SWEEPS passes over the provider list. A healthy call returns in
                // a couple of seconds; a hung provider call breaches the start-to-close
                // timeout and Temporal retries the Activity with a timeout, which drives
                // the timeout failover. The heartbeat timeout sits above it so the
                // start-to-close timeout — not a missed heartbeat — is what trips a hang.
                CompletionActivities generateStub = Workflow.newActivityStub(
                        CompletionActivities.class,
                        ActivityOptions.newBuilder()
                                .setStartToCloseTimeout(Duration.ofSeconds(6))
                                .setHeartbeatTimeout(Duration.ofSeconds(20))
                                .setRetryOptions(RetryOptions.newBuilder()
                                        .setMaximumAttempts(Shared.MAX_SWEEPS * config.providers().size())
                                        .build())
                                .setSummary("generate (" + preferredProvider + ")")
                                .build());

                Shared.GenerateResult result = generateStub.generate(prompt, preferredProvider, config);
                preferredProvider = result.provider(); // stick with the provider that just worked
                Workflow.getLogger(CompletionWorkflow.class)
                        .info("turn {}: answered by {}", turn, result.provider());

                if (result.toolCall() == null || result.toolCall().isEmpty()) {
                    return result.text(); // final answer — the agent is done
                }

                // The model requested a tool. Run it, then feed the output into the
                // next turn.
                String output = toolStub.runTool(result.toolCall(), question);
                prompt = "[" + result.toolCall() + " output] " + output;
            }

            throw ApplicationFailure.newNonRetryableFailure(
                    "agent did not finish within " + Shared.MAX_TURNS + " turns",
                    "AgentLoopExhausted");
        }
    }
}
