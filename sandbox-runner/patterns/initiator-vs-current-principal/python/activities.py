from temporalio import activity

@activity.defn
async def noop() -> str:
    return "ok"
