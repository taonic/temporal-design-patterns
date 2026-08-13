from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import flaky_tool


@workflow.defn
class AgentSessionWorkflow:
    """Fast/Slow Tool Retries: short bounded phase, then patient phase."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        fast = RetryPolicy(
            initial_interval=timedelta(milliseconds=50),
            backoff_coefficient=1.0,
            maximum_interval=timedelta(milliseconds=50),
            maximum_attempts=2,
        )
        slow = RetryPolicy(
            initial_interval=timedelta(milliseconds=50),
            backoff_coefficient=1.0,
            maximum_interval=timedelta(milliseconds=50),
            maximum_attempts=5,
        )
        try:
            return await workflow.execute_activity(
                flaky_tool,
                user_message,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=fast,
            )
        except ActivityError:
            result = await workflow.execute_activity(
                flaky_tool,
                user_message,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=slow,
            )
            return f"slow_phase:{result}"
