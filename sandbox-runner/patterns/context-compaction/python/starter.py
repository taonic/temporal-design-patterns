import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    memory = {
        "turns": ["t0", "t1"],
        "open_items": ["approve refund"],
        "summary": "",
    }
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, memory, 0],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
