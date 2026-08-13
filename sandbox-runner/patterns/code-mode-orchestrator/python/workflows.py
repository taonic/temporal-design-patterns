from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import host_search, host_summarize, run_script


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        # Code Mode Orchestrator: one script step, host calls remain Activities.
        await workflow.execute_activity(
            run_script,
            "orchestrate_search",
            start_to_close_timeout=timedelta(seconds=30),
        )
        hits = await workflow.execute_activity(
            host_search,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        summary = await workflow.execute_activity(
            host_summarize,
            hits,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return summary
