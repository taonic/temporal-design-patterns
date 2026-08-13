from dataclasses import dataclass
from temporalio import workflow

@dataclass
class Principal:
    principal_id: str
    principal_type: str

@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self.initiator: Principal | None = None
        self.current: Principal | None = None

    @workflow.run
    async def run(self, initiator: Principal, delivery_from: Principal) -> str:
        self.initiator = initiator
        self.current = delivery_from
        if self.current.principal_id != self.initiator.principal_id:
            return "rejected:not_owner"
        return f"ok:{self.current.principal_id}"
