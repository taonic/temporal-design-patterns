from temporalio import activity

@activity.defn
async def answer_turn(user_message: str) -> str:
    return f"answered:{user_message}"

@activity.defn
async def generate_suggestions(user_message: str, reply: str) -> list[str]:
    return [f"Tell me more about {user_message}", "Summarize next steps"]
