import asyncio
import time

from temporalio.client import Client

from shared import TASK_QUEUE, WORKFLOW_ID_PREFIX
from workflows import DataProcessorWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    workflow_id = f"{WORKFLOW_ID_PREFIX}-{int(time.time() * 1000)}"
    handle = await client.start_workflow(
        DataProcessorWorkflow.run,
        args=["", 0],
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )
    print(f"Started workflow: {workflow_id}")

    total = await handle.result()
    print(f"Final result: processed {total} records")
    print(
        f"Open the Temporal UI and search for '{workflow_id}' to see the Continue-As-New chain."
    )


if __name__ == "__main__":
    asyncio.run(main())
