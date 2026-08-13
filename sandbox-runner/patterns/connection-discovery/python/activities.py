from temporalio import activity

CATALOG = [
    {"name": "linear__list_issues", "summary": "List issues", "tokens": "SECRET"},
    {"name": "github__list_prs", "summary": "List pull requests", "tokens": "SECRET"},
]

@activity.defn
async def connection_search(query: str) -> list[dict]:
    q = query.lower()
    out = []
    for item in CATALOG:
        if q in item["name"] or q in item["summary"].lower():
            out.append({"name": item["name"], "summary": item["summary"]})
    return out

@activity.defn
async def invoke_connection_tool(tool_name: str) -> str:
    return f"invoked:{tool_name}"
