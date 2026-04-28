from dataclasses import dataclass

TASK_QUEUE = "early-return-task-queue"
WORKFLOW_ID_PREFIX = "transaction"


@dataclass
class TransactionRequest:
    amount: float
    currency: str


@dataclass
class Transaction:
    id: str
    status: str
