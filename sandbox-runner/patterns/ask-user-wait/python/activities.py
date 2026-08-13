from temporalio import activity


@activity.defn
async def model_step(phase: str, user_answer: str) -> dict:
    if phase == "ask":
        return {"kind": "ask_user", "prompt": "Refund amount?", "options": ["25", "50"]}
    return {"kind": "final", "text": f"refunding {user_answer}"}
