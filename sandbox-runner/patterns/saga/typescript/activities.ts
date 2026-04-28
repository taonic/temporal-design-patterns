import type { TransferDetails } from "./shared";

export async function withdraw(details: TransferDetails): Promise<void> {
  console.log(`Withdrew $${details.amount} from ${details.fromAccount}`);
}

export async function deposit(details: TransferDetails): Promise<void> {
  console.log(`Deposited $${details.amount} to ${details.toAccount}`);
}

export async function notifyDownstream(details: TransferDetails): Promise<void> {
  console.log(`Notify: simulating downstream failure for transfer ${details.transferId}`);
  // Comment out the throw to watch the saga succeed end-to-end:
  throw new Error("notification service down");
}

export async function withdrawCompensation(details: TransferDetails): Promise<void> {
  console.log(`Refunded $${details.amount} to ${details.fromAccount}`);
}

export async function depositCompensation(details: TransferDetails): Promise<void> {
  console.log(`Reversed deposit of $${details.amount} from ${details.toAccount}`);
}
