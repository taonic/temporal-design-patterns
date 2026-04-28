import type { OpenAccountRequest } from "./shared";

export async function createAccount(req: OpenAccountRequest): Promise<void> {
  console.log(`Created account ${req.accountId} for ${req.clientName}`);
}

export async function addAddress(req: OpenAccountRequest): Promise<void> {
  console.log(`Added address '${req.address}' to ${req.accountId}`);
}

export async function addClient(req: OpenAccountRequest): Promise<void> {
  console.log(`Added client ${req.clientEmail} to ${req.accountId}`);
}

export async function addBankAccount(req: OpenAccountRequest): Promise<void> {
  console.log(`Linking bank account ${req.bankAccount}: simulating downstream failure`);
  // Comment out the throw to watch the saga succeed end-to-end:
  throw new Error("bank link service down");
}

export async function clearPostalAddresses(req: OpenAccountRequest): Promise<void> {
  console.log(`Cleared postal addresses for ${req.accountId}`);
}

export async function removeClient(req: OpenAccountRequest): Promise<void> {
  console.log(`Removed client from ${req.accountId}`);
}

export async function disconnectBankAccounts(req: OpenAccountRequest): Promise<void> {
  console.log(`Disconnected any bank accounts from ${req.accountId}`);
}
