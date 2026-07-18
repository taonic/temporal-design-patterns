import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowOptions;
import io.temporal.client.WorkflowStub;
import io.temporal.serviceclient.WorkflowServiceStubs;

public class Starter {
    public static void main(String[] args) throws InterruptedException {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);

        String workflowId = Shared.WORKFLOW_ID_PREFIX + "-" + System.currentTimeMillis();
        String orderId = "order-42";

        CancellationPropagationWorkflow.Parent workflow =
                client.newWorkflowStub(
                        CancellationPropagationWorkflow.Parent.class,
                        WorkflowOptions.newBuilder()
                                .setTaskQueue(Shared.TASK_QUEUE)
                                .setWorkflowId(workflowId)
                                .build());

        // Start asynchronously so the running workflow can be signalled.
        WorkflowClient.start(workflow::run, orderId);
        System.out.println("Started workflow: " + workflowId);
        System.out.println(
                "Fulfilling " + orderId + "; children are reserving resources concurrently…");

        // Let the children apply their steps, then request a stop.
        Thread.sleep(2000);
        System.out.println("Requesting stop; cancellation will propagate to every child…");
        workflow.stop();

        String result = WorkflowStub.fromTyped(workflow).getResult(String.class);
        System.out.println(result);
        System.out.println(
                "Open the Temporal UI and search for '" + workflowId
                        + "' to see each child transition to Canceled after compensating.");
    }
}
