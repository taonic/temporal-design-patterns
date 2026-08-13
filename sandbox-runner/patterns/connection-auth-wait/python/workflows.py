from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import call_connected_tool


@dataclass
class AuthCompleted:
    connection_id: str
    status: str


@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._auth_done: AuthCompleted | None = None

    @workflow.signal
    def connection_auth_completed(self, msg: AuthCompleted) -> None:
        self._auth_done = msg

    @workflow.run
    async def run(self, session_id: str, connection_id: str) -> str:
        try:
            return await workflow.execute_activity(
                call_connected_tool,
                connection_id,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )
        except ActivityError as err:
            if not (
                isinstance(err.cause, ApplicationError) and err.cause.type == "NeedsAuth"
            ):
                raise
        await workflow.wait_condition(lambda: self._auth_done is not None)
        if not self._auth_done or self._auth_done.status != "granted":
            return "auth_denied"
        return await workflow.execute_activity(
            call_connected_tool,
            connection_id,
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(maximum_attempts=1),
        )
