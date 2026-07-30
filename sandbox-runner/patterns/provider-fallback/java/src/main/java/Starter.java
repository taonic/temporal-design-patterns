import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowOptions;
import io.temporal.serviceclient.WorkflowServiceStubs;

public class Starter {
    public static void main(String[] args) {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);

        String workflowId = Shared.WORKFLOW_ID_PREFIX + "-" + System.currentTimeMillis();
        // Change to "" (empty) to exercise the abort (invalid request) path.
        String question = "What is the meaning of durable execution?";

        CompletionWorkflow workflow = client.newWorkflowStub(
                CompletionWorkflow.class,
                WorkflowOptions.newBuilder()
                        .setTaskQueue(Shared.TASK_QUEUE)
                        .setWorkflowId(workflowId)
                        .build());

        System.out.println("Started workflow: " + workflowId);

        String result = workflow.providerFallback(question);
        System.out.println(result);
        System.out.println("Open the Temporal UI and search for '" + workflowId
                + "' to see the agent loop and provider sweep.");
    }
}
