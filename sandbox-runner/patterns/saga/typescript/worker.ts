import { Worker } from "@temporalio/worker";

import * as activities from "./activities";
import { TASK_QUEUE } from "./shared";

async function main(): Promise<void> {
  const worker = await Worker.create({
    workflowsPath: require.resolve("./workflows"),
    activities,
    taskQueue: TASK_QUEUE,
  });
  console.log(`Worker listening on task queue '${TASK_QUEUE}'`);
  await worker.run();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
