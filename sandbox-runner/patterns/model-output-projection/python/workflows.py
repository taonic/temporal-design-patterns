from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import create_ticket

def to_model_output(full: dict) -> dict:
    return {"type": "json", "value": {"status": full["status"], "id": full["id"]}}

@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self) -> dict:
        full = await workflow.execute_activity(
            create_ticket, start_to_close_timeout=timedelta(seconds=30)
        )
        projected = to_model_output(full)
        return {"channel": full, "model": projected}
