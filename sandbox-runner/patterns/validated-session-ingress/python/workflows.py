from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@dataclass
class Delivery:
    delivery_id: str
    text: str


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._deliveries: set[str] = set()
        self._queue: list[str] = []
        self._stop = False

    @workflow.update
    async def deliver(self, d: Delivery) -> str:
        if d.delivery_id in self._deliveries:
            return "duplicate"
        self._deliveries.add(d.delivery_id)
        self._queue.append(d.text)
        return "accepted"

    @deliver.validator
    def validate_deliver(self, d: Delivery) -> None:
        if not d.delivery_id or not d.text.strip():
            raise ValueError("delivery_id and text required")
        if len(d.text) > 8000:
            raise ValueError("text too large")

    @workflow.signal
    def stop(self) -> None:
        self._stop = True

    @workflow.run
    async def run(self, session_id: str) -> str:
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
