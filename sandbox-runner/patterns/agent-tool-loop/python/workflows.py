from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_llm, search


@workflow.defn
class AgentSessionWorkflow:
    """Agent Tool Loop: model Activity → tool Activities until done or max_steps."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        max_steps = 5
        messages: list[dict] = [{"role": "user", "content": user_message}]
        for _ in range(max_steps):
            response = await workflow.execute_activity(
                call_llm,
                messages,
                start_to_close_timeout=timedelta(seconds=30),
            )
            tool_calls = response.get("tool_calls") or []
            if not tool_calls:
                return response["content"]
            for call in tool_calls:
                result = await workflow.execute_activity(
                    search,
                    call["arguments"],
                    start_to_close_timeout=timedelta(seconds=60),
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": result,
                    }
                )
        return "max_steps_reached"
