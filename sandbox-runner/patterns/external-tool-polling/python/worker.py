import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import poll_job_until_done, start_job
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[start_job, poll_job_until_done],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
