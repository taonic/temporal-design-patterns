from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def call_tool(name: str, item_id: str) -> str:
    if item_id == "poison":
        raise ApplicationError("poison_payload", type="PoisonTool", non_retryable=True)
    return f"{name}:{item_id}"
