from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


def validate_total(cents: int) -> str:
    """Workflow Tool: pure, deterministic, no Activity boundary."""
    if cents < 0:
        raise ValueError("negative total")
    return f"valid:{cents}"


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return validate_total(42)
