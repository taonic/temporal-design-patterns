from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import poll_job_until_done, start_job


@workflow.defn
class AgentSessionWorkflow:
    """External Tool Polling: start job, poll inside Activity with heartbeats."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        job_id = await workflow.execute_activity(
            start_job,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        result = await workflow.execute_activity(
            poll_job_until_done,
            job_id,
            start_to_close_timeout=timedelta(seconds=30),
            heartbeat_timeout=timedelta(seconds=10),
        )
        return f"{result['state']}:{result['result']}"
