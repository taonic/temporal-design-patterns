import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    result = await client.execute_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "same-input"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
