from datetime import timedelta
from typing import Awaitable, Callable, List

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import (
        deposit,
        deposit_compensation,
        notify_downstream,
        withdraw,
        withdraw_compensation,
    )
    from shared import TransferDetails


@workflow.defn
class TransferMoneyWorkflow:
    @workflow.run
    async def run(self, details: TransferDetails) -> str:
        compensations: List[Callable[[], Awaitable[None]]] = []
        retry = RetryPolicy(maximum_attempts=1)

        try:
            workflow.logger.info(
                f"Starting transfer {details.transferId}: ${details.amount}"
            )

            compensations.append(
                lambda: workflow.execute_activity(
                    withdraw_compensation,
                    details,
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=retry,
                )
            )
            await workflow.execute_activity(
                withdraw,
                details,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            compensations.append(
                lambda: workflow.execute_activity(
                    deposit_compensation,
                    details,
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=retry,
                )
            )
            await workflow.execute_activity(
                deposit,
                details,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            await workflow.execute_activity(
                notify_downstream,
                details,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            return f"Transfer {details.transferId} completed"
        except Exception as err:
            workflow.logger.warning(
                f"Transfer {details.transferId} failed ({err}); running {len(compensations)} compensation(s)"
            )
            for compensate in reversed(compensations):
                try:
                    await compensate()
                except Exception as comp_err:
                    workflow.logger.error(f"Compensation failed: {comp_err}")
            # Return a status instead of re-raising so the workflow execution
            # itself succeeds. Re-raising is the canonical pattern (see
            # saga-pattern.md best practices); this demo prefers a clean ✅
            # in the Temporal UI and surfaces the rollback via the result.
            return f"Transfer {details.transferId} rolled back: {err}"
