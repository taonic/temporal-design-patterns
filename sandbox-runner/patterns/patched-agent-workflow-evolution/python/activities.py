from temporalio import activity


@activity.defn
async def guardrail_check(kind: str, text: str) -> str:
    return f"guard:{kind}"


@activity.defn
async def call_model(text: str) -> str:
    return f"model:{text}"
