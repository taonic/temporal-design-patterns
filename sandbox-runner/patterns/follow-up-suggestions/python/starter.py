import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    on = await client.execute_workflow(
        AgentSessionWorkflow.run, args=["deploy", True],
        id=f"sug-on-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    off = await client.execute_workflow(
        AgentSessionWorkflow.run, args=["deploy", False],
        id=f"sug-off-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    print(f"on={on}|off={off}")

if __name__ == "__main__":
    asyncio.run(main())
