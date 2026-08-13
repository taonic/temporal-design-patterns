import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, Principal

async def main() -> None:
    client = await Client.connect("localhost:7233")
    owner = Principal("user-1", "user")
    ok = await client.execute_workflow(
        AgentSessionWorkflow.run, args=[owner, owner],
        id=f"ivc-ok-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    other = Principal("user-2", "user")
    bad = await client.execute_workflow(
        AgentSessionWorkflow.run, args=[owner, other],
        id=f"ivc-bad-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    print(f"ok={ok}|bad={bad}")

if __name__ == "__main__":
    asyncio.run(main())
