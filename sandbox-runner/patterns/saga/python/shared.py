from dataclasses import dataclass

TASK_QUEUE = "saga-task-queue"
WORKFLOW_ID_PREFIX = "transfer"


@dataclass
class TransferDetails:
    transferId: str
    fromAccount: str
    toAccount: str
    amount: int
