import asyncio
import json
import uuid

from temporalio.client import Client

from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    result = await client.execute_workflow(
        AgentSessionWorkflow.run,
        args=[
            session_id,
            {"transcript": ["t1", "t2", "t3", "t4"]},
            {
                "todos": ["ship"],
                "approved_tools": ["deploy"],
                "read_files": {"a.py": True},
            },
        ],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    print(
        f"todos={result['todos']}|approved={result['approved_tools']}|"
        f"reads={result['read_files']}|transcript={result['memory']['transcript']}"
    )


if __name__ == "__main__":
    asyncio.run(main())
