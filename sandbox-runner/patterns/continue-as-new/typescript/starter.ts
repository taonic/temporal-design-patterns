import { Client, Connection } from "@temporalio/client";

import { TASK_QUEUE, WORKFLOW_ID_PREFIX } from "./shared";
import { dataProcessorWorkflow } from "./workflows";

async function main(): Promise<void> {
  const connection = await Connection.connect();
  try {
    const client = new Client({ connection });
    const workflowId = `${WORKFLOW_ID_PREFIX}-${Date.now()}`;
    const handle = await client.workflow.start(dataProcessorWorkflow, {
      args: ["", 0],
      taskQueue: TASK_QUEUE,
      workflowId,
    });
    console.log(`Started workflow: ${workflowId}`);

    const total = await handle.result();
    console.log(`Final result: processed ${total} records`);
    console.log(`Open the Temporal UI and search for '${workflowId}' to see the Continue-As-New chain.`);
  } finally {
    await connection.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
