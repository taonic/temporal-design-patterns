import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import transfer_funds

TASK_QUEUE = "agentic-patterns"


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
