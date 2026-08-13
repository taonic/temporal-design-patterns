from temporalio import activity


@activity.defn
async def compact_session_memory(memory: dict) -> dict:
    turns = memory.get("turns", [])
    summary = f"summary_of_{len(turns)}_turns"
    return {
        "summary": summary,
        "turns": turns[-2:],
        "open_items": memory.get("open_items", []),
    }
