from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@dataclass
class DeliveryAck:
    delivery_id: str
    status: str
    turn_id: str | None = None


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._deliveries: dict[str, DeliveryAck] = {}
        self._pending: list[tuple[str, str]] = []
        self._stop = False

    @workflow.update
    async def deliver(self, delivery_id: str, text: str) -> DeliveryAck:
        existing = self._deliveries.get(delivery_id)
        if existing:
            return DeliveryAck(
                delivery_id=existing.delivery_id,
                status="duplicate",
                turn_id=existing.turn_id,
            )
        turn_id = f"turn-{len(self._deliveries) + 1}"
        ack = DeliveryAck(delivery_id=delivery_id, status="accepted", turn_id=turn_id)
        self._deliveries[delivery_id] = ack
        self._pending.append((turn_id, text))
        return ack

    @workflow.signal
    def stop(self) -> None:
        self._stop = True

    @workflow.run
    async def run(self, session_id: str) -> str:
        results: list[str] = []
        while not self._stop or self._pending:
            await workflow.wait_condition(lambda: bool(self._pending) or self._stop)
            while self._pending:
                turn_id, text = self._pending.pop(0)
                out = await workflow.execute_activity(
                    run_turn,
                    text,
                    start_to_close_timeout=timedelta(seconds=30),
                )
                results.append(f"{turn_id}:{out}")
        return "|".join(results)
