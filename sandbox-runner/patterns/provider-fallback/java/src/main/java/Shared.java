import java.util.List;
import java.util.Map;

public final class Shared {
    // The Workflow and the sweeping Activity both run on this Task Queue.
    public static final String TASK_QUEUE = "provider-fallback-task-queue";
    public static final String WORKFLOW_ID_PREFIX = "completion";

    // Maximum number of full passes over the provider list before giving up.
    public static final int MAX_SWEEPS = 3;

    // Maximum agent turns (model calls) before giving up on the tool-calling loop.
    public static final int MAX_TURNS = 6;

    // Sentinel used both as a scripted provider outcome (a hung call) and as the
    // errorCost key for a start-to-close timeout, so a timeout spends the budget the
    // same way an HTTP error does. Not a real HTTP status, hence the negative value.
    public static final int TIMEOUT = -1;

    // What one model call returns: the provider that produced the response, the
    // message text, and an optional tool the model wants to run next. A null or
    // empty toolCall means the model returned a final answer.
    public record GenerateResult(String provider, String text, String toolCall) {}

    // Error state maintained ACROSS Activity retries via heartbeat details, so a
    // retried attempt resumes the sweep where the previous one left off instead of
    // restarting from the first provider. `spent` is the retry budget already spent
    // per provider; `lastResolvedAttempt` is the attempt number that last recorded
    // an HTTP outcome (success or a spent budget) — any retry beyond it without
    // advancing it was a start-to-close timeout, so the gap counts the timeouts.
    public record ErrorState(Map<String, Integer> spent, int lastResolvedAttempt) {}

    // Fallback policy passed into the generate Activity: which providers to sweep
    // in preference order, how much retry budget each one gets before failover,
    // and what each outcome costs against that budget — the errorCost map is keyed
    // by HTTP status and by TIMEOUT, so a timed-out call spends budget like any
    // other error.
    public record FallbackConfig(
            List<String> providers,
            int budget,
            Map<Integer, Integer> errorCost,
            int defaultErrorCost) {}

    private Shared() {}
}
