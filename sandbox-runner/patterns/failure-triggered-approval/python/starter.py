import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    # ordinary success
    ok = await client.execute_workflow(
        AgentTurnWorkflow.run, "echo hi",
        id=f"fta-ok-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    # ordinary failure (no escalation)
    err = await client.execute_workflow(
        AgentTurnWorkflow.run, "boom",
        id=f"fta-err-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    # sandbox denial -> escalate -> grant
    wid = f"fta-esc-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentTurnWorkflow.run, "write /etc/hosts",
        id=wid, task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentTurnWorkflow.escalation_response, "granted")
    esc = await handle.result()
    print(f"ok={ok}|err={err}|esc={esc}")

if __name__ == "__main__":
    asyncio.run(main())
