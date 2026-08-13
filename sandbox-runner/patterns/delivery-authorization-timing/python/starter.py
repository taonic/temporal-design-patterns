import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, Delivery


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    owner = "tenant-a"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, owner],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await asyncio.sleep(0.3)
    await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery("d1", "hello", "user-1", owner),
    )
    await asyncio.sleep(0.4)
    await handle.signal(AgentSessionWorkflow.revoke_actor, "user-1")
    await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery("d2", "later", "user-1", owner),
    )
    await handle.signal(AgentSessionWorkflow.stop)
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
