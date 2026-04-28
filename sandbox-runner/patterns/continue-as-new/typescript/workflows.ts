import { continueAsNew, log, proxyActivities } from "@temporalio/workflow";

import type * as activities from "./activities";
import { BATCH_SIZE } from "./shared";

const { fetchBatch, processRecord } = proxyActivities<typeof activities>({
  startToCloseTimeout: "10 seconds",
});

export async function dataProcessorWorkflow(
  cursor: string = "",
  totalProcessed: number = 0,
): Promise<number> {
  const batch = await fetchBatch(cursor, BATCH_SIZE);

  for (const record of batch) {
    await processRecord(record);
    totalProcessed++;
    cursor = record.id;
  }

  log.info(`Processed batch of ${batch.length} (running total: ${totalProcessed})`);

  if (batch.length === BATCH_SIZE) {
    await continueAsNew<typeof dataProcessorWorkflow>(cursor, totalProcessed);
  }

  return totalProcessed;
}
