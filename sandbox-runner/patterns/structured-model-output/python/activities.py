from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def call_structured_model(prompt: str) -> dict:
    # Stub "model" returns schema-shaped JSON.
    if "bad" in prompt:
        raise ApplicationError("schema_invalid", non_retryable=True)
    return {"intent": "search", "query": prompt, "limit": 3}
