from temporalio import activity


@activity.defn
async def sanitize_user_text(text: str) -> str:
    return text.strip().lower()


@activity.defn
async def call_model(prompt: str) -> str:
    return f"stub-reply:{prompt}"
