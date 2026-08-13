from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import first_step


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._text = ""

    @workflow.signal
    def user_message(self, text: str) -> None:
        self._text = text

    @workflow.run
    async def run(self, session_id: str) -> str:
        await workflow.wait_condition(lambda: bool(self._text))
        return await workflow.execute_activity(
            first_step,
            self._text,
            start_to_close_timeout=timedelta(seconds=10),
        )
