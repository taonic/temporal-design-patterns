import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, Delivery


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        session_id,
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentSessionWorkflow.mark_turn_open)
    q1 = await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery("d1", "user-1", "hello"),
    )
    q2 = await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery("d2", "user-1", "world"),
    )
    await handle.signal(AgentSessionWorkflow.mark_turn_idle)
    await asyncio.sleep(0.4)
    await handle.signal(AgentSessionWorkflow.stop)
    result = await handle.result()
    print(f"q1={q1}|q2={q2}|result={result}")


if __name__ == "__main__":
    asyncio.run(main())
