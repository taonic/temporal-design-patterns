from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import load_blob, store_blob


@workflow.defn
class AgentSessionWorkflow:
    """Claim-Check Payloads: store large text, pass ref through the Turn."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        large = user_message * 50
        ref = await workflow.execute_activity(
            store_blob,
            large,
            start_to_close_timeout=timedelta(seconds=30),
        )
        loaded = await workflow.execute_activity(
            load_blob,
            ref,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"ref={ref}|bytes={len(loaded)}"
