import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow
from activities import ship_external

async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(client, task_queue=TASK_QUEUE, workflows=[AgentTurnWorkflow], activities=[ship_external])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
