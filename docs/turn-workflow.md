<h1>Turn Workflow <img src="/images/child-workflows-icon.svg" alt="Turn Workflow" class="pattern-page-icon"></h1>

## Overview

The Turn Workflow pattern represents each agent turn (input → reply) as its own Child Workflow or explicitly tracked sub-state.
A turn encapsulates model reasoning, tool calls, and subagents, and emits a self-contained slice of the event stream.
Primitives used: Turn, TurnId, Step, Child Workflow (optional), turn events.

## Problem

When every turn shares one undifferentiated Workflow path, a stuck tool call or heavy child can block the whole session.
You also lose a clean unit for cancellation, timeouts, and per-turn metrics.

## Solution

Model each Turn as a bounded unit: either a Child Workflow started by the Session, or a Session sub-state with its own `turn_id`, step list, and timeout.
The Session remains the owner of memory and approvals; the Turn owns the work for one input.

```mermaid
flowchart TB
    Session --> Turn1[Turn Child or sub-state]
    Turn1 --> Steps[Model and tool Steps]
    Steps --> Events[turn_* events]
    Turn1 --> Session
```

The following describes each step in the diagram:

1. The Session receives an input and allocates a `turn_id`.
2. It starts a Turn Child Workflow or enters turn sub-state.
3. The Turn runs model and tool Steps, then returns a reply or error.
4. The Session merges results into memory and continues waiting for the next input.

```python
# Session starts an isolated turn
handle = await workflow.start_child_workflow(
    AgentTurnWorkflow.run,
    args=[session_id, turn_id, user_message],
    id=f"{session_id}-{turn_id}",
)
reply = await handle
```

## Implementation

<DaytonaRunner pattern="turn-workflow" />


### Child Workflow turns

Use Child Workflows when turns need strong isolation, independent timeouts, or parallelism with other turns.

### Embedded turns

Keep turns in Session state when isolation overhead is unnecessary, but still emit `turn_started` / `turn_ended` and track Steps explicitly.

### Cancel in-flight Steps

Expose a Session or Turn cancel path (Signal, Update, or `/stop` slash command) that:

1. Cancels the open Turn Child Workflow (or marks embedded turn state cancelled).
2. Cancels in-flight Activities with a reason so Workers stop model and tool work instead of finishing spend after the user left.
3. Cascades to Fan-Out children with an intentional `ParentClosePolicy` (usually cancel, not abandon).
4. Emits `turn_cancelled` (or equivalent) so Progress Streaming and Cost & Token Accounting close the bracket.

Idempotent tools still matter: cancel is not undo. Design write tools so a cancelled Activity retry does not double-apply.

```python
import asyncio

@workflow.signal
async def cancel_turn(self, reason: str) -> None:
    self._cancel_reason = reason
    if self._turn_handle:
        self._turn_handle.cancel()  # Child Turn Workflow
    # Embedded turns: set a flag; Activities must heartbeat and honor is_cancelled

@activity.defn
async def call_model(prompt: str) -> str:
    # Long model/tool Activities should heartbeat and check cancellation.
    while True:
        if activity.is_cancelled():
            # Best-effort provider abort if available; then acknowledge cancel.
            raise asyncio.CancelledError()
        activity.heartbeat("streaming")
        ...
```

Pair cancel with [Heartbeat Long Steps](/heartbeat-long-steps) so Workers notice cancellation promptly instead of waiting for `start_to_close_timeout`.

## When to use

Use Turn Workflows when turns are independent, need cancellation, or must be metered separately.
Prefer embedded turns for short, tightly coupled chat loops.

## Benefits and trade-offs

You gain per-turn isolation and clearer observability.
You accept Child Workflow overhead or the discipline of explicit sub-state.

## Comparison with alternatives

| Approach | Isolation | Overhead |
| :--- | :--- | :--- |
| Turn as Child Workflow | High | Higher |
| Turn as Session sub-state | Medium | Lower |
| No turn boundary | Low | Lowest |

## Best practices

- **Always assign `turn_id`.** Search attributes and events depend on it.
- **Bound turn duration.** Use timeouts so a hung tool cannot stall the session forever.
- **Return typed outcomes.** Reply, error, and cancel should be explicit.
- **Cancel Activities, not only the Workflow wait.** Otherwise model calls keep running after the UI stops.

## Common pitfalls

- **Starting unbounded parallel turns.** Cap concurrency on the Session.
- **Duplicating session memory in every child.** Pass summaries, not full history.
- **Forgetting Parent Close Policy.** Decide whether children survive session stop.
- **Reusing Child Workflow IDs.** Colliding IDs fail starts or attach to the wrong Turn.
- **Parent Continue-As-New without snapshotting open turn children.** You lose handles to in-flight Turns.
- **Stopping the UI without cancelling the Turn.** Tokens and tool side effects continue until timeouts fire.

## Related patterns

- [Session Workflow](/session-workflow)
- [Fan-Out Subagents](/fanout-subagents)
- [Operator Slash Commands](/operator-slash-commands)
- [Scheduled Agent Turns](/scheduled-agent-turns)
- [Standardized Event Stream](/standardized-event-stream)

## Sample code

- [`sandbox-runner/patterns/turn-workflow/python/`](https://github.com/temporal-sa/temporal-agentic-patterns/tree/main/sandbox-runner/patterns/turn-workflow/python)

## References

- [Temporal Docs: Child Workflows](https://docs.temporal.io/child-workflows)
