from temporalio import activity


@activity.defn
async def call_summarize_model(text: str, max_tokens: int) -> str:
    return text[: max(1, min(max_tokens, len(text)))]
