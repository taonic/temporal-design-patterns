from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@dataclass
class ExperimentPin:
    experiment_id: str
    variant: str
    prompt_version: str


def assign_variant(session_id: str, experiment_id: str) -> ExperimentPin:
    variant = "A" if int(session_id[-1], 16) % 2 == 0 else "B"
    prompt_version = "v3" if variant == "A" else "v3-exp"
    return ExperimentPin(experiment_id, variant, prompt_version)


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._pin: ExperimentPin | None = None

    @workflow.query
    def experiment(self) -> dict:
        if not self._pin:
            return {}
        return {
            "experiment_id": self._pin.experiment_id,
            "variant": self._pin.variant,
            "prompt_version": self._pin.prompt_version,
        }

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        self._pin = assign_variant(session_id, "summarizer-2026-08")
        return await workflow.execute_activity(
            call_model,
            args=[self._pin.prompt_version, user_message],
            start_to_close_timeout=timedelta(seconds=10),
        )
