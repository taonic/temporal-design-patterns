import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    ro = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["write ./x", "read-only"],
        id=f"spt-ro-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    ww = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["write ./x", "workspace-write"],
        id=f"spt-ww-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    fa = await client.execute_workflow(
        AgentTurnWorkflow.run, args=["write /etc/hosts", "full-access"],
        id=f"spt-fa-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    print(f"ro={ro}|ww={ww}|fa={fa}")

if __name__ == "__main__":
    asyncio.run(main())
