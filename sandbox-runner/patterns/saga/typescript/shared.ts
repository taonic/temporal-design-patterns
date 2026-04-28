export const TASK_QUEUE = "saga-task-queue";
export const WORKFLOW_ID_PREFIX = "transfer";

export interface TransferDetails {
  transferId: string;
  fromAccount: string;
  toAccount: string;
  amount: number;
}
