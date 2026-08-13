from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_structured_model


@workflow.defn
class AgentSessionWorkflow:
    """Structured Model Output: Activity returns schema-shaped fields."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        data = await workflow.execute_activity(
            call_structured_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"intent={data['intent']}|query={data['query']}|limit={data['limit']}"
