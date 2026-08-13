from temporalio import activity


@activity.defn
async def transfer_funds(amount: int) -> str:
    return f"transferred:{amount}"
