import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentTurnWorkflow.run,
        args=[session_id, "please refund"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    for _ in range(50):
        q = await handle.query(AgentTurnWorkflow.pending_question)
        if q:
            break
        await asyncio.sleep(0.1)
    await handle.execute_update(AgentTurnWorkflow.answer, "50")
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
