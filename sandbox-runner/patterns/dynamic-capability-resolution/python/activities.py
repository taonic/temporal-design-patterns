from temporalio import activity


@activity.defn
async def resolve_capabilities(principal: dict) -> dict:
    role = principal.get("role", "viewer")
    tools = ["search"]
    if role == "admin":
        tools.append("deploy")
    return {
        "catalog_snapshot_id": f"cat@{role}",
        "tool_names": tools,
    }


@activity.defn
async def call_model(catalog_snapshot_id: str, tool_names: list[str], user_message: str) -> str:
    return f"snap={catalog_snapshot_id}|tools={','.join(tool_names)}|msg={user_message}"
