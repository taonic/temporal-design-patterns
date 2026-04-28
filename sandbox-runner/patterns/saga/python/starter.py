import asyncio
import time

from temporalio.client import Client

from shared import TASK_QUEUE, WORKFLOW_ID_PREFIX, TransferDetails
from workflows import TransferMoneyWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    transfer_id = f"{WORKFLOW_ID_PREFIX}-{int(time.time() * 1000)}"
    details = TransferDetails(
        transferId=transfer_id,
        fromAccount="alice",
        toAccount="bob",
        amount=100,
    )

    handle = await client.start_workflow(
        TransferMoneyWorkflow.run,
        details,
        id=transfer_id,
        task_queue=TASK_QUEUE,
    )
    print(f"Started workflow: {transfer_id}")

    result = await handle.result()
    print(result)
    print(f"Open the Temporal UI and search for '{transfer_id}' to see the saga history.")


if __name__ == "__main__":
    asyncio.run(main())
