from temporalio import activity


@activity.defn
async def call_model(prompt: str) -> str:
    return "validate total 42"
