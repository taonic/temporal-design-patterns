import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import cancel_transaction, complete_transaction, init_transaction
from shared import TASK_QUEUE
from workflows import TransactionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[TransactionWorkflow],
        activities=[init_transaction, complete_transaction, cancel_transaction],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
