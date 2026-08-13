from temporalio import activity


@activity.defn
async def call_model(prompt: str) -> str:
    return f"turn-reply:{prompt}"
