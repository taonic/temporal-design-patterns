import io.temporal.api.enums.v1.WorkflowIdConflictPolicy;
import io.temporal.client.UpdateOptions;
import io.temporal.client.WithStartWorkflowOperation;
import io.temporal.client.WorkflowClient;
import io.temporal.client.WorkflowOptions;
import io.temporal.client.WorkflowStub;
import io.temporal.client.WorkflowUpdateHandle;
import io.temporal.client.WorkflowUpdateStage;
import io.temporal.serviceclient.WorkflowServiceStubs;

public class Starter {
    public static void main(String[] args) throws Exception {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);

        String transactionId = Shared.WORKFLOW_ID_PREFIX + "-" + System.currentTimeMillis();
        Shared.TransactionRequest req = new Shared.TransactionRequest(100.0, "USD");

        TransactionWorkflow workflow = client.newWorkflowStub(
                TransactionWorkflow.class,
                WorkflowOptions.newBuilder()
                        .setTaskQueue(Shared.TASK_QUEUE)
                        .setWorkflowId(transactionId)
                        .setWorkflowIdConflictPolicy(
                                WorkflowIdConflictPolicy.WORKFLOW_ID_CONFLICT_POLICY_FAIL)
                        .build());

        long t0 = System.currentTimeMillis();
        WorkflowUpdateHandle<Shared.Transaction> updateHandle =
                WorkflowClient.startUpdateWithStart(
                        workflow::returnInitResult,
                        UpdateOptions.<Shared.Transaction>newBuilder()
                                .setWaitForStage(WorkflowUpdateStage.COMPLETED)
                                .build(),
                        new WithStartWorkflowOperation<>(workflow::processTransaction, req));

        Shared.Transaction tx = updateHandle.getResultAsync().get();
        System.out.printf("Early return after %dms: %s (status=%s)%n",
                System.currentTimeMillis() - t0, tx.id(), tx.status());

        WorkflowStub stub = WorkflowStub.fromTyped(workflow);
        Shared.Transaction finalTx = stub.getResult(Shared.Transaction.class);
        System.out.printf("Workflow completed after %dms: %s (status=%s)%n",
                System.currentTimeMillis() - t0,
                finalTx == null ? "null" : finalTx.id(),
                finalTx == null ? "n/a" : finalTx.status());
        System.out.println("Open the Temporal UI and search for '" + transactionId
                + "' to see the history.");

        System.exit(0);
    }
}
