import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow, SessionPins


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    pins = SessionPins(
        catalog_snapshot_id="cat@sha256:demo",
        definition_revision="def@1",
        binding_revision="bind@1",
    )
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, pins, "hello"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    q = await handle.query(AgentSessionWorkflow.pins)
    result = await handle.result()
    print(f"snap={q['catalog_snapshot_id']}|result={result}")


if __name__ == "__main__":
    asyncio.run(main())
