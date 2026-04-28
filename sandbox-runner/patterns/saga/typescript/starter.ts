import { Client, Connection } from "@temporalio/client";

import { TASK_QUEUE, WORKFLOW_ID_PREFIX, type TransferDetails } from "./shared";
import { transferMoneyWorkflow } from "./workflows";

async function main(): Promise<void> {
  const connection = await Connection.connect();
  try {
    const client = new Client({ connection });
    const transferId = `${WORKFLOW_ID_PREFIX}-${Date.now()}`;
    const details: TransferDetails = {
      transferId,
      fromAccount: "alice",
      toAccount: "bob",
      amount: 100,
    };

    const handle = await client.workflow.start(transferMoneyWorkflow, {
      args: [details],
      taskQueue: TASK_QUEUE,
      workflowId: transferId,
    });
    console.log(`Started workflow: ${transferId}`);

    const result = await handle.result();
    console.log(result);
    console.log(`Open the Temporal UI and search for '${transferId}' to see the saga history.`);
  } finally {
    await connection.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
