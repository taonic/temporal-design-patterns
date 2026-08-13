import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import transfer_funds
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[transfer_funds],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
