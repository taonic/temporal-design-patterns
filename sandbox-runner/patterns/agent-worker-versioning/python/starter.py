import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE, WORKER_BUILD_ID
from workflows import AgentSessionWorkflow, SessionPins


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    pins = SessionPins(
        worker_build_id=WORKER_BUILD_ID,
        definition_revision="agent@sha256:demo",
        binding_revision="bind@2026-08-13.3",
    )
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, pins, "hello"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    q = await handle.query(AgentSessionWorkflow.pins)
    result = await handle.result()
    print(
        f"pins={q['worker_build_id']}|{q['definition_revision']}|{q['binding_revision']}|result={result}"
    )


if __name__ == "__main__":
    asyncio.run(main())
