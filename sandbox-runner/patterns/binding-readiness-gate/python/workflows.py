from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import call_model, check_binding_ready


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, binding_revision: str, user_message: str) -> str:
        try:
            await workflow.execute_activity(
                check_binding_ready,
                binding_revision,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )
        except ActivityError as err:
            if isinstance(err.cause, ApplicationError) and err.cause.type == "BindingNotReady":
                return "binding_not_ready"
            raise
        text = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return text
