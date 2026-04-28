public final class Shared {
    public static final String TASK_QUEUE = "saga-task-queue";
    public static final String WORKFLOW_ID_PREFIX = "open-account";

    public record OpenAccountRequest(
            String accountId,
            String clientName,
            String clientEmail,
            String address,
            String bankAccount) {}

    private Shared() {}
}
