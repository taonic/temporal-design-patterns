from temporalio import activity


@activity.defn
async def run_turn(texts: list[str]) -> str:
    return "|".join(texts)
