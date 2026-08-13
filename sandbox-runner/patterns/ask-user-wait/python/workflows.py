from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import model_step


@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._answer: str | None = None
        self._prompt: str = ""

    @workflow.query
    def pending_question(self) -> str:
        return self._prompt

    @workflow.update
    async def answer(self, text: str) -> str:
        if not text.strip():
            raise ValueError("answer required")
        self._answer = text
        return "accepted"

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        step = await workflow.execute_activity(
            model_step,
            args=["ask", ""],
            start_to_close_timeout=timedelta(seconds=30),
        )
        self._prompt = step["prompt"]
        await workflow.wait_condition(lambda: self._answer is not None)
        final = await workflow.execute_activity(
            model_step,
            args=["final", self._answer or ""],
            start_to_close_timeout=timedelta(seconds=30),
        )
        return final["text"]
