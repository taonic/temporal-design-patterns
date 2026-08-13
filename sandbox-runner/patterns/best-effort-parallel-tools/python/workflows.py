import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import search_web


@workflow.defn
class AgentSessionWorkflow:
    """Best-Effort Parallel Tools: gather with return_exceptions, keep successes."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        queries = ["temporal", "fail", "workflows"]
        tasks = [
            workflow.execute_activity(
                search_web,
                q,
                start_to_close_timeout=timedelta(seconds=30),
                schedule_to_close_timeout=timedelta(seconds=60),
                retry_policy=RetryPolicy(maximum_attempts=1),
            )
            for q in queries
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        ok = [r for r in results if not isinstance(r, BaseException)]
        if not ok:
            return "no_successes"
        return f"successes={len(ok)}:{'|'.join(ok)}"
