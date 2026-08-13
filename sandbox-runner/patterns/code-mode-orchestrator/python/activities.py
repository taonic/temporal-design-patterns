from temporalio import activity


@activity.defn
async def host_search(query: str) -> list[str]:
    return [f"hit:{query}:1", f"hit:{query}:2"]


@activity.defn
async def host_summarize(items: list[str]) -> str:
    return f"summary({len(items)})"


@activity.defn
async def run_script(script_name: str) -> str:
    # Stub Code Mode: pretend the model wrote a script that fans out host calls.
    return f"script_ran:{script_name}"
