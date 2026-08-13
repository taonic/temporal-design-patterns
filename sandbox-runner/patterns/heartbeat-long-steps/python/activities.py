import asyncio

from temporalio import activity


@activity.defn
async def long_model_step(prompt: str) -> str:
    details = activity.info().heartbeat_details
    start = int(details[0]) if details else 0
    chunks: list[str] = []
    for i in range(start, 5):
        if activity.is_cancelled():
            raise asyncio.CancelledError()
        chunks.append(f"tok{i}")
        activity.heartbeat(i + 1)
        await asyncio.sleep(0.05)
    return f"{prompt}:" + "".join(chunks)
