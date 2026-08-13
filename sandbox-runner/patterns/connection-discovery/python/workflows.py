from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import connection_search, invoke_connection_tool

@workflow.defn
class AgentTurnWorkflow:
    def __init__(self) -> None:
        self._loaded: set[str] = set()

    @workflow.run
    async def run(self, query: str, tool_name: str) -> str:
        matches = await workflow.execute_activity(
            connection_search, query, start_to_close_timeout=timedelta(seconds=15)
        )
        self._loaded.update(m["name"] for m in matches)
        if tool_name not in self._loaded:
            return "tool_not_loaded"
        return await workflow.execute_activity(
            invoke_connection_tool, tool_name, start_to_close_timeout=timedelta(seconds=30)
        )
