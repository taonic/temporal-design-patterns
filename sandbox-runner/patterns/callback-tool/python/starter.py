import asyncio
import uuid

from temporalio.client import Client

from workflows import AgentSessionWorkflow

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "read local file"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    # Simulates the attached client completing the callback tool.
    await handle.signal(AgentSessionWorkflow.callback_completed, "file://notes.md")
    result = await handle.result()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
