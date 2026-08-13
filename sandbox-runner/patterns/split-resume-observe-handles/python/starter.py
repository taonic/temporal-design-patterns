import asyncio
import uuid

from temporalio.client import Client
from temporalio.client import WorkflowUpdateFailedError

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, Caps, Delivery


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    caps = Caps(resume_token=f"res_{uuid.uuid4().hex}", observe_token=f"obs_{uuid.uuid4().hex}")
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, caps],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    obs_ok = await handle.query(AgentSessionWorkflow.observe, caps.observe_token)
    obs_bad = await handle.query(AgentSessionWorkflow.observe, "wrong")
    rejected = "ok"
    try:
        await handle.execute_update(
            AgentSessionWorkflow.deliver,
            Delivery(resume_token="wrong", delivery_id="d0", text="nope"),
        )
        rejected = "not_rejected"
    except WorkflowUpdateFailedError:
        rejected = "rejected"
    await handle.execute_update(
        AgentSessionWorkflow.deliver,
        Delivery(resume_token=caps.resume_token, delivery_id="d1", text="hello"),
    )
    await handle.signal(AgentSessionWorkflow.stop)
    result = await handle.result()
    print(
        f"obs_ok={obs_ok['ok']}|obs_bad={obs_bad['ok']}|write={rejected}|result={result}"
    )


if __name__ == "__main__":
    asyncio.run(main())
