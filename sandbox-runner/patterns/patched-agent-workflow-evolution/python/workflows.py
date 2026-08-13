from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model, guardrail_check


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        steps: list[str] = []
        if workflow.patched("guardrail-pre-model-v1"):
            g = await workflow.execute_activity(
                guardrail_check,
                args=["pre_model", user_message],
                start_to_close_timeout=timedelta(seconds=10),
            )
            steps.append(g)
        text = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=10),
        )
        steps.append(text)
        return "|".join(steps)
