from temporalio import activity


@activity.defn
async def call_llm(messages: list[dict]) -> dict:
    # Stub provider: request a search once, then return final text.
    if any(m.get("role") == "tool" for m in messages):
        return {
            "content": "Based on search: Temporal Workflows are durable functions.",
            "tool_calls": [],
        }
    return {
        "content": "",
        "tool_calls": [
            {
                "id": "call_1",
                "name": "search",
                "arguments": "what is a temporal workflow",
            }
        ],
    }


@activity.defn
async def search(query: str) -> str:
    return f"search-results:{query}"
