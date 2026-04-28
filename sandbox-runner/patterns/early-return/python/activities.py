import asyncio
import time
from typing import Optional

from temporalio import activity

from shared import Transaction, TransactionRequest


@activity.defn
async def init_transaction(req: TransactionRequest) -> Transaction:
    activity.logger.info(f"Init: validating {req.amount} {req.currency}")
    if req.amount <= 0:
        raise ValueError(f"Invalid amount: {req.amount}")
    return Transaction(id=f"tx-{int(time.time() * 1000)}", status="initialized")


@activity.defn
async def complete_transaction(tx: Transaction) -> None:
    # Simulate slow background settlement so the early-return effect is visible.
    await asyncio.sleep(2)
    activity.logger.info(f"Completed transaction {tx.id}")


@activity.defn
async def cancel_transaction(tx: Optional[Transaction]) -> None:
    label = tx.id if tx else "(uninitialized)"
    activity.logger.info(f"Cancelled transaction {label}")
