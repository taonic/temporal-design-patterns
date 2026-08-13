from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def guardrail_check(kind: str, text: str) -> dict:
    if "FORBIDDEN" in text:
        raise ApplicationError(
            "guardrail_blocked",
            type="GuardrailBlocked",
            non_retryable=True,
        )
    return {"kind": kind, "status": "allow"}


@activity.defn
async def call_model(text: str) -> str:
    return f"reply:{text}"
