import asyncio, uuid
from temporalio.client import Client
from temporalio.worker import Replayer
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    wid = f"crash-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run, "ping",
        id=wid, task_queue=TASK_QUEUE,
    )
    result = await handle.result()
    history = await handle.fetch_history()
    await Replayer(workflows=[AgentSessionWorkflow]).replay_workflow(history)
    print(f"result={result}|replay=ok")

if __name__ == "__main__":
    asyncio.run(main())
