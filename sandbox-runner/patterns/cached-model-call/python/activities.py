import hashlib

from temporalio import activity

from shared import CACHE


@activity.defn
async def call_model(prompt_id: str, prompt_version: str, user: str) -> dict:
    digest = hashlib.sha256(user.encode()).hexdigest()[:16]
    key = f"{prompt_id}:{prompt_version}:{digest}"
    cached = CACHE.get(key)
    if cached is not None:
        return {"text": cached, "cached": True, "total_tokens": 0}
    text = f"fresh:{user}"
    CACHE[key] = text
    return {"text": text, "cached": False, "total_tokens": 10}
