import asyncio
import uuid

from temporalio.client import Client
from temporalio.client import WorkflowUpdateFailedError

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, Delivery


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    rejected = "ok"
    try:
        await handle.execute_update(
            AgentSessionWorkflow.deliver,
            Delivery(delivery_id="d1", text="   "),
        )
        rejected = "not_rejected"
    except WorkflowUpdateFailedError:
        rejected = "rejected"
    ack = await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery(delivery_id="d2", text="hello"),
    )
    dup = await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery(delivery_id="d2", text="hello"),
    )
    await handle.signal(AgentSessionWorkflow.stop)
    result = await handle.result()
    print(f"rejected={rejected}|ack={ack}|dup={dup}|result={result}")


if __name__ == "__main__":
    asyncio.run(main())
