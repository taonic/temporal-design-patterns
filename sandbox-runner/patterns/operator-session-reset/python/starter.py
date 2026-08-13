import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, RestoreRequest


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, {"note": "initial"}, 0],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentSessionWorkflow.user_message, "hello")
    await asyncio.sleep(0.3)
    await handle.signal(
        AgentSessionWorkflow.operator_restore,
        RestoreRequest(snapshot={"note": "clean"}, reason="bad_state"),
    )
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
