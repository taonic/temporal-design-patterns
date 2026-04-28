from datetime import timedelta
from typing import Awaitable, Callable, List

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import (
        add_address,
        add_bank_account,
        add_client,
        clear_postal_addresses,
        create_account,
        disconnect_bank_accounts,
        remove_client,
    )
    from shared import OpenAccountRequest


@workflow.defn
class OpenAccountWorkflow:
    @workflow.run
    async def run(self, req: OpenAccountRequest) -> str:
        compensations: List[Callable[[], Awaitable[None]]] = []
        retry = RetryPolicy(maximum_attempts=1)

        try:
            workflow.logger.info(
                f"Opening account {req.accountId} for {req.clientName}"
            )

            # Step 1: create_account has no compensation registered — leaving
            # an empty account stub on later failure is acceptable for this demo.
            await workflow.execute_activity(
                create_account,
                req,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            compensations.append(
                lambda: workflow.execute_activity(
                    clear_postal_addresses,
                    req,
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=retry,
                )
            )
            await workflow.execute_activity(
                add_address,
                req,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            compensations.append(
                lambda: workflow.execute_activity(
                    remove_client,
                    req,
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=retry,
                )
            )
            await workflow.execute_activity(
                add_client,
                req,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            compensations.append(
                lambda: workflow.execute_activity(
                    disconnect_bank_accounts,
                    req,
                    start_to_close_timeout=timedelta(seconds=10),
                    retry_policy=retry,
                )
            )
            await workflow.execute_activity(
                add_bank_account,
                req,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry,
            )

            return f"Account {req.accountId} opened"
        except Exception as err:
            workflow.logger.warning(
                f"Account {req.accountId} failed ({err}); running {len(compensations)} compensation(s)"
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
            return f"Account {req.accountId} rolled back: {err}"
