from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        first = await workflow.execute_activity(
            call_model,
            args=["summarizer", "v1", user_message],
            start_to_close_timeout=timedelta(seconds=10),
        )
        second = await workflow.execute_activity(
            call_model,
            args=["summarizer", "v1", user_message],
            start_to_close_timeout=timedelta(seconds=10),
        )
        return f"first_cached={first['cached']}|second_cached={second['cached']}|text={second['text']}"
