import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE, store_secret
from workflows import AgentTurnWorkflow, AuthCompleted


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    connection_id = f"conn-{uuid.uuid4().hex[:6]}"
    handle = await client.start_workflow(
        AgentTurnWorkflow.run,
        args=[session_id, connection_id],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await asyncio.sleep(0.3)
    # channel stores secret outside history, then signals ids-only resume
    store_secret(connection_id, "tok_demo")
    await handle.signal(
        AgentTurnWorkflow.connection_auth_completed,
        AuthCompleted(connection_id=connection_id, status="granted"),
    )
    print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
