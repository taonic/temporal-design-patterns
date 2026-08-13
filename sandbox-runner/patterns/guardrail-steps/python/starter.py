import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    blocked_id = f"session-{uuid.uuid4().hex[:8]}"
    allowed_id = f"session-{uuid.uuid4().hex[:8]}"
    blocked = await client.execute_workflow(
        AgentTurnWorkflow.run,
        args=[blocked_id, "hello FORBIDDEN"],
        id=blocked_id,
        task_queue=TASK_QUEUE,
    )
    allowed = await client.execute_workflow(
        AgentTurnWorkflow.run,
        args=[allowed_id, "hello"],
        id=allowed_id,
        task_queue=TASK_QUEUE,
    )
    print(f"blocked={blocked}|allowed={allowed}")


if __name__ == "__main__":
    asyncio.run(main())
