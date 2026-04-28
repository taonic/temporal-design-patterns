import asyncio
import time

from temporalio.client import (
    Client,
    WithStartWorkflowOperation,
    WorkflowUpdateStage,
)
from temporalio.common import WorkflowIDConflictPolicy

from shared import TASK_QUEUE, WORKFLOW_ID_PREFIX, TransactionRequest
from workflows import TransactionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    transaction_id = f"{WORKFLOW_ID_PREFIX}-{int(time.time() * 1000)}"
    req = TransactionRequest(amount=100, currency="USD")

    start_op = WithStartWorkflowOperation(
        TransactionWorkflow.run,
        req,
        id=transaction_id,
        task_queue=TASK_QUEUE,
        id_conflict_policy=WorkflowIDConflictPolicy.FAIL,
    )

    t0 = time.monotonic()
    update_handle = await client.start_update_with_start_workflow(
        TransactionWorkflow.return_init_result,
        wait_for_stage=WorkflowUpdateStage.COMPLETED,
        start_workflow_operation=start_op,
    )
    tx = await update_handle.result()
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    print(f"Early return after {elapsed_ms}ms: {tx.id} (status={tx.status})")

    handle = client.get_workflow_handle(transaction_id)
    final = await handle.result()
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    print(f"Workflow completed after {elapsed_ms}ms: {final}")
    print(
        f"Open the Temporal UI and search for '{transaction_id}' to see the history."
    )


if __name__ == "__main__":
    asyncio.run(main())
