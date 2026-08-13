from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@dataclass
class SessionPins:
    definition_revision: str
    binding_revision: str


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._pins: SessionPins | None = None

    @workflow.query
    def pins(self) -> dict:
        if not self._pins:
            return {}
        return {
            "definition_revision": self._pins.definition_revision,
            "binding_revision": self._pins.binding_revision,
        }

    @workflow.run
    async def run(self, session_id: str, pins: SessionPins, user_message: str) -> str:
        self._pins = pins
        return await workflow.execute_activity(
            call_model,
            args=[pins.definition_revision, pins.binding_revision, user_message],
            start_to_close_timeout=timedelta(seconds=30),
        )
