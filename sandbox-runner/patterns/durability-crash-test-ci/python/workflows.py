from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import fake_model

@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, prompt: str) -> str:
        return await workflow.execute_activity(
            fake_model, prompt, start_to_close_timeout=timedelta(seconds=10)
        )
