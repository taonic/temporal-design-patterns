import io.temporal.activity.ActivityOptions;
import io.temporal.activity.LocalActivityOptions;
import io.temporal.workflow.UpdateMethod;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

import java.time.Duration;

@WorkflowInterface
public interface TransactionWorkflow {
    @WorkflowMethod
    Shared.Transaction processTransaction(Shared.TransactionRequest req);

    @UpdateMethod
    Shared.Transaction returnInitResult();

    final class Impl implements TransactionWorkflow {
        private final Activities localActivities = Workflow.newLocalActivityStub(
                Activities.class,
                LocalActivityOptions.newBuilder()
                        .setScheduleToCloseTimeout(Duration.ofSeconds(5))
                        .build());

        private final Activities activities = Workflow.newActivityStub(
                Activities.class,
                ActivityOptions.newBuilder()
                        .setStartToCloseTimeout(Duration.ofSeconds(30))
                        .build());

        private boolean initDone = false;
        private Shared.Transaction tx;
        private RuntimeException initError;

        @Override
        public Shared.Transaction processTransaction(Shared.TransactionRequest req) {
            // Phase 1: fast synchronous initialization (local activity).
            try {
                this.tx = localActivities.initTransaction(req);
            } catch (RuntimeException e) {
                this.initError = e;
            } finally {
                this.initDone = true;
            }

            // Phase 2: slow asynchronous completion.
            if (initError != null) {
                activities.cancelTransaction(tx);
                return null;
            }

            activities.completeTransaction(tx);
            return tx;
        }

        @Override
        public Shared.Transaction returnInitResult() {
            Workflow.await(() -> initDone);
            if (initError != null) {
                throw Workflow.wrap(initError);
            }
            return tx;
        }
    }
}
