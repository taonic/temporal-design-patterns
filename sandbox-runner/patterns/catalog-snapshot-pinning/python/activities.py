from temporalio import activity
from temporalio.exceptions import ApplicationError

from shared import SNAPSHOTS


@activity.defn
async def call_model(catalog_snapshot_id: str, user_message: str) -> str:
    snap = SNAPSHOTS.get(catalog_snapshot_id)
    if snap is None:
        raise ApplicationError("unknown_snapshot", type="UnknownSnapshot", non_retryable=True)
    return f"{catalog_snapshot_id}|{snap['instructions']}|{user_message}"
