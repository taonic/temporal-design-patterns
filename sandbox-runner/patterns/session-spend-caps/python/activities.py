from temporalio import activity


@activity.defn
async def call_model(text: str) -> dict:
    return {"text": f"reply:{text}", "total_tokens": 60}
