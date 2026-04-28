export const TASK_QUEUE = "saga-task-queue";
export const WORKFLOW_ID_PREFIX = "open-account";

export interface OpenAccountRequest {
  accountId: string;
  clientName: string;
  clientEmail: string;
  address: string;
  bankAccount: string;
}
