import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import SpecialistSession, SummarizeRequest


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        SpecialistSession.run,
        args=[session_id],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    ops = await handle.query(SpecialistSession.list_operations)
    resp = await handle.execute_update(
        SpecialistSession.summarize,
        SummarizeRequest(text="durable agent patterns", max_tokens=16),
    )
    await handle.signal(SpecialistSession.stop)
    await handle.result()
    print(f"ops={ops[0]['name']}|summary={resp.summary}|ver={resp.prompt_version}")


if __name__ == "__main__":
    asyncio.run(main())
