from temporalio import activity

@activity.defn
async def create_ticket() -> dict:
    return {
        "id": "T-1",
        "status": "open",
        "secret_token": "sekrit",
        "description": "long body " * 20,
    }
