import java.util.List;

public final class Shared {
    public static final String TASK_QUEUE = "cancellation-propagation-task-queue";
    public static final String WORKFLOW_ID_PREFIX = "cancellation-propagation";
    public static final List<String> STEPS =
            List.of("reserve-inventory", "authorize-payment", "book-shipping");

    private Shared() {}
}
