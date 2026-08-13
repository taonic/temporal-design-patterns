from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def check_binding_ready(binding_revision: str) -> dict:
    if binding_revision.endswith(":down"):
        raise ApplicationError(
            "binding_not_ready",
            type="BindingNotReady",
            non_retryable=True,
        )
    return {"ready": True, "binding_revision": binding_revision}


@activity.defn
async def call_model(text: str) -> str:
    return f"ok:{text}"
