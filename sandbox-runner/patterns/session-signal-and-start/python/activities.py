from temporalio import activity


@activity.defn
async def reply_turn(text: str) -> str:
    return f"echo:{text}"
