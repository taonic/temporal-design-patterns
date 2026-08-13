from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import long_model_step


@workflow.defn
class AgentSessionWorkflow:
    """Heartbeat Long Steps: heartbeat_timeout + progress details."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        return await workflow.execute_activity(
            long_model_step,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
            heartbeat_timeout=timedelta(seconds=10),
        )
