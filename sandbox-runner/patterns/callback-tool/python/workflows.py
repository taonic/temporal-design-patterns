from temporalio import workflow


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._callback_result: str | None = None

    @workflow.signal
    def callback_completed(self, result: str) -> None:
        self._callback_result = result

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        # callback_requested: park until the client posts a result.
        await workflow.wait_condition(lambda: self._callback_result is not None)
        return f"callback_completed:{self._callback_result}"
