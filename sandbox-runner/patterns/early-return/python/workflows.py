from datetime import timedelta
from typing import Optional

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import cancel_transaction, complete_transaction, init_transaction
    from shared import Transaction, TransactionRequest


@workflow.defn
class TransactionWorkflow:
    def __init__(self) -> None:
        self.tx: Optional[Transaction] = None
        self.init_done: bool = False
        self.init_err: Optional[Exception] = None

    @workflow.run
    async def run(self, req: TransactionRequest) -> Optional[Transaction]:
        # Phase 1: fast synchronous initialization (local activity).
        try:
            self.tx = await workflow.execute_local_activity(
                init_transaction,
                req,
                schedule_to_close_timeout=timedelta(seconds=5),
            )
        except Exception as e:
            self.init_err = e
        finally:
            self.init_done = True

        # Phase 2: slow asynchronous completion.
        if self.init_err is not None:
            await workflow.execute_activity(
                cancel_transaction,
                self.tx,
                start_to_close_timeout=timedelta(seconds=30),
            )
            return None

        await workflow.execute_activity(
            complete_transaction,
            self.tx,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return self.tx

    @workflow.update
    async def return_init_result(self) -> Transaction:
        await workflow.wait_condition(lambda: self.init_done)
        if self.init_err is not None:
            raise self.init_err
        assert self.tx is not None
        return self.tx
