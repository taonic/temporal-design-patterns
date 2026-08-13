import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "pay"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await asyncio.sleep(0.2)
    await handle.signal(AgentSessionWorkflow.extend_deadline, 5.0)
    await handle.signal(AgentSessionWorkflow.approve, "granted")
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
