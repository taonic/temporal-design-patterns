from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_summarize_model


@dataclass
class SummarizeRequest:
    text: str
    max_tokens: int = 32


@dataclass
class SummarizeResponse:
    summary: str
    prompt_version: str


@workflow.defn
class SpecialistSession:
    def __init__(self) -> None:
        self._done = False

    @workflow.query
    def list_operations(self) -> list[dict]:
        return [{"name": "summarize", "version": "1", "kind": "update"}]

    @workflow.update
    async def summarize(self, req: SummarizeRequest) -> SummarizeResponse:
        summary = await workflow.execute_activity(
            call_summarize_model,
            args=[req.text, req.max_tokens],
            start_to_close_timeout=timedelta(seconds=30),
        )
        return SummarizeResponse(summary=summary, prompt_version="summarize.v1")

    @summarize.validator
    def validate_summarize(self, req: SummarizeRequest) -> None:
        if not req.text.strip():
            raise ValueError("text required")

    @workflow.signal
    def stop(self) -> None:
        self._done = True

    @workflow.run
    async def run(self, session_id: str) -> str:
        await workflow.wait_condition(lambda: self._done)
        return "specialist-done"
