from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self, session_id: str, turn_id: str, user_message: str) -> str:
        text = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"{turn_id}:{text}"


@workflow.defn
class AgentSessionWorkflow:
    """Turn Workflow: Session starts an isolated Turn child."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        turn_id = "turn-1"
        return await workflow.execute_child_workflow(
            AgentTurnWorkflow.run,
            args=[session_id, turn_id, user_message],
            id=f"{session_id}-{turn_id}",
        )
