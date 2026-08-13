from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import call_model, run_tool


@workflow.defn
class AgentSessionWorkflow:
    """Session Workflow: one durable Workflow owns turns for a session_id."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        events: list[str] = [f"session_started:{session_id}", "turn_started"]
        reply = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        events.append("model_call_completed")
        tool_result = await workflow.execute_activity(
            run_tool,
            args=["echo", reply],
            start_to_close_timeout=timedelta(seconds=30),
        )
        events.append(f"tool_call_completed:{tool_result}")
        events.append("turn_ended")
        events.append("session_ended")
        return " | ".join(events)
