import io.temporal.activity.ActivityOptions;
import io.temporal.common.RetryOptions;
import io.temporal.workflow.Saga;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

import java.time.Duration;

@WorkflowInterface
public interface TransferMoneyWorkflow {
    @WorkflowMethod
    String transfer(Shared.TransferDetails details);

    final class Impl implements TransferMoneyWorkflow {
        private final Activities activities = Workflow.newActivityStub(
                Activities.class,
                ActivityOptions.newBuilder()
                        .setStartToCloseTimeout(Duration.ofSeconds(10))
                        .setRetryOptions(RetryOptions.newBuilder().setMaximumAttempts(1).build())
                        .build());

        @Override
        public String transfer(Shared.TransferDetails details) {
            Saga saga = new Saga(new Saga.Options.Builder().setParallelCompensation(false).build());

            try {
                Workflow.getLogger(TransferMoneyWorkflow.class)
                        .info("Starting transfer {}: ${}", details.transferId(), details.amount());

                saga.addCompensation(activities::withdrawCompensation, details);
                activities.withdraw(details);

                saga.addCompensation(activities::depositCompensation, details);
                activities.deposit(details);

                activities.notifyDownstream(details);

                return "Transfer " + details.transferId() + " completed";
            } catch (Exception e) {
                Workflow.getLogger(TransferMoneyWorkflow.class)
                        .warn("Transfer {} failed ({}); running compensations",
                                details.transferId(), e.getMessage());
                saga.compensate();
                // Return a status instead of re-throwing so the workflow execution
                // itself succeeds. Re-throwing is the canonical pattern (see
                // saga-pattern.md best practices); this demo prefers a clean ✅
                // in the Temporal UI and surfaces the rollback via the result.
                return "Transfer " + details.transferId() + " rolled back: " + e.getMessage();
            }
        }
    }
}
