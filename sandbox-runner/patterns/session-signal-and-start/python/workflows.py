from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import reply_turn


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._messages: list[str] = []
        self._stop = False

    @workflow.signal
    def user_message(self, text: str) -> None:
        self._messages.append(text)

    @workflow.run
    async def run(self, session_id: str) -> str:
        await workflow.wait_condition(lambda: len(self._messages) > 0)
        text = self._messages.pop(0)
        return await workflow.execute_activity(
            reply_turn,
            text,
            start_to_close_timeout=timedelta(seconds=30),
        )
