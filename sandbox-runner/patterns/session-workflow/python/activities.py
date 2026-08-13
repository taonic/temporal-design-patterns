from temporalio import activity


@activity.defn
async def call_model(prompt: str) -> str:
    # Deterministic stub — no external API key required.
    return f"stub-reply: {prompt[:80]}"


@activity.defn
async def run_tool(name: str, payload: str) -> str:
    return f"{name}:ok:{payload}"
