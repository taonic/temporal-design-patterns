import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import HumanDecision, ParentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        ParentSessionWorkflow.run,
        args=[session_id, 50],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await asyncio.sleep(0.4)
    await handle.signal(
        ParentSessionWorkflow.human_decision,
        HumanDecision(request_id="r1", status="granted"),
    )
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
