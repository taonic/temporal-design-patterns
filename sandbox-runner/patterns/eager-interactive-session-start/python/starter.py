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
        args=[session_id],
        id=session_id,
        task_queue=TASK_QUEUE,
        start_signal="user_message",
        start_signal_args=["hello"],
        request_eager_start=True,
    )
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
