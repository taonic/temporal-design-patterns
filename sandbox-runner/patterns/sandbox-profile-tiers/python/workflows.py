from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import exec_in_sandbox

@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self, command: str, mode: str) -> str:
        return await workflow.execute_activity(
            exec_in_sandbox, args=[command, mode],
            start_to_close_timeout=timedelta(seconds=30),
        )
