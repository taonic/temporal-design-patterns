import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    pure = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["normalize", "  Hi "],
        id=f"ect-p-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    state = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["remember", "note"],
        id=f"ect-s-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    ext = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["ship", "artifact"],
        id=f"ect-e-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    print(f"pure={pure}|state={state}|external={ext}")

if __name__ == "__main__":
    asyncio.run(main())
