from temporalio import activity

from shared import WORKER_BUILD_ID


@activity.defn
async def call_model(definition_revision: str, binding_revision: str, user_message: str) -> dict:
    return {
        "worker_build_id": WORKER_BUILD_ID,
        "definition_revision": definition_revision,
        "binding_revision": binding_revision,
        "text": user_message,
    }
