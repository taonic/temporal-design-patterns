import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.workflow import ActivityCancellationType, ChildWorkflowCancellationType

with workflow.unsafe.imports_passed_through():
    from activities import apply_step, compensate_step, hold_reservation
    from shared import STEPS, TASK_QUEUE


@workflow.defn
class FulfillmentStep:
    """Child workflow: applies one fulfillment step and holds it until the order
    is confirmed or cancelled, compensating on cancellation."""

    @workflow.run
    async def run(self, order_id: str, step: str) -> None:
        await workflow.execute_activity(
            apply_step,
            args=[order_id, step],
            start_to_close_timeout=timedelta(seconds=10),
        )

        # Hold the reservation open in a long-running, heartbeating activity
        # until the workflow is cancelled. The activity runs in its own task so
        # that this workflow method can still schedule compensation after the
        # cancellation is delivered.
        hold = asyncio.create_task(
            workflow.execute_activity(
                hold_reservation,
                args=[order_id, step],
                start_to_close_timeout=timedelta(minutes=5),
                heartbeat_timeout=timedelta(seconds=2),
                cancellation_type=ActivityCancellationType.WAIT_CANCELLATION_COMPLETED,
            )
        )

        try:
            # Shield the hold task so cancellation lands here, not inside it.
            await asyncio.shield(hold)
        except asyncio.CancelledError:
            # Cancel the reservation activity and wait for it to release.
            hold.cancel()
            try:
                await hold
            except Exception:
                pass
            # Compensate before allowing the cancellation to proceed.
            await workflow.execute_activity(
                compensate_step,
                args=[order_id, step],
                start_to_close_timeout=timedelta(seconds=10),
            )
            raise  # Re-raise so the child reports Canceled.


@workflow.defn
class FulfillOrderWorkflow:
    """Parent workflow: starts one child per step and cancels the whole group
    through a single cancellation when a stop is requested."""

    def __init__(self) -> None:
        self._stop = False

    @workflow.run
    async def run(self, order_id: str) -> str:
        parent_id = workflow.info().workflow_id

        # Start every child in its own task. Cancelling a task that is executing
        # a child workflow sends a durable cancellation request to that child.
        # See:
        # https://temporal.io/blog/durable-distributed-asyncio-event-loop#cancellation
        children = [
            asyncio.create_task(
                workflow.execute_child_workflow(
                    FulfillmentStep.run,
                    args=[order_id, step],
                    id=f"{parent_id}/{step}",
                    task_queue=TASK_QUEUE,
                    cancellation_type=ChildWorkflowCancellationType.WAIT_CANCELLATION_COMPLETED,
                )
            )
            for step in STEPS
        ]

        # A scope owns any mix of operations. Alongside the children, start a
        # timer that would fire a follow-up reminder later. Cancelling the group
        # cancels this pending timer as well as the children.
        reminder = asyncio.create_task(
            asyncio.sleep(timedelta(hours=1).total_seconds())
        )

        # Wait until a stop is requested or every child has finished.
        await workflow.wait_condition(
            lambda: self._stop or all(child.done() for child in children)
        )

        # Cancel the whole group.
        if self._stop:
            for child in children:
                child.cancel()
        # The reminder timer is part of the same group; cancel it too.
        reminder.cancel()

        # asyncio.gather with return_exceptions=True waits for every child to
        # finish its cleanup and collects each cancellation result, so none is
        # left unretrieved.
        await asyncio.gather(*children, return_exceptions=True)

        # The cancelled timer raises CancelledError when awaited.
        reminder_cancelled = False
        try:
            await reminder
        except asyncio.CancelledError:
            reminder_cancelled = True
            workflow.logger.info(f"Reminder timer for {order_id} cancelled with the scope")

        return (
            f"Order {order_id} stopped: cancelled and compensated "
            f"{len(STEPS)} fulfillment steps ({', '.join(STEPS)})"
            + (" and cancelled the pending reminder timer" if reminder_cancelled else "")
        )

    @workflow.signal
    def stop(self) -> None:
        self._stop = True
