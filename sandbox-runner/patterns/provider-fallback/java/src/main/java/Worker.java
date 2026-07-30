import io.temporal.client.WorkflowClient;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.worker.WorkerFactory;

public class Worker {
    public static void main(String[] args) {
        WorkflowServiceStubs service = WorkflowServiceStubs.newLocalServiceStubs();
        WorkflowClient client = WorkflowClient.newInstance(service);

        // One registry shared by every Activity this worker runs, injected into the
        // activities instance instead of reached for as a static field. See the note in
        // CompletionActivities.java on why this is safe only for same-worker,
        // per-Workflow-keyed state.
        LLMRegistry registry = new LLMRegistry();

        WorkerFactory factory = WorkerFactory.newInstance(client);
        io.temporal.worker.Worker worker = factory.newWorker(Shared.TASK_QUEUE);
        worker.registerWorkflowImplementationTypes(CompletionWorkflow.Impl.class);
        worker.registerActivitiesImplementations(new CompletionActivities.Impl(registry));

        System.out.println("Worker listening on task queue '" + Shared.TASK_QUEUE + "'");
        factory.start();

        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
