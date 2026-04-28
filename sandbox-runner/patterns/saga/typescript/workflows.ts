import { log, proxyActivities } from "@temporalio/workflow";

import type * as activities from "./activities";
import type { OpenAccountRequest } from "./shared";

const acts = proxyActivities<typeof activities>({
  startToCloseTimeout: "10 seconds",
  retry: { maximumAttempts: 1 },
});

type Compensation = () => Promise<void>;

export async function openAccount(req: OpenAccountRequest): Promise<string> {
  const compensations: Compensation[] = [];

  try {
    log.info(`Opening account ${req.accountId} for ${req.clientName}`);

    // Step 1: createAccount has no compensation registered — leaving an empty
    // account stub on later failure is acceptable for this demo.
    await acts.createAccount(req);

    compensations.unshift(() => acts.clearPostalAddresses(req));
    await acts.addAddress(req);

    compensations.unshift(() => acts.removeClient(req));
    await acts.addClient(req);

    compensations.unshift(() => acts.disconnectBankAccounts(req));
    await acts.addBankAccount(req);

    return `Account ${req.accountId} opened`;
  } catch (err) {
    const reason = (err as Error).message;
    log.warn(
      `Account ${req.accountId} failed (${reason}); running ${compensations.length} compensation(s)`,
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
    return `Account ${req.accountId} rolled back: ${reason}`;
  }
}
