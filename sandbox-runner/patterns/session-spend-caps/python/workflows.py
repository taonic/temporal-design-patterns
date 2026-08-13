from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


@dataclass
class Budget:
    max_tokens: int
    used_tokens: int = 0


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._budget = Budget(max_tokens=100)
        self._pending: list[str] = []
        self._stop = False

    @workflow.update
    async def raise_cap(self, max_tokens: int) -> int:
        self._budget.max_tokens = max_tokens
        return self._budget.max_tokens

    @workflow.signal
    def enqueue(self, text: str) -> None:
        self._pending.append(text)

    @workflow.signal
    def stop(self) -> None:
        self._stop = True

    @workflow.query
    def used_tokens(self) -> int:
        return self._budget.used_tokens

    @workflow.run
    async def run(self, session_id: str) -> str:
        outcomes: list[str] = []
        while not self._stop or self._pending:
            await workflow.wait_condition(lambda: bool(self._pending) or self._stop)
            while self._pending:
                if self._budget.used_tokens >= self._budget.max_tokens:
                    outcomes.append("budget_exceeded")
                    self._pending.clear()
                    self._stop = True
                    break
                text = self._pending.pop(0)
                usage = await workflow.execute_activity(
                    call_model,
                    text,
                    start_to_close_timeout=timedelta(seconds=10),
                )
                self._budget.used_tokens += int(usage["total_tokens"])
                if self._budget.used_tokens > self._budget.max_tokens:
                    outcomes.append("budget_exceeded")
                    self._pending.clear()
                    self._stop = True
                    break
                outcomes.append(usage["text"])
        return "|".join(outcomes)
