import { Client, Connection } from "@temporalio/client";

import { TASK_QUEUE, WORKFLOW_ID_PREFIX, type OpenAccountRequest } from "./shared";
import { openAccount } from "./workflows";

async function main(): Promise<void> {
  const connection = await Connection.connect();
  try {
    const client = new Client({ connection });
    const accountId = `${WORKFLOW_ID_PREFIX}-${Date.now()}`;
    const request: OpenAccountRequest = {
      accountId,
      clientName: "Alice Example",
      clientEmail: "alice@example.com",
      address: "123 Main St, Brooklyn NY",
      bankAccount: "DE89-3704-0044-0532-0130-00",
    };

    const handle = await client.workflow.start(openAccount, {
      args: [request],
      taskQueue: TASK_QUEUE,
      workflowId: accountId,
    });
    console.log(`Started workflow: ${accountId}`);

    const result = await handle.result();
    console.log(result);
    console.log(`Open the Temporal UI and search for '${accountId}' to see the saga history.`);
  } finally {
    await connection.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
