from temporalio import activity


@activity.defn
async def create_ticket(goal: str) -> dict:
    return {"id": f"tkt-{abs(hash(goal)) % 10000}", "goal": goal}


@activity.defn
async def charge_customer(ticket_id: str) -> dict:
    return {"id": f"chg-{ticket_id}", "amount": 25}


@activity.defn
async def notify_user(ticket_id: str) -> str:
    # Force compensation path for the demo.
    raise RuntimeError(f"notify failed for {ticket_id}")


@activity.defn
async def close_ticket(ticket_id: str) -> str:
    return f"closed:{ticket_id}"


@activity.defn
async def refund_charge(charge_id: str) -> str:
    return f"refunded:{charge_id}"
