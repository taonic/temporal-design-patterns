import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import risky_tool
from shared import TASK_QUEUE
from workflows import ChildTurnWorkflow, ParentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ParentSessionWorkflow, ChildTurnWorkflow],
        activities=[risky_tool],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
