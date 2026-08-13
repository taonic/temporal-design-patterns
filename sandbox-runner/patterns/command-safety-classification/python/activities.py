from temporalio import activity

SAFE = {"ls", "pwd", "echo"}

@activity.defn
async def classify_command(command: str) -> dict:
    compact = command.replace(" ", "")
    if "rm-rf/" in compact or "curl|sh" in compact or ":(){:|:&};:" in compact:
        return {"requirement": "forbid", "reason": "dangerous_pattern", "is_safe": False}
    head = command.strip().split(" ", 1)[0]
    if head in SAFE and "|" not in command and ";" not in command:
        return {"requirement": "skip", "reason": "known_safe", "is_safe": True}
    return {"requirement": "need_approval", "reason": "unknown_command", "is_safe": False}

@activity.defn
async def exec_command(command: str) -> str:
    return f"ran:{command}"
