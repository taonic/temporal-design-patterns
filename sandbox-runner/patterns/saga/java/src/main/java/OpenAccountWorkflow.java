import io.temporal.activity.ActivityOptions;
import io.temporal.common.RetryOptions;
import io.temporal.workflow.Saga;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

import java.time.Duration;

@WorkflowInterface
public interface OpenAccountWorkflow {
    @WorkflowMethod
    String openAccount(Shared.OpenAccountRequest req);

    final class Impl implements OpenAccountWorkflow {
        private final Activities activities = Workflow.newActivityStub(
                Activities.class,
                ActivityOptions.newBuilder()
                        .setStartToCloseTimeout(Duration.ofSeconds(10))
                        .setRetryOptions(RetryOptions.newBuilder().setMaximumAttempts(1).build())
                        .build());

        @Override
        public String openAccount(Shared.OpenAccountRequest req) {
            Saga saga = new Saga(new Saga.Options.Builder().setParallelCompensation(false).build());

            try {
                Workflow.getLogger(OpenAccountWorkflow.class)
                        .info("Opening account {} for {}", req.accountId(), req.clientName());

                // Step 1: createAccount has no compensation registered — leaving
                // an empty account stub on later failure is acceptable for this demo.
                activities.createAccount(req);

                saga.addCompensation(activities::clearPostalAddresses, req);
                activities.addAddress(req);

                saga.addCompensation(activities::removeClient, req);
                activities.addClient(req);

                saga.addCompensation(activities::disconnectBankAccounts, req);
                activities.addBankAccount(req);

                return "Account " + req.accountId() + " opened";
            } catch (Exception e) {
                Workflow.getLogger(OpenAccountWorkflow.class)
                        .warn("Account {} failed ({}); running compensations",
                                req.accountId(), e.getMessage());
                saga.compensate();
                // Return a status instead of re-throwing so the workflow execution
                // itself succeeds. Re-throwing is the canonical pattern (see
                // saga-pattern.md best practices); this demo prefers a clean ✅
                // in the Temporal UI and surfaces the rollback via the result.
                return "Account " + req.accountId() + " rolled back: " + e.getMessage();
            }
        }
    }
}
