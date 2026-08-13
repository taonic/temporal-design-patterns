import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import call_model
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, AgentTurnWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow, AgentTurnWorkflow],
        activities=[call_model],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
