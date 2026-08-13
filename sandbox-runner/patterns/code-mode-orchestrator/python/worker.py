import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import host_search, host_summarize, run_script

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[host_search, host_summarize, run_script],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
