from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import call_tool


@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._fixed_id: str | None = None
        self._quarantined = False

    @workflow.query
    def status(self) -> str:
        return "quarantined" if self._quarantined and self._fixed_id is None else "ok"

    @workflow.signal
    def correct(self, item_id: str) -> None:
        self._fixed_id = item_id

    @workflow.run
    async def run(self, session_id: str, item_id: str) -> str:
        current = item_id
        while True:
            try:
                return await workflow.execute_activity(
                    call_tool,
                    args=["lookup", current],
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=RetryPolicy(maximum_attempts=1),
                )
            except ActivityError as err:
                if isinstance(err.cause, ApplicationError) and err.cause.type == "PoisonTool":
                    self._quarantined = True
                    await workflow.wait_condition(lambda: self._fixed_id is not None)
                    current = self._fixed_id or current
                    self._quarantined = False
                    continue
                raise
