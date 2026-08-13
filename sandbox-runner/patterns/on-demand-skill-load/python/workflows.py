from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model_with_context, load_skill_body


@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self, session_id: str, catalog_snapshot_id: str, user_message: str) -> str:
        body = await workflow.execute_activity(
            load_skill_body,
            args=[catalog_snapshot_id, "deploy"],
            start_to_close_timeout=timedelta(seconds=10),
        )
        return await workflow.execute_activity(
            call_model_with_context,
            args=[user_message, body],
            start_to_close_timeout=timedelta(seconds=10),
        )
