import asyncio

from temporalio import activity


@activity.defn
async def apply_step(order_id: str, step: str) -> None:
    """Reserve a resource for one fulfillment step."""
    print(f"Applied {step} for order {order_id}", flush=True)
    # Simulate holding a real reservation.
    await asyncio.sleep(0.1)


@activity.defn
async def hold_reservation(order_id: str, step: str) -> None:
    """Long-running activity that keeps the reservation open until it is
    cancelled. It heartbeats on each iteration so the server can deliver the
    cancellation request."""
    print(f"Holding {step} for order {order_id}", flush=True)
    try:
        while True:
            activity.heartbeat(step)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f"Reservation for {step} released on cancellation", flush=True)
        raise


@activity.defn
async def compensate_step(order_id: str, step: str) -> None:
    """Undo a previously applied fulfillment step."""
    print(f"Compensated {step} for order {order_id}", flush=True)
    await asyncio.sleep(0.1)
