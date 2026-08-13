import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    safe = await client.execute_workflow(
        AgentTurnWorkflow.run, "ls",
        id=f"csc-safe-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    forbidden = await client.execute_workflow(
        AgentTurnWorkflow.run, "rm -rf /",
        id=f"csc-bad-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    wid = f"csc-appr-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentTurnWorkflow.run, "npm install left-pad",
        id=wid, task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentTurnWorkflow.approve, "granted")
    approved = await handle.result()
    print(f"safe={safe}|forbidden={forbidden}|approved={approved}")

if __name__ == "__main__":
    asyncio.run(main())
