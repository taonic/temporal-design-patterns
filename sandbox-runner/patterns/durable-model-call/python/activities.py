from temporalio import activity


@activity.defn
async def call_model(prompt: str, model: str) -> dict:
    # Stub provider — no API key. Returns text plus fake token usage.
    return {
        "text": f"stub-reply: {prompt[:80]}",
        "usage": {
            "model": model,
            "input_tokens": 12,
            "output_tokens": 24,
        },
    }
