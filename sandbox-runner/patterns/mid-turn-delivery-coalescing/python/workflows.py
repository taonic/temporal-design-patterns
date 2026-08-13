from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@dataclass
class Delivery:
    delivery_id: str
    actor_id: str
    text: str


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._buffer: list[Delivery] = []
        self._turn_open = False
        self._stop = False
        self._outcomes: list[str] = []

    @workflow.update
    async def deliver(self, d: Delivery) -> str:
        if self._turn_open:
            self._buffer.append(d)
            return "queued"
        self._buffer.append(d)
        return "accepted"

    @workflow.signal
    def mark_turn_open(self) -> None:
        self._turn_open = True

    @workflow.signal
    def mark_turn_idle(self) -> None:
        self._turn_open = False

    @workflow.signal
    def stop(self) -> None:
        self._stop = True

    def _coalesce(self) -> list[str]:
        if not self._buffer:
            return []
        first = self._buffer[0].actor_id
        texts: list[str] = []
        while self._buffer and self._buffer[0].actor_id == first:
            texts.append(self._buffer.pop(0).text)
        return texts

    @workflow.run
    async def run(self, session_id: str) -> str:
        # Demo: first delivery starts a "turn"; more queue; idle drains coalesce.
        while not self._stop or self._buffer:
            await workflow.wait_condition(
                lambda: (not self._turn_open and bool(self._buffer)) or self._stop
            )
            if self._stop and not self._buffer:
                break
            if self._turn_open:
                continue
            batch = self._coalesce()
            if not batch:
                continue
            self._turn_open = True
            out = await workflow.execute_activity(
                run_turn,
                batch,
                start_to_close_timeout=timedelta(seconds=10),
            )
            self._outcomes.append(out)
            self._turn_open = False
        return ";".join(self._outcomes)
