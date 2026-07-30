import { Client, Connection } from "@temporalio/client";

import { TASK_QUEUE, WORKFLOW_ID_PREFIX } from "./shared";
import { providerFallbackWorkflow } from "./workflows";

async function main(): Promise<void> {
  const connection = await Connection.connect();
  try {
    const client = new Client({ connection });
    const workflowId = `${WORKFLOW_ID_PREFIX}-${Date.now()}`;
    // Change to "" (empty) to exercise the abort (invalid request) path.
    const question = "What is the meaning of durable execution?";

    const handle = await client.workflow.start(providerFallbackWorkflow, {
      args: [question],
      taskQueue: TASK_QUEUE,
      workflowId,
    });
    console.log(`Started workflow: ${workflowId}`);

    const result = await handle.result();
    console.log(result);
    console.log(`Open the Temporal UI and search for '${workflowId}' to see the agent loop and provider sweep.`);
  } finally {
    await connection.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
