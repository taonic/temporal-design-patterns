from temporalio import activity


@activity.defn
async def first_step(text: str) -> str:
    return f"eager:{text}"
