public final class Shared {
    public static final String TASK_QUEUE = "saga-task-queue";
    public static final String WORKFLOW_ID_PREFIX = "transfer";

    public record TransferDetails(String transferId, String fromAccount, String toAccount, int amount) {}

    private Shared() {}
}
