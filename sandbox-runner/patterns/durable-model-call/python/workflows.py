from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@workflow.defn
class AgentSessionWorkflow:
    """Durable Model Call: one Activity-backed model invocation returns the reply."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        result = await workflow.execute_activity(
            call_model,
            args=[user_message, "stub-model"],
            start_to_close_timeout=timedelta(seconds=30),
        )
        usage = result["usage"]
        return (
            f"{result['text']} | "
            f"tokens={usage['input_tokens']}+{usage['output_tokens']} "
            f"model={usage['model']}"
        )
