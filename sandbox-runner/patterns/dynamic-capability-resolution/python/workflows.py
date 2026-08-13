from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model, resolve_capabilities


@workflow.defn
class AgentSessionWorkflow:
    @workflow.query
    def capabilities(self) -> dict:
        return self._resolved

    @workflow.run
    async def run(self, session_id: str, principal: dict, user_message: str) -> str:
        self._resolved = await workflow.execute_activity(
            resolve_capabilities,
            principal,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return await workflow.execute_activity(
            call_model,
            args=[
                self._resolved["catalog_snapshot_id"],
                self._resolved["tool_names"],
                user_message,
            ],
            start_to_close_timeout=timedelta(seconds=10),
        )
