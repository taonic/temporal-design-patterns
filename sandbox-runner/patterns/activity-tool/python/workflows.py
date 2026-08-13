from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model, charge_card


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        decision = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        # Activity Tool: durable, retried, observable step boundary.
        result = await workflow.execute_activity(
            charge_card,
            args=[500, f"{session_id}-charge-1"],
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"{decision} -> {result}"
