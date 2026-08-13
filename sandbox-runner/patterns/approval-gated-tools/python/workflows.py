from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import transfer_funds


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._approved = False
        self._decision = ""

    @workflow.signal
    def approve(self, decision: str) -> None:
        self._decision = decision
        self._approved = decision == "granted"

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        # Emit approval_requested semantics by waiting for a Signal.
        await workflow.wait_condition(lambda: self._approved or self._decision == "denied")
        if self._decision == "denied":
            return "approval_denied"
        result = await workflow.execute_activity(
            transfer_funds,
            100,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"approval_granted:{result}"
