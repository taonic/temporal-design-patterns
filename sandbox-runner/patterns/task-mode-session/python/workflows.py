from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.exceptions import ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import run_task


@dataclass
class TurnInput:
    mode: str
    user_message: str


@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._human_reply: str | None = None

    @workflow.signal
    def human_reply(self, text: str) -> None:
        self._human_reply = text

    @workflow.run
    async def run(self, inp: TurnInput) -> str:
        needs_clarification = "?" in inp.user_message
        if needs_clarification:
            if inp.mode == "task":
                raise ApplicationError(
                    "task_mode_cannot_wait",
                    type="TaskModeCannotWait",
                    non_retryable=True,
                )
            await workflow.wait_condition(lambda: self._human_reply is not None)
            return f"answered:{self._human_reply}"
        return await workflow.execute_activity(
            run_task,
            inp.user_message,
            start_to_close_timeout=timedelta(seconds=10),
        )
