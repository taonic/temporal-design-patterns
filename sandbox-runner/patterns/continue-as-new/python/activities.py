import asyncio

from temporalio import activity

from shared import TOTAL_RECORDS


@activity.defn
async def fetch_batch(cursor: str, batch_size: int) -> list[dict]:
    start = 0 if cursor == "" else int(cursor) + 1
    end = min(start + batch_size, TOTAL_RECORDS)
    return [{"id": str(i)} for i in range(start, end)]


@activity.defn
async def process_record(record: dict) -> None:
    await asyncio.sleep(0.05)
