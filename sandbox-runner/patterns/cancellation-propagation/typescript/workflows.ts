import {
  ActivityCancellationType,
  CancellationScope,
  ChildWorkflowCancellationType,
  condition,
  defineSignal,
  executeChild,
  isCancellation,
  proxyActivities,
  setHandler,
  sleep,
  workflowInfo,
} from "@temporalio/workflow";

import type * as activities from "./activities";
import { STEPS, TASK_QUEUE } from "./shared";

const { applyStep, compensateStep } = proxyActivities<typeof activities>({
  startToCloseTimeout: "10 seconds",
});

// The reservation is held open by a long-running, heartbeating activity. A
// short heartbeat timeout lets cancellation reach the activity promptly, and
// WAIT_CANCELLATION_COMPLETED makes the workflow wait for the activity to
// acknowledge the cancellation and run its own cleanup before continuing.
const { holdReservation } = proxyActivities<typeof activities>({
  startToCloseTimeout: "5 minutes",
  heartbeatTimeout: "2 seconds",
  cancellationType: ActivityCancellationType.WAIT_CANCELLATION_COMPLETED,
});

export const stopSignal = defineSignal("stop");

/**
 * Child workflow: applies one fulfillment step, then holds the reservation open
 * in a long-running activity until the order is confirmed or the workflow's
 * scope is cancelled. Cancelling the scope cancels that running activity.
 */
export async function fulfillmentStep(orderId: string, step: string): Promise<void> {
  await applyStep(orderId, step);

  try {
    // Cancelling the scope propagates into this running, heartbeating activity,
    // which rejects with a CancelledFailure.
    await holdReservation(orderId, step);
  } catch (err) {
    if (!isCancellation(err)) throw err;
    // The reservation activity was cancelled; compensate in a non-cancellable
    // scope so the compensation activity can still run.
    await CancellationScope.nonCancellable(() => compensateStep(orderId, step));
    throw err; // Re-raise so the child reports Canceled.
  }
}

/**
 * Parent workflow: starts one child per step inside a cancellation scope and
 * cancels the whole group when a stop is requested.
 */
export async function fulfillOrderWorkflow(orderId: string): Promise<string> {
  let stopRequested = false;
  setHandler(stopSignal, () => {
    stopRequested = true;
  });

  const parentId = workflowInfo().workflowId;
  const scope = new CancellationScope();

  // A scope owns any mix of operations. Alongside the children, start a timer
  // inside it that would fire a follow-up reminder later. Cancelling the scope
  // cancels this pending timer as well as the children. The handler is attached
  // when the timer is created so the CancelledFailure is never left unhandled.
  let reminderCancelled = false;
  let reminder!: Promise<void>;

  // Start every child inside the scope.
  const children = scope.run(() => {
    reminder = sleep("1 hour")
      .then(() => console.log(`Reminder timer fired for ${orderId}`))
      .catch((err) => {
        if (!isCancellation(err)) throw err;
        reminderCancelled = true;
        console.log(`Reminder timer for ${orderId} cancelled with the scope`);
      });
    return Promise.all(
      STEPS.map((step) =>
        executeChild(fulfillmentStep, {
          args: [orderId, step],
          workflowId: `${parentId}/${step}`,
          taskQueue: TASK_QUEUE,
          cancellationType: ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
        })
      )
    );
  });

  // Cancel the whole group when a stop is requested.
  await Promise.race([
    children.catch(() => undefined),
    condition(() => stopRequested).then(() => scope.cancel()),
  ]);

  // Wait for every child to finish its cleanup.
  try {
    await children;
  } catch (err) {
    if (!isCancellation(err)) throw err;
  }

  // The timer created in the scope was cancelled along with the children; wait
  // for its handler to finish.
  await reminder;

  return `Order ${orderId} stopped: cancelled and compensated ${STEPS.length} fulfillment steps (${STEPS.join(", ")})${
    reminderCancelled ? " and cancelled the pending reminder timer" : ""
  }`;
}
