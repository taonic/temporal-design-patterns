import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import transfer_funds


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self.decision: str | None = None
        self.deadline: float = 0.0
        self._deadline_updated = False

    @workflow.signal
    def approve(self, decision: str) -> None:
        self.decision = decision

    @workflow.signal
    def extend_deadline(self, extra_seconds: float) -> None:
        self.deadline = workflow.time() + extra_seconds
        self._deadline_updated = True

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        self.deadline = workflow.time() + 2.0  # short demo SLA
        while self.decision is None:
            self._deadline_updated = False
            remaining = self.deadline - workflow.time()
            try:
                await workflow.wait_condition(
                    lambda: self.decision is not None or self._deadline_updated,
                    timeout=timedelta(seconds=max(remaining, 0)),
                )
            except asyncio.TimeoutError:
                return "approval_timeout"
        if self.decision != "granted":
            return "approval_denied"
        result = await workflow.execute_activity(
            transfer_funds,
            50,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"approval_granted:{result}"
