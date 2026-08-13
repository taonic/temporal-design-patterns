import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import compact_session_memory
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[compact_session_memory],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
