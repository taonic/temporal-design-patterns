import { Client, Connection } from "@temporalio/client";

import { TASK_QUEUE, WORKFLOW_ID_PREFIX } from "./shared";
import { fulfillOrderWorkflow, stopSignal } from "./workflows";

async function main(): Promise<void> {
  const connection = await Connection.connect();
  try {
    const client = new Client({ connection });
    const workflowId = `${WORKFLOW_ID_PREFIX}-${Date.now()}`;
    const orderId = "order-42";

    const handle = await client.workflow.start(fulfillOrderWorkflow, {
      args: [orderId],
      taskQueue: TASK_QUEUE,
      workflowId,
    });
    console.log(`Started workflow: ${workflowId}`);
    console.log(`Fulfilling ${orderId}; children are reserving resources concurrently…`);

    // Let the children apply their steps, then request a stop.
    await new Promise((r) => setTimeout(r, 2000));
    console.log("Requesting stop; cancellation will propagate to every child…");
    await handle.signal(stopSignal);

    const result = await handle.result();
    console.log(result);
    console.log(
      `Open the Temporal UI and search for '${workflowId}' to see each child transition to Canceled after compensating.`
    );
  } finally {
    await connection.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
