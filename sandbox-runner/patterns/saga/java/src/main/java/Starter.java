import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowOptions;
import io.temporal.serviceclient.WorkflowServiceStubs;

public class Starter {
    public static void main(String[] args) {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);

        String transferId = Shared.WORKFLOW_ID_PREFIX + "-" + System.currentTimeMillis();
        Shared.TransferDetails details = new Shared.TransferDetails(transferId, "alice", "bob", 100);

        TransferMoneyWorkflow workflow = client.newWorkflowStub(
                TransferMoneyWorkflow.class,
                WorkflowOptions.newBuilder()
                        .setTaskQueue(Shared.TASK_QUEUE)
                        .setWorkflowId(transferId)
                        .build());

        System.out.println("Started workflow: " + transferId);

        String result = workflow.transfer(details);
        System.out.println(result);
        System.out.println("Open the Temporal UI and search for '" + transferId
                + "' to see the saga history.");
    }
}
