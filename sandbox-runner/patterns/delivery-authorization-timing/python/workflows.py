from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import run_turn


@dataclass
class Delivery:
    delivery_id: str
    text: str
    actor_id: str
    tenant_id: str


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._owner = ""
        self._queue: list[Delivery] = []
        self._revoked: set[str] = set()
        self._stop = False
        self._outcomes: list[str] = []

    @workflow.signal
    def revoke_actor(self, actor_id: str) -> None:
        self._revoked.add(actor_id)

    @workflow.signal
    def stop(self) -> None:
        self._stop = True

    @workflow.update
    async def deliver(self, d: Delivery) -> str:
        if self._owner and d.tenant_id != self._owner:
            return "forbidden"
        self._queue.append(d)
        return "accepted"

    @deliver.validator
    def validate_deliver(self, d: Delivery) -> None:
        if not d.delivery_id or not d.text.strip():
            raise ValueError("invalid_delivery")
        # Skip tenant check until run() has assigned owner (Update can race first Task).
        if self._owner and d.tenant_id != self._owner:
            raise ValueError("forbidden")

    @workflow.run
    async def run(self, session_id: str, owner: str) -> str:
        self._owner = owner
        while not self._stop or self._queue:
            await workflow.wait_condition(lambda: bool(self._queue) or self._stop)
            while self._queue:
                d = self._queue.pop(0)
                if d.tenant_id != self._owner or d.actor_id in self._revoked:
                    self._outcomes.append(f"{d.delivery_id}:rejected_at_apply")
                    continue
                out = await workflow.execute_activity(
                    run_turn,
                    d.text,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                self._outcomes.append(f"{d.delivery_id}:{out}")
        return "|".join(self._outcomes)
