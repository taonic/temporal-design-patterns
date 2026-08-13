from temporalio import activity

@activity.defn
async def fake_model(prompt: str) -> str:
    return f"reply:{prompt}"
