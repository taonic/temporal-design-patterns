import asyncio
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:7]}0"  # force variant A
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "hello"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    pin = await handle.query(AgentSessionWorkflow.experiment)
    result = await handle.result()
    print(f"variant={pin['variant']}|prompt={pin['prompt_version']}|result={result}")


if __name__ == "__main__":
    asyncio.run(main())
