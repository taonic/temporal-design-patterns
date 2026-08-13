from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@dataclass
class RestoreRequest:
    snapshot: dict
    reason: str


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._pending: str | None = None
        self._restore: RestoreRequest | None = None
        self._generation = 0

    @workflow.signal
    def user_message(self, text: str) -> None:
        self._pending = text

    @workflow.signal
    def operator_restore(self, req: RestoreRequest) -> None:
        self._restore = req

    @workflow.run
    async def run(self, session_id: str, memory: dict, generation: int = 0) -> str:
        self._generation = generation
        if generation > 0:
            return f"restored:{memory.get('note', '')}:gen={generation}"
        await workflow.wait_condition(
            lambda: self._pending is not None or self._restore is not None
        )
        if self._restore is not None:
            workflow.continue_as_new(
                args=[session_id, self._restore.snapshot, generation + 1]
            )
        text = self._pending or ""
        await workflow.execute_activity(
            run_turn,
            text,
            start_to_close_timeout=timedelta(seconds=10),
        )
        await workflow.wait_condition(lambda: self._restore is not None)
        snap = self._restore.snapshot if self._restore else {"note": "empty"}
        workflow.continue_as_new(args=[session_id, snap, generation + 1])
        return "unreachable"
