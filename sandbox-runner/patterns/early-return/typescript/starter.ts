import { Client, Connection, WithStartWorkflowOperation } from "@temporalio/client";

import { TASK_QUEUE, WORKFLOW_ID_PREFIX, type TransactionRequest } from "./shared";
import { returnInitResultUpdate, transactionWorkflow } from "./workflows";

async function main(): Promise<void> {
  const connection = await Connection.connect();
  try {
    const client = new Client({ connection });
    const transactionId = `${WORKFLOW_ID_PREFIX}-${Date.now()}`;
    const req: TransactionRequest = { amount: 100, currency: "USD" };

    const startOp = new WithStartWorkflowOperation(transactionWorkflow, {
      workflowId: transactionId,
      args: [req],
      taskQueue: TASK_QUEUE,
      workflowIdConflictPolicy: "FAIL",
    });

    const t0 = Date.now();
    const tx = await client.workflow.executeUpdateWithStart(returnInitResultUpdate, {
      startWorkflowOperation: startOp,
    });
    console.log(
      `Early return after ${Date.now() - t0}ms: ${tx.id} (status=${tx.status})`,
    );

    const handle = await startOp.workflowHandle();
    const final = await handle.result();
    console.log(`Workflow completed after ${Date.now() - t0}ms: ${JSON.stringify(final)}`);
    console.log(
      `Open the Temporal UI and search for '${transactionId}' to see the history.`,
    );
  } finally {
    await connection.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
