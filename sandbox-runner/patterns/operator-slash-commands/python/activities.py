from temporalio import activity


@activity.defn
async def noop(_: str) -> str:
    return "ok"
