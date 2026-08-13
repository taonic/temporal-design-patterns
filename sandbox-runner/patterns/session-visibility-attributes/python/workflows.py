from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import noop
    from shared import TENANT_ID, TURN_STATUS


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._status = "idle"
        self._approve = False

    @workflow.query
    def turn_status(self) -> str:
        return self._status

    @workflow.signal
    def approve(self) -> None:
        self._approve = True

    @workflow.run
    async def run(self, session_id: str, tenant_id: str) -> str:
        self._status = "running"
        workflow.upsert_search_attributes(
            [
                TURN_STATUS.value_set(self._status),
                TENANT_ID.value_set(tenant_id),
            ]
        )
        await workflow.execute_activity(
            noop,
            start_to_close_timeout=timedelta(seconds=10),
        )
        self._status = "awaiting_approval"
        workflow.upsert_search_attributes([TURN_STATUS.value_set(self._status)])
        await workflow.wait_condition(lambda: self._approve)
        self._status = "idle"
        workflow.upsert_search_attributes([TURN_STATUS.value_set(self._status)])
        return self._status
