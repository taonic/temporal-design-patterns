import type { Transaction, TransactionRequest } from "./shared";

export async function initTransaction(req: TransactionRequest): Promise<Transaction> {
  console.log(`Init: validating ${req.amount} ${req.currency}`);
  if (req.amount <= 0) {
    throw new Error(`Invalid amount: ${req.amount}`);
  }
  return { id: `tx-${Date.now()}`, status: "initialized" };
}

export async function completeTransaction(tx: Transaction): Promise<void> {
  // Simulate slow background settlement so the early-return effect is visible.
  await new Promise((resolve) => setTimeout(resolve, 2000));
  console.log(`Completed transaction ${tx.id}`);
}

export async function cancelTransaction(tx: Transaction | undefined): Promise<void> {
  console.log(`Cancelled transaction ${tx?.id ?? "(uninitialized)"}`);
}
