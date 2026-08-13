from temporalio import activity


@activity.defn
async def run_turn(text: str) -> str:
    return f"ok:{text}"
