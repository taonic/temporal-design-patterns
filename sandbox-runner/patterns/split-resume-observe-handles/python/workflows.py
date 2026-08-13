from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@dataclass
class Caps:
    resume_token: str
    observe_token: str


@dataclass
class Delivery:
    resume_token: str
    delivery_id: str
    text: str


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._caps: Caps | None = None
        self._queue: list[str] = []
        self._stop = False

    @workflow.query
    def observe(self, observe_token: str) -> dict:
        if not self._caps or observe_token != self._caps.observe_token:
            return {"ok": False, "error": "observe_forbidden"}
        return {"ok": True, "queued": len(self._queue)}

    @workflow.update
    async def deliver(self, d: Delivery) -> str:
        self._queue.append(d.text)
        return "accepted"

    @deliver.validator
    def validate_deliver(self, d: Delivery) -> None:
        if not self._caps or d.resume_token != self._caps.resume_token:
            raise ValueError("resume_forbidden")
        if not d.delivery_id or not d.text.strip():
            raise ValueError("invalid_delivery")

    @workflow.signal
    def stop(self) -> None:
        self._stop = True

    @workflow.run
    async def run(self, session_id: str, caps: Caps) -> str:
        self._caps = caps
        outs: list[str] = []
        while not self._stop or self._queue:
            await workflow.wait_condition(lambda: bool(self._queue) or self._stop)
            while self._queue:
                text = self._queue.pop(0)
                outs.append(
                    await workflow.execute_activity(
                        run_turn,
                        text,
                        start_to_close_timeout=timedelta(seconds=10),
                    )
                )
        return "|".join(outs)
