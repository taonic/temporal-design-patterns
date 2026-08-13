from temporalio import activity


@activity.defn
async def run_task(text: str) -> str:
    return f"done:{text}"
