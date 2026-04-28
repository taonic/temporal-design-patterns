import asyncio
import time

from temporalio.client import Client

from shared import TASK_QUEUE, WORKFLOW_ID_PREFIX, OpenAccountRequest
from workflows import OpenAccountWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    account_id = f"{WORKFLOW_ID_PREFIX}-{int(time.time() * 1000)}"
    request = OpenAccountRequest(
        accountId=account_id,
        clientName="Alice Example",
        clientEmail="alice@example.com",
        address="123 Main St, Brooklyn NY",
        bankAccount="DE89-3704-0044-0532-0130-00",
    )

    handle = await client.start_workflow(
        OpenAccountWorkflow.run,
        request,
        id=account_id,
        task_queue=TASK_QUEUE,
    )
    print(f"Started workflow: {account_id}")

    result = await handle.result()
    print(result)
    print(f"Open the Temporal UI and search for '{account_id}' to see the saga history.")


if __name__ == "__main__":
    asyncio.run(main())
