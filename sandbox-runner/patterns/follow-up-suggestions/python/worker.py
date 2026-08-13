import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow
from activities import answer_turn, generate_suggestions

async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client, task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[answer_turn, generate_suggestions],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
