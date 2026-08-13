import asyncio
import uuid

from temporalio.client import Client, WorkflowFailureError

from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow, TurnInput


async def main() -> None:
    client = await Client.connect("localhost:7233")
    ok_id = f"task-ok-{uuid.uuid4().hex[:8]}"
    ok = await client.execute_workflow(
        AgentTurnWorkflow.run,
        TurnInput(mode="task", user_message="ship it"),
        id=ok_id,
        task_queue=TASK_QUEUE,
    )
    bad_id = f"task-bad-{uuid.uuid4().hex[:8]}"
    failed = "ok"
    try:
        await client.execute_workflow(
            AgentTurnWorkflow.run,
            TurnInput(mode="task", user_message="what next?"),
            id=bad_id,
            task_queue=TASK_QUEUE,
        )
        failed = "not_failed"
    except WorkflowFailureError:
        failed = "task_mode_cannot_wait"
    print(f"ok={ok}|clarification={failed}")


if __name__ == "__main__":
    asyncio.run(main())
