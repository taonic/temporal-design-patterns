from temporalio import activity
from temporalio.exceptions import ApplicationError

from shared import load_secret, store_secret


@activity.defn
async def call_connected_tool(connection_id: str) -> str:
    token = load_secret(connection_id)
    if not token:
        raise ApplicationError("needs_auth", type="NeedsAuth", non_retryable=True)
    return f"tool:{connection_id}:ok"


@activity.defn
async def store_token(connection_id: str, token: str) -> str:
    store_secret(connection_id, token)
    return "stored"
