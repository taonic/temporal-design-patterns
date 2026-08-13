from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_sandboxed, run_unsandboxed

@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._decision: str | None = None

    @workflow.signal
    def escalation_response(self, decision: str) -> None:
        self._decision = decision

    @workflow.run
    async def run(self, command: str) -> str:
        result = await workflow.execute_activity(
            run_sandboxed, command, start_to_close_timeout=timedelta(seconds=30)
        )
        if result["ok"]:
            return result["output"]
        if not result["sandbox_denial"]:
            return f"tool_error:{result['output']}"
        await workflow.wait_condition(lambda: self._decision is not None)
        if self._decision != "granted":
            return f"escalation_denied:{result['output']}"
        return await workflow.execute_activity(
            run_unsandboxed, command, start_to_close_timeout=timedelta(seconds=30)
        )
