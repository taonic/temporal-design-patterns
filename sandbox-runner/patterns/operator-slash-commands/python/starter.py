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
        args=[session_id, "hi"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentSessionWorkflow.slash, "/approvals safe")
    result = await handle.result()
    print(result)
    print(await handle.query(AgentSessionWorkflow.status))


if __name__ == "__main__":
    asyncio.run(main())
