from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.workflow import ParentClosePolicy

with workflow.unsafe.imports_passed_through():
    from activities import risky_tool


@dataclass
class ProxyRequest:
    request_id: str
    child_id: str
    tool_name: str


@dataclass
class HumanDecision:
    request_id: str
    status: str


@workflow.defn
class ChildTurnWorkflow:
    def __init__(self) -> None:
        self._decision: str | None = None

    @workflow.signal
    def approval_result(self, status: str) -> None:
        self._decision = status

    @workflow.run
    async def run(self, parent_id: str, child_id: str, amount: int) -> str:
        parent = workflow.get_external_workflow_handle(parent_id)
        await parent.signal(
            ParentSessionWorkflow.child_needs_approval,
            ProxyRequest(request_id="r1", child_id=child_id, tool_name="transfer"),
        )
        await workflow.wait_condition(lambda: self._decision is not None)
        if self._decision != "granted":
            return "denied"
        return await workflow.execute_activity(
            risky_tool,
            amount,
            start_to_close_timeout=timedelta(seconds=10),
        )


@workflow.defn
class ParentSessionWorkflow:
    def __init__(self) -> None:
        self._pending: ProxyRequest | None = None
        self._decision: HumanDecision | None = None

    @workflow.signal
    def child_needs_approval(self, req: ProxyRequest) -> None:
        self._pending = req

    @workflow.signal
    def human_decision(self, decision: HumanDecision) -> None:
        self._decision = decision

    @workflow.run
    async def run(self, session_id: str, amount: int) -> str:
        child_id = f"{session_id}-child"
        child = await workflow.start_child_workflow(
            ChildTurnWorkflow.run,
            args=[session_id, child_id, amount],
            id=child_id,
            parent_close_policy=ParentClosePolicy.TERMINATE,
        )
        await workflow.wait_condition(lambda: self._pending is not None)
        await workflow.wait_condition(lambda: self._decision is not None)
        assert self._pending is not None and self._decision is not None
        handle = workflow.get_external_workflow_handle(self._pending.child_id)
        await handle.signal(
            ChildTurnWorkflow.approval_result,
            self._decision.status,
        )
        return await child
