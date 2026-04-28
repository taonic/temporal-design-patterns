import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import (
    deposit,
    deposit_compensation,
    notify_downstream,
    withdraw,
    withdraw_compensation,
)
from shared import TASK_QUEUE
from workflows import TransferMoneyWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[TransferMoneyWorkflow],
        activities=[
            withdraw,
            deposit,
            notify_downstream,
            withdraw_compensation,
            deposit_compensation,
        ],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
