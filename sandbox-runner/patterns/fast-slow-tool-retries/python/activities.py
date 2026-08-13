from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def flaky_tool(prompt: str) -> str:
    attempt = activity.info().attempt
    # Fail fast-phase attempts; succeed once slow phase starts (attempt resets per execute).
    # Use a side channel via heartbeat details? Better: fail when attempt < 3 always for first
    # execute; second execute (slow) uses same activity — attempt starts at 1 again.
    # Demo: fail attempts 1-2, succeed on 3+ so fast phase (max 2) exhausts, slow succeeds quickly.
    if attempt < 3:
        raise ApplicationError(f"transient:{attempt}", non_retryable=False)
    return f"ok:{prompt}:attempt={attempt}"
