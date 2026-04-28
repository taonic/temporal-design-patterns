import { log, proxyActivities } from "@temporalio/workflow";

import type * as activities from "./activities";
import type { TransferDetails } from "./shared";

const acts = proxyActivities<typeof activities>({
  startToCloseTimeout: "10 seconds",
  retry: { maximumAttempts: 1 },
});

type Compensation = () => Promise<void>;

export async function transferMoneyWorkflow(details: TransferDetails): Promise<string> {
  const compensations: Compensation[] = [];

  try {
    log.info(`Starting transfer ${details.transferId}: $${details.amount}`);

    compensations.unshift(() => acts.withdrawCompensation(details));
    await acts.withdraw(details);

    compensations.unshift(() => acts.depositCompensation(details));
    await acts.deposit(details);

    await acts.notifyDownstream(details);

    return `Transfer ${details.transferId} completed`;
  } catch (err) {
    const reason = (err as Error).message;
    log.warn(
      `Transfer ${details.transferId} failed (${reason}); running ${compensations.length} compensation(s)`,
    );
    for (const compensate of compensations) {
      try {
        await compensate();
      } catch (compErr) {
        log.error(`Compensation failed: ${(compErr as Error).message}`);
      }
    }
    // Return a status instead of re-throwing so the workflow execution itself
    // succeeds. Re-throwing is the canonical pattern (see saga-pattern.md
    // best practices); this demo prefers a clean ✅ in the Temporal UI and
    // surfaces the rollback via the result string.
    return `Transfer ${details.transferId} rolled back: ${reason}`;
  }
}
