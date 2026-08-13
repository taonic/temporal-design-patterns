import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    down_id = f"session-{uuid.uuid4().hex[:8]}"
    up_id = f"session-{uuid.uuid4().hex[:8]}"
    down = await client.execute_workflow(
        AgentSessionWorkflow.run,
        args=[down_id, "bind@1:down", "hello"],
        id=down_id,
        task_queue=TASK_QUEUE,
    )
    up = await client.execute_workflow(
        AgentSessionWorkflow.run,
        args=[up_id, "bind@1", "hello"],
        id=up_id,
        task_queue=TASK_QUEUE,
    )
    print(f"down={down}|up={up}")


if __name__ == "__main__":
    asyncio.run(main())
