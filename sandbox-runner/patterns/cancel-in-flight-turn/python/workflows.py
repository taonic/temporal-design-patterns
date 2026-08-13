from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import CancelledError, ChildWorkflowError

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self, session_id: str, turn_id: str, user_message: str) -> str:
        return await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=60),
            heartbeat_timeout=timedelta(seconds=2),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._turn_handle = None

    @workflow.signal
    def cancel_turn(self, reason: str) -> None:
        if self._turn_handle is not None:
            self._turn_handle.cancel()

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        self._turn_handle = await workflow.start_child_workflow(
            AgentTurnWorkflow.run,
            args=[session_id, "turn-1", user_message],
            id=f"{session_id}-turn-1",
        )
        try:
            return await self._turn_handle
        except ChildWorkflowError as err:
            if isinstance(err.cause, CancelledError):
                return "turn_cancelled"
            raise
        except CancelledError:
            return "turn_cancelled"
