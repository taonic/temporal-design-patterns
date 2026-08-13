from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import call_model, guardrail_check


@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        try:
            await workflow.execute_activity(
                guardrail_check,
                args=["pre_model", user_message],
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )
        except ActivityError as err:
            if isinstance(err.cause, ApplicationError) and err.cause.type == "GuardrailBlocked":
                return "guardrail_blocked"
            raise
        reply = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
        await workflow.execute_activity(
            guardrail_check,
            args=["post_model", reply],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
        return reply
