from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import compact_transcript


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, memory: dict, tool_state: dict) -> dict:
        summary = await workflow.execute_activity(
            compact_transcript,
            memory["transcript"],
            start_to_close_timeout=timedelta(seconds=10),
        )
        memory = {"transcript": [summary]}
        tool_state = dict(tool_state)
        tool_state["read_files"] = {}
        if tool_state.get("todos"):
            memory["transcript"].append(f"Active todos: {tool_state['todos']}")
        return {
            "memory": memory,
            "approved_tools": tool_state.get("approved_tools", []),
            "read_files": tool_state.get("read_files", {}),
            "todos": tool_state.get("todos", []),
        }
