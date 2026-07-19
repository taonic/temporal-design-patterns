import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import apply_step, compensate_step, hold_reservation
from shared import TASK_QUEUE
from workflows import FulfillmentStep, FulfillOrderWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[FulfillOrderWorkflow, FulfillmentStep],
        activities=[apply_step, hold_reservation, compensate_step],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
