from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import compact_session_memory


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, memory: dict, generation: int) -> str:
        turns = list(memory.get("turns", []))
        turns.append(f"turn-{generation}")
        memory = {**memory, "turns": turns}
        if generation == 0 and len(turns) >= 3:
            memory = await workflow.execute_activity(
                compact_session_memory,
                memory,
                start_to_close_timeout=timedelta(seconds=30),
            )
            workflow.continue_as_new(args=[session_id, memory, 1])
        return f"{memory.get('summary', '')}|turns={len(memory.get('turns', []))}"
