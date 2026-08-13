from temporalio import activity


@activity.defn
async def charge_card(amount_cents: int, idempotency_key: str) -> str:
    # Side-effecting tool body — retries must use the idempotency key.
    return f"charged:{amount_cents}:{idempotency_key}"


@activity.defn
async def call_model(prompt: str) -> str:
    return "charge 500 cents"
