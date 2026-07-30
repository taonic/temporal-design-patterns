import io.temporal.activity.Activity;
import io.temporal.activity.ActivityExecutionContext;
import io.temporal.activity.ActivityInterface;
import io.temporal.failure.ApplicationFailure;

import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@ActivityInterface
public interface CompletionActivities {
    // generate calls one provider per invocation: 400 aborts, other errors are
    // retryable so Temporal retries and the next attempt may switch providers.
    // Returns the provider that answered so the caller can reuse it.
    Shared.GenerateResult generate(String prompt, String defaultProvider, Shared.FallbackConfig config);

    // runTool executes a tool the model asked for between turns.
    String runTool(String tool, String question);

    final class Impl implements CompletionActivities {
        // Injected worker-local state (dependency injection): Worker.java constructs one
        // LLMRegistry and passes it to this constructor, so generate and runTool share
        // it through the instance instead of reaching for a static field.
        private final LLMRegistry registry;

        Impl(LLMRegistry registry) {
            this.registry = registry;
        }

        // Per-status backoff before Temporal retries the Activity (applied via nextRetryDelay).
        private static final Map<Integer, Duration> BACKOFF = Map.of(
                429, Duration.ofSeconds(2),
                500, Duration.ofSeconds(1),
                408, Duration.ofSeconds(1),
                503, Duration.ofSeconds(2));

        // Each provider returns a scripted sequence of outcomes, indexed by how many
        // times that provider has been called across the whole run. 0 = success; an
        // HTTP status (429, 500, …) throws that error; TIMEOUT makes the call hang
        // past the Activity's start-to-close timeout so Temporal times the attempt
        // out. Run with an empty prompt to see the 400 (invalid request) abort path.
        // The scripted outcomes drive a three-turn agent loop:
        //   turn 1: anthropic is rate limited (429) until its budget is spent, then
        //           fails over to openai, which answers for the first time.
        //   turn 2: openai returns a server error (500) that spends its budget in
        //           one shot, then fails over to gemini, which answers.
        //   turn 3: gemini's calls hang and time out; after two timeouts spend its
        //           budget it fails over to anthropic, which has recovered and answers.
        private static final Map<String, int[]> MOCK_STATUSES = Map.of(
                "anthropic", new int[] {429, 429, 429},              // three rate-limit responses in turn 1, then recovers
                "openai", new int[] {0, 500},                        // succeeds in turn 1, then a server error in turn 2
                "gemini", new int[] {0, Shared.TIMEOUT, Shared.TIMEOUT}); // answers in turn 2, then two hangs in turn 3

        // Simulated per-call latency (ms) so each provider round-trip takes time, the
        // way a real model call would. Keep it well under the start-to-close timeout.
        private static final long SIMULATED_LATENCY_MS = 2500;

        // A hung call sleeps this long — past the generate Activity's start-to-close
        // timeout — so Temporal kills the attempt with a timeout instead of ever
        // returning. Real model calls stall the same way when a provider is degraded.
        private static final long HUNG_CALL_MS = 20000;

        // Per-provider call counter kept in worker-process memory (like the heartbeat
        // sample's static callIndex), so callProvider walks down each provider's
        // scripted MOCK_STATUSES by itself. NOTE: process-local demo state — it does
        // not survive a worker restart and is not safe across concurrent Workflow
        // executions.
        private static final Map<String, Integer> providerCallCount = new HashMap<>();

        // An error raised by the provider's HTTP client, carrying the status and
        // message the library would surface. A real SDK throws something equivalent;
        // the Activity reads `status` and `message` off it rather than reconstructing.
        private static final class ProviderException extends RuntimeException {
            final int status;

            ProviderException(int status, String message) {
                super(message);
                this.status = status;
            }
        }

        // The model's reasoning output: message text and an optional tool to run next.
        private record Response(String text, String toolCall) {}

        // respond simulates the model's reasoning: it inspects the prompt and either
        // asks to run a tool or returns a final answer. This is what makes the
        // Workflow loop — the model drives an agentic tool-calling cycle.
        private static Response respond(String prompt) {
            if (prompt.contains("[calculator output]")) {
                return new Response(
                        "Durable execution keeps workflow state safe across failures — the answer is 42.",
                        null);
            }
            if (prompt.contains("[search output]")) {
                return new Response("Got the figures; running the numbers.", "calculator");
            }
            return new Response("I need to look that up first.", "search");
        }

        // callProvider stands in for the provider SDK: given the prompt, it waits for
        // the simulated round-trip, then returns the model's response on success or
        // throws a ProviderException carrying the HTTP status and message. It walks
        // down the provider's scripted MOCK_STATUSES, counting calls itself.
        private static Response callProvider(String provider, String prompt) {
            int index = providerCallCount.getOrDefault(provider, 0);
            providerCallCount.put(provider, index + 1);
            int[] statuses = MOCK_STATUSES.get(provider);
            int status = (statuses != null && index < statuses.length) ? statuses[index] : 0;

            // A scripted TIMEOUT is a latency failure: the call hangs so long that the
            // Activity's start-to-close timeout fires and Temporal kills the attempt.
            // The Activity never returns from here — there is no error to catch, which
            // is why the retry has to detect the timeout from its own context (see
            // generate).
            if (status == Shared.TIMEOUT) {
                sleep(HUNG_CALL_MS);
            }

            sleep(SIMULATED_LATENCY_MS);
            if (status != 0) {
                throw new ProviderException(status, provider + " responded HTTP " + status);
            }
            return respond(prompt);
        }

        // pickProvider prefers the caller's default, then sweeps the remaining
        // providers in preference order — starting from the default's position and
        // wrapping around the list — skipping any that have spent their budget. This
        // can be extended with more sophisticated rules.
        private static String pickProvider(
                Map<String, Integer> spent, String defaultProvider, Shared.FallbackConfig config) {
            List<String> providers = config.providers();
            int n = providers.size();
            int start = Math.max(0, providers.indexOf(defaultProvider));
            String last = providers.get((start + n - 1) % n);
            for (int i = 0; i < n; i++) {
                String provider = providers.get((start + i) % n);
                if (spent.getOrDefault(provider, 0) < config.budget()) {
                    return provider;
                }
            }
            // Every provider is exhausted; stay on the last one and let Temporal's
            // maximumAttempts stop the retries.
            return last;
        }

        // chargeTimeouts rebuilds the spent budget after `count` start-to-close
        // timeouts. A timeout leaves no outcome to persist (the attempt was killed
        // mid-call), so instead of storing a running count each attempt replays the
        // timeouts the gap implies. Each one charges the TIMEOUT cost against the
        // provider pickProvider would have chosen; once a provider's spend reaches the
        // budget the sweep fails over to the next one — even though no HTTP error was
        // ever seen.
        private static void chargeTimeouts(
                Map<String, Integer> spent, int count, String defaultProvider, Shared.FallbackConfig config) {
            int cost = config.errorCost().getOrDefault(Shared.TIMEOUT, config.defaultErrorCost());
            for (int i = 0; i < count; i++) {
                String provider = pickProvider(spent, defaultProvider, config);
                spent.merge(provider, cost, Integer::sum);
            }
        }

        @Override
        public Shared.GenerateResult generate(
                String prompt, String defaultProvider, Shared.FallbackConfig config) {
            // A malformed request is an HTTP 400 that no provider will accept — abort.
            if (prompt == null || prompt.isBlank()) {
                throw ApplicationFailure.newNonRetryableFailure("empty prompt (HTTP 400)", "400");
            }

            ActivityExecutionContext ctx = Activity.getExecutionContext();

            // attempt is Temporal's built-in retry counter (1-based); heartbeat details
            // carry the spent budget and the last resolved attempt across retries.
            int attempt = ctx.getInfo().getAttempt();
            Shared.ErrorState errorState = ctx.getHeartbeatDetails(Shared.ErrorState.class)
                    .orElse(new Shared.ErrorState(new HashMap<>(), 0));
            Map<String, Integer> baseSpent =
                    errorState.spent() != null ? errorState.spent() : new HashMap<>();

            // Any attempt since the last one that recorded an HTTP outcome was a
            // timeout — a hung call Temporal killed before it could heartbeat or return
            // a result. The activity context carries no "last failure", so infer those
            // timeouts from the attempt gap and replay them onto a working copy of the
            // budget before picking.
            int timeouts = Math.max(0, attempt - 1 - errorState.lastResolvedAttempt());
            Map<String, Integer> spent = new HashMap<>(baseSpent);
            chargeTimeouts(spent, timeouts, defaultProvider, config);

            // Decide which provider to call: the default until it has spent its budget
            // (to HTTP errors or timeouts), then the next in preference order.
            String provider = pickProvider(spent, defaultProvider, config);

            // Publish the current provider so runTool (same worker) can read it — a
            // convenience hint; the durable budget lives in heartbeat details.
            registry.set(ctx.getInfo().getWorkflowId(), provider);

            System.out.printf(
                    "[%s] attempt %d, %d timeout(s) since last HTTP outcome, budget spent %s%n",
                    provider, attempt, timeouts, spent);

            try {
                Response response = callProvider(provider, prompt);
                return new Shared.GenerateResult(provider, response.text(), response.toolCall());
            } catch (ProviderException err) {
                int status = err.status;

                // 400 Bad Request is permanent — no provider will accept the request.
                if (status == 400) {
                    throw ApplicationFailure.newNonRetryableFailure(err.getMessage(), "400");
                }

                // Transient (408 / 429 / 500 / 503): spend this provider's budget by the
                // error's cost and record this as the last resolved attempt, so later
                // retries count only the timeouts that follow it. pickProvider keeps this
                // provider until its budget runs out, then switches.
                int cost = config.errorCost().getOrDefault(status, config.defaultErrorCost());
                spent.merge(provider, cost, Integer::sum);

                // Persist the running tally (including any replayed timeout failovers) so
                // the retried attempt resumes from here.
                ctx.heartbeat(new Shared.ErrorState(spent, attempt));

                // Retryable: Temporal retries the Activity after the per-status backoff.
                throw ApplicationFailure.newFailureWithCauseAndDelay(
                        err.getMessage() + "; failing over",
                        String.valueOf(status),
                        null,
                        BACKOFF.getOrDefault(status, Duration.ofSeconds(1)));
            }
        }

        @Override
        public String runTool(String tool, String question) {
            // Read the current provider from the injected registry — state generate
            // wrote on this same worker.
            String workflowId = Activity.getExecutionContext().getInfo().getWorkflowId();
            String provider = registry.get(workflowId);
            System.out.printf(
                    "running tool '%s' (generate is currently on provider '%s')%n",
                    tool, provider == null ? "unknown" : provider);
            sleep(500);
            switch (tool) {
                case "search":
                    return "top hit for \"" + question + "\"";
                case "calculator":
                    return "42";
                default:
                    return "";
            }
        }

        private static void sleep(long ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        }
    }
}

// LLMRegistry is worker-local state injected into the Activities: it records the
// provider generate settled on per Workflow so runTool can read it without threading
// it through Workflow arguments. Keyed by Workflow ID so concurrent executions do not
// collide, and safe only because every Activity of one execution runs on the same
// worker (use a worker-specific Task Queue to guarantee that). It is process-local and
// NOT durable — which is why the retry BUDGET travels through heartbeat details
// instead; this registry only shares a convenience hint. Backed by a ConcurrentHashMap
// because the worker runs activities on concurrent threads.
final class LLMRegistry {
    private final Map<String, String> byWorkflow = new ConcurrentHashMap<>();

    void set(String workflowId, String provider) {
        byWorkflow.put(workflowId, provider);
    }

    String get(String workflowId) {
        return byWorkflow.get(workflowId);
    }

    // Production code should evict an entry when the Workflow completes so the map
    // does not grow without bound. The demo runs one short Workflow, so it does not.
    void clear(String workflowId) {
        byWorkflow.remove(workflowId);
    }
}
