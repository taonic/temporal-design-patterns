from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model, sanitize_user_text


@workflow.defn
class AgentSessionWorkflow:
    """Local Activity Tools: tiny helper local, model call regular."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        cleaned = await workflow.execute_local_activity(
            sanitize_user_text,
            user_message,
            start_to_close_timeout=timedelta(seconds=5),
        )
        return await workflow.execute_activity(
            call_model,
            cleaned,
            start_to_close_timeout=timedelta(seconds=30),
        )
