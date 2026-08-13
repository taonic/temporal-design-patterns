from temporalio import activity

@activity.defn
async def exec_in_sandbox(command: str, mode: str) -> str:
    if mode == "read-only" and command.startswith("write "):
        return "denied:read-only"
    if mode == "workspace-write" and command.startswith("write /etc"):
        return "denied:outside_writable_roots"
    return f"{mode}:{command}"
