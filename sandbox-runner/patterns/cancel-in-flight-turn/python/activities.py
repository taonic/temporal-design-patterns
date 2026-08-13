import asyncio

from temporalio import activity


@activity.defn
async def call_model(prompt: str) -> str:
    for i in range(100):
        if activity.is_cancelled():
            raise asyncio.CancelledError()
        activity.heartbeat(i)
        await asyncio.sleep(0.1)
    return f"done:{prompt}"
