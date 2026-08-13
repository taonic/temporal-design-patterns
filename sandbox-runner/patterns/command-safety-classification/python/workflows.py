from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import classify_command, exec_command

@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._decision: str | None = None

    @workflow.signal
    def approve(self, decision: str) -> None:
        self._decision = decision

    @workflow.run
    async def run(self, command: str) -> str:
        c = await workflow.execute_activity(
            classify_command, command, start_to_close_timeout=timedelta(seconds=10)
        )
        if c["requirement"] == "forbid":
            return f"forbidden:{c['reason']}"
        if c["requirement"] == "need_approval":
            await workflow.wait_condition(lambda: self._decision is not None)
            if self._decision != "granted":
                return "approval_denied"
        return await workflow.execute_activity(
            exec_command, command, start_to_close_timeout=timedelta(seconds=30)
        )
