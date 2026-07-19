import asyncio
import time

from temporalio.client import Client

from shared import TASK_QUEUE, WORKFLOW_ID_PREFIX
from workflows import FulfillOrderWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    workflow_id = f"{WORKFLOW_ID_PREFIX}-{int(time.time() * 1000)}"
    order_id = "order-42"

    handle = await client.start_workflow(
        FulfillOrderWorkflow.run,
        order_id,
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )
    print(f"Started workflow: {workflow_id}")
    print(f"Fulfilling {order_id}; children are reserving resources concurrently…")

    # Let the children apply their steps, then request a stop.
    await asyncio.sleep(2)
    print("Requesting stop; cancellation will propagate to every child…")
    await handle.signal(FulfillOrderWorkflow.stop)

    result = await handle.result()
    print(result)
    print(
        f"Open the Temporal UI and search for '{workflow_id}' to see each child "
        f"transition to Canceled after compensating."
    )


if __name__ == "__main__":
    asyncio.run(main())
