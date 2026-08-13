from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import answer_turn, generate_suggestions

@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, user_message: str, enable_suggestions: bool) -> dict:
        reply = await workflow.execute_activity(
            answer_turn, user_message, start_to_close_timeout=timedelta(seconds=30)
        )
        suggestions: list[str] = []
        if enable_suggestions:
            suggestions = await workflow.execute_activity(
                generate_suggestions,
                args=[user_message, reply],
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )
        return {"reply": reply, "suggestions": suggestions}
