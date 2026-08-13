from temporalio import activity

DENIAL_MARKERS = ("permission denied", "read-only file system", "operation not permitted")

@activity.defn
async def run_sandboxed(command: str) -> dict:
    # Demo: commands containing "write /etc" fail as sandbox denials.
    if "write /etc" in command:
        msg = "permission denied: read-only file system"
        return {"ok": False, "output": msg, "sandbox_denial": True}
    if "boom" in command:
        return {"ok": False, "output": "exit 1: boom", "sandbox_denial": False}
    return {"ok": True, "output": f"sandboxed:{command}", "sandbox_denial": False}

@activity.defn
async def run_unsandboxed(command: str) -> str:
    return f"unsandboxed:{command}"
