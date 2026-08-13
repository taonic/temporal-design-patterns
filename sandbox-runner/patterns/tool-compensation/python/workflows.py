from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from activities import (
        charge_customer,
        close_ticket,
        create_ticket,
        notify_user,
        refund_charge,
    )


@dataclass
class Compensation:
    kind: str
    arg: str


@workflow.defn
class AgentSessionWorkflow:
    """Tool Compensation: on failure, run undo Activities newest-first."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        compensations: list[Compensation] = []
        once = RetryPolicy(maximum_attempts=1)
        try:
            ticket = await workflow.execute_activity(
                create_ticket,
                user_message,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=once,
            )
            compensations.append(Compensation("close", ticket["id"]))

            charge = await workflow.execute_activity(
                charge_customer,
                ticket["id"],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=once,
            )
            compensations.append(Compensation("refund", charge["id"]))

            await workflow.execute_activity(
                notify_user,
                ticket["id"],
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=once,
            )
            return f"ok:{ticket['id']}"
        except ActivityError:
            undone: list[str] = []
            for comp in reversed(compensations):
                if comp.kind == "refund":
                    undone.append(
                        await workflow.execute_activity(
                            refund_charge,
                            comp.arg,
                            start_to_close_timeout=timedelta(seconds=30),
                            retry_policy=once,
                        )
                    )
                else:
                    undone.append(
                        await workflow.execute_activity(
                            close_ticket,
                            comp.arg,
                            start_to_close_timeout=timedelta(seconds=30),
                            retry_policy=once,
                        )
                    )
            return "compensated:" + "|".join(undone)
