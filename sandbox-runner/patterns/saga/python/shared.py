from dataclasses import dataclass

TASK_QUEUE = "saga-task-queue"
WORKFLOW_ID_PREFIX = "open-account"


@dataclass
class OpenAccountRequest:
    accountId: str
    clientName: str
    clientEmail: str
    address: str
    bankAccount: str
