from temporalio import activity

@activity.defn
async def ship_external(arg: str) -> str:
    return f"shipped:{arg}"
