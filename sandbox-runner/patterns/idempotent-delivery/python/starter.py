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
    )
    delivery_id = f"del-{uuid.uuid4().hex[:8]}"
    first = await handle.execute_update(
        AgentSessionWorkflow.deliver, args=[delivery_id, "hello"]
    )
    second = await handle.execute_update(
        AgentSessionWorkflow.deliver, args=[delivery_id, "hello"]
    )
    await handle.signal(AgentSessionWorkflow.stop)
    result = await handle.result()
    print(
        f"first={first.status}|second={second.status}|turns={result}|same_turn={first.turn_id == second.turn_id}"
    )


if __name__ == "__main__":
    asyncio.run(main())
