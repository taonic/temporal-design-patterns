import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import fetch_batch, process_record
from shared import TASK_QUEUE
from workflows import DataProcessorWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[DataProcessorWorkflow],
        activities=[fetch_batch, process_record],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
