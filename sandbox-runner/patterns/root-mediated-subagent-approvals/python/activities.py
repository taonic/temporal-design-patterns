from temporalio import activity


@activity.defn
async def risky_tool(amount: int) -> str:
    return f"transferred:{amount}"
