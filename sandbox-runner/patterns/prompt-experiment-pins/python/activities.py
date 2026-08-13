from temporalio import activity


@activity.defn
async def call_model(prompt_version: str, user: str) -> str:
    return f"{prompt_version}:{user}"
