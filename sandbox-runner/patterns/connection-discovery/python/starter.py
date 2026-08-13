import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    hit = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["linear", "linear__list_issues"],
        id=f"cd-hit-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    miss = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["linear", "github__list_prs"],
        id=f"cd-miss-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    print(f"hit={hit}|miss={miss}")

if __name__ == "__main__":
    asyncio.run(main())
