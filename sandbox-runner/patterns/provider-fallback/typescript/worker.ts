import { Worker } from "@temporalio/worker";

import { createActivities, LLMRegistry } from "./activities";
import { TASK_QUEUE } from "./shared";

async function main(): Promise<void> {
  // One registry shared by every Activity this worker runs. Injected here so the
  // implementations receive their state instead of reaching for module globals.
  // See the note in activities.ts on why this is safe only for same-worker,
  // per-Workflow-keyed state.
  const registry = new LLMRegistry();

  const worker = await Worker.create({
    workflowsPath: require.resolve("./workflows"),
    activities: createActivities(registry),
    taskQueue: TASK_QUEUE,
  });
  console.log(`Worker listening on task queue '${TASK_QUEUE}'`);
  await worker.run();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
