import { CancelledFailure, Context } from "@temporalio/activity";

export async function applyStep(orderId: string, step: string): Promise<void> {
  // Reserve a resource for one fulfillment step.
  console.log(`Applied ${step} for order ${orderId}`);
  // Simulate holding a real reservation.
  await new Promise((r) => setTimeout(r, 100));
}

export async function holdReservation(orderId: string, step: string): Promise<void> {
  // Long-running activity that keeps the reservation open until it is cancelled.
  console.log(`Holding ${step} for order ${orderId}`);
  const ctx = Context.current();
  try {
    for (let i = 0; ; i++) {
      // Heartbeat so the server can deliver the cancellation request, then wait.
      // Context.sleep is cancellation-aware: it rejects with CancelledFailure
      // as soon as the activity is cancelled.
      ctx.heartbeat(i);
      await ctx.sleep(1000);
    }
  } catch (err) {
    if (err instanceof CancelledFailure) {
      console.log(`Reservation for ${step} released on cancellation`);
    }
    throw err;
  }
}

export async function compensateStep(orderId: string, step: string): Promise<void> {
  // Undo a previously applied fulfillment step.
  console.log(`Compensated ${step} for order ${orderId}`);
  await new Promise((r) => setTimeout(r, 100));
}
