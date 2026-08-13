import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._pending: str | None = None

    @workflow.signal
    def user_message(self, text: str) -> None:
        self._pending = text

    @workflow.run
    async def run(self, session_id: str, idle_seconds: int = 2) -> str:
        turns = 0
        while True:
            try:
                await workflow.wait_condition(
                    lambda: self._pending is not None,
                    timeout=timedelta(seconds=idle_seconds),
                )
            except asyncio.TimeoutError:
                return "evicted" if turns == 0 else f"evicted_after_{turns}"
            text = self._pending or ""
            self._pending = None
            await workflow.execute_activity(
                run_turn,
                text,
                start_to_close_timeout=timedelta(seconds=10),
            )
            turns += 1
