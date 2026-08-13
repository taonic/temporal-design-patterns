from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import ship_external

TOOLS = {
    "normalize": {"effect": "pure"},
    "remember": {"effect": "state"},
    "ship": {"effect": "external"},
}

@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._memory: list[str] = []

    @workflow.run
    async def run(self, tool: str, arg: str) -> str:
        effect = TOOLS[tool]["effect"]
        if effect == "pure":
            return arg.strip().lower()
        if effect == "state":
            self._memory.append(arg)
            return f"stored:{len(self._memory)}"
        return await workflow.execute_activity(
            ship_external, arg, start_to_close_timeout=timedelta(seconds=30)
        )
