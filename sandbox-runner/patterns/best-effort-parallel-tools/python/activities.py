from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def search_web(query: str) -> str:
    # One branch fails; others return stub hits.
    if query == "fail":
        raise ApplicationError("search unavailable", non_retryable=True)
    return f"hits:{query}"
