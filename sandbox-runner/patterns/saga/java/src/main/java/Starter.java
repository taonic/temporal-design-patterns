import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowOptions;
import io.temporal.serviceclient.WorkflowServiceStubs;

public class Starter {
    public static void main(String[] args) {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);

        String accountId = Shared.WORKFLOW_ID_PREFIX + "-" + System.currentTimeMillis();
        Shared.OpenAccountRequest req = new Shared.OpenAccountRequest(
                accountId,
                "Alice Example",
                "alice@example.com",
                "123 Main St, Brooklyn NY",
                "DE89-3704-0044-0532-0130-00");

        OpenAccountWorkflow workflow = client.newWorkflowStub(
                OpenAccountWorkflow.class,
                WorkflowOptions.newBuilder()
                        .setTaskQueue(Shared.TASK_QUEUE)
                        .setWorkflowId(accountId)
                        .build());

        System.out.println("Started workflow: " + accountId);

        String result = workflow.openAccount(req);
        System.out.println(result);
        System.out.println("Open the Temporal UI and search for '" + accountId
                + "' to see the saga history.");
    }
}
