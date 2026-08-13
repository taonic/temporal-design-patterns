import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    viewer_id = f"session-{uuid.uuid4().hex[:8]}"
    admin_id = f"session-{uuid.uuid4().hex[:8]}"
    viewer = await client.execute_workflow(
        AgentSessionWorkflow.run,
        args=[viewer_id, {"role": "viewer"}, "hello"],
        id=viewer_id,
        task_queue=TASK_QUEUE,
    )
    admin = await client.execute_workflow(
        AgentSessionWorkflow.run,
        args=[admin_id, {"role": "admin"}, "hello"],
        id=admin_id,
        task_queue=TASK_QUEUE,
    )
    print(f"viewer={viewer}|admin={admin}")


if __name__ == "__main__":
    asyncio.run(main())
