import {
  condition,
  defineUpdate,
  proxyActivities,
  proxyLocalActivities,
  setHandler,
} from "@temporalio/workflow";

import type * as activities from "./activities";
import type { Transaction, TransactionRequest } from "./shared";

const { initTransaction } = proxyLocalActivities<typeof activities>({
  scheduleToCloseTimeout: "5 seconds",
});

const { completeTransaction, cancelTransaction } = proxyActivities<typeof activities>({
  startToCloseTimeout: "30 seconds",
});

export const returnInitResultUpdate = defineUpdate<Transaction>("returnInitResult");

export async function transactionWorkflow(
  req: TransactionRequest,
): Promise<Transaction | null> {
  let tx: Transaction | undefined;
  let initDone = false;
  let initError: Error | undefined;

  setHandler(returnInitResultUpdate, async () => {
    await condition(() => initDone);
    if (initError) {
      throw initError;
    }
    return tx!;
  });

  // Phase 1: fast synchronous initialization (local activity).
  try {
    tx = await initTransaction(req);
  } catch (err) {
    initError = err as Error;
  } finally {
    initDone = true;
  }

  // Phase 2: slow asynchronous completion.
  if (initError) {
    await cancelTransaction(tx);
    return null;
  }

  await completeTransaction(tx!);
  return tx!;
}
