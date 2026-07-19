import io.temporal.activity.ActivityCancellationType;
import io.temporal.activity.ActivityOptions;
import io.temporal.failure.ActivityFailure;
import io.temporal.failure.CanceledFailure;
import io.temporal.failure.ChildWorkflowFailure;
import io.temporal.workflow.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

@WorkflowInterface
public interface CancellationPropagationWorkflow {

    /** Parent workflow: cancels every child through one scope on stop. */
    @WorkflowInterface
    interface Parent {
        @WorkflowMethod
        String run(String orderId);

        @SignalMethod
        void stop();
    }

    /** Child workflow: applies one fulfillment step and compensates on cancel. */
    @WorkflowInterface
    interface Child {
        @WorkflowMethod
        void run(String orderId, String step);
    }

    final class ParentImpl implements Parent {
        private boolean stopRequested = false;

        @Override
        public String run(String orderId) {
            String parentId = Workflow.getInfo().getWorkflowId();
            List<Promise<Void>> results = new ArrayList<>();

            // A scope owns any mix of operations. Alongside the children, start a
            // timer inside the scope that would fire a follow-up reminder later.
            // Cancelling the scope cancels this pending timer as well.
            @SuppressWarnings("unchecked")
            final Promise<Void>[] reminderHolder = new Promise[1];

            // Start every child inside one cancellation scope.
            CancellationScope scope =
                    Workflow.newCancellationScope(
                            () -> {
                                reminderHolder[0] = Workflow.newTimer(Duration.ofHours(1));
                                for (String step : Shared.STEPS) {
                                    ChildWorkflowOptions opts =
                                            ChildWorkflowOptions.newBuilder()
                                                    .setWorkflowId(parentId + "/" + step)
                                                    .setTaskQueue(Shared.TASK_QUEUE)
                                                    .setCancellationType(
                                                            ChildWorkflowCancellationType
                                                                    .WAIT_CANCELLATION_COMPLETED)
                                                    .build();
                                    Child child = Workflow.newChildWorkflowStub(Child.class, opts);
                                    results.add(Async.procedure(child::run, orderId, step));
                                }
                            });
            scope.run();

            // Cancel the whole group when a stop is requested.
            Promise<Void> all = Promise.allOf(results);
            Workflow.await(() -> stopRequested || all.isCompleted());
            if (stopRequested) {
                scope.cancel("Order stopped");
            }

            // Wait for every child to finish its cleanup.
            for (Promise<Void> result : results) {
                try {
                    result.get();
                } catch (ChildWorkflowFailure e) {
                    if (!(e.getCause() instanceof CanceledFailure)) {
                        throw e;
                    }
                }
            }

            // The timer created inside the scope is cancelled along with the
            // children; its Promise completes with a CanceledFailure.
            boolean reminderCancelled = false;
            try {
                reminderHolder[0].get();
            } catch (CanceledFailure e) {
                reminderCancelled = true;
                Workflow.getLogger(getClass())
                        .info("Reminder timer for {} cancelled with the scope", orderId);
            }

            return "Order " + orderId + " stopped: cancelled and compensated "
                    + Shared.STEPS.size() + " fulfillment steps ("
                    + String.join(", ", Shared.STEPS) + ")"
                    + (reminderCancelled ? " and cancelled the pending reminder timer" : "");
        }

        @Override
        public void stop() {
            stopRequested = true;
        }
    }

    final class ChildImpl implements Child {
        private final Activities activities =
                Workflow.newActivityStub(
                        Activities.class,
                        ActivityOptions.newBuilder()
                                .setStartToCloseTimeout(Duration.ofSeconds(10))
                                .build());

        // The reservation is held open by a long-running, heartbeating activity.
        // A short heartbeat timeout lets cancellation reach the activity
        // promptly, and WAIT_CANCELLATION_COMPLETED makes the workflow wait for
        // the activity to acknowledge the cancellation and run its own cleanup.
        private final Activities holdActivities =
                Workflow.newActivityStub(
                        Activities.class,
                        ActivityOptions.newBuilder()
                                .setStartToCloseTimeout(Duration.ofMinutes(5))
                                .setHeartbeatTimeout(Duration.ofSeconds(2))
                                .setCancellationType(
                                        ActivityCancellationType.WAIT_CANCELLATION_COMPLETED)
                                .build());

        @Override
        public void run(String orderId, String step) {
            activities.applyStep(orderId, step);
            try {
                // Cancelling the scope propagates into this running, heartbeating
                // activity, which fails with a CanceledFailure.
                holdActivities.holdReservation(orderId, step);
            } catch (ActivityFailure e) {
                if (!(e.getCause() instanceof CanceledFailure)) {
                    throw e;
                }
                // Compensate in a detached scope so the activity can still run.
                Workflow.newDetachedCancellationScope(
                                () -> activities.compensateStep(orderId, step))
                        .run();
                throw e; // Re-raise so the child reports Canceled.
            }
        }
    }
}
