from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import fetch_batch, process_record
    from shared import BATCH_SIZE


@workflow.defn
class DataProcessorWorkflow:
    @workflow.run
    async def run(self, cursor: str = "", total_processed: int = 0) -> int:
        batch = await workflow.execute_activity(
            fetch_batch,
            args=[cursor, BATCH_SIZE],
            start_to_close_timeout=timedelta(seconds=10),
        )

        for record in batch:
            await workflow.execute_activity(
                process_record,
                record,
                start_to_close_timeout=timedelta(seconds=10),
            )
            total_processed += 1
            cursor = record["id"]

        workflow.logger.info(
            f"Processed batch of {len(batch)} (running total: {total_processed})"
        )

        if len(batch) == BATCH_SIZE:
            workflow.continue_as_new(args=[cursor, total_processed])

        return total_processed
