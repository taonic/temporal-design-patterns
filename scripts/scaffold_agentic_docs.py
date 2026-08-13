#!/usr/bin/env python3
"""Generate vernacular, category, and pattern Markdown stubs plus wave-1 samples."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PATTERNS = ROOT / "sandbox-runner" / "patterns"
ICONS = "/images/child-workflows-icon.svg"  # reuse existing icon until custom SVGs land

VERNACULAR = [
    ("identity", "Identity", "Stable identifiers for agents, sessions, turns, and steps."),
    ("session-turn-step", "Session, Turn, and Step", "How durable agent work is nested and bounded."),
    ("event-stream", "Event Stream", "The ordered record of session, turn, and step lifecycle."),
    ("tools-and-operations", "Tools and Operations", "Callable tools and typed agent operations."),
    ("approvals-vernacular", "Approvals", "When tool calls pause for human decisions."),
    ("sandbox-vernacular", "Sandbox and Code Mode", "Running model-authored scripts over host tools."),
    ("http-and-client", "HTTP and Client", "Session APIs and client drivers for agents."),
    ("filesystem-authoring", "Filesystem Authoring", "Organizing agent code so identity follows paths."),
]

CATEGORIES = [
    (
        "agent-session-patterns",
        "Agent & Session Patterns",
        "These patterns model long-lived agent sessions and how turns attach to them.",
        [
            ("session-workflow", "Session Workflow", "One Workflow owns a session, memory, and event stream."),
            ("turn-workflow", "Turn Workflow", "Isolate each turn as a child Workflow or sub-state."),
            ("session-signal-and-start", "Session with Signal-and-Start", "Create or signal a session from the first message."),
            ("entity-agent", "Entity Agent", "One long-lived agent Workflow per business entity."),
            ("continue-as-new-session", "Continue-As-New Session", "Reset history while preserving session identity."),
        ],
    ),
    (
        "tool-model-call-patterns",
        "Tool & Model Call Patterns",
        "These patterns make model and tool calls durable Temporal Activities or deterministic Workflow code.",
        [
            ("activity-tool", "Activity Tool", "Side-effecting tools as durable Activities."),
            ("workflow-tool", "Workflow Tool", "Deterministic tools as in-Workflow code."),
            ("callback-tool", "Callback Tool", "Tools that run on an attached client."),
            ("durable-model-call", "Durable Model Call", "LLM calls as first-class Activity steps."),
            ("tool-retry-profiles", "Tool Retry Profiles", "Per-tool retry and safety policies."),
        ],
    ),
    (
        "human-in-the-loop-patterns",
        "Human-in-the-loop Patterns",
        "These patterns pause agents for approvals, corrections, and operator commands.",
        [
            ("approval-gated-tools", "Approval-Gated Tools", "Require approval before risky tools run."),
            ("session-scoped-approvals", "Session-Scoped Approvals", "Approve a tool for the rest of a session."),
            ("resumable-correction", "Resumable Correction", "Park after repeated failures until a human fixes inputs."),
            ("operator-slash-commands", "Operator Slash Commands", "Deterministic textual commands inside the session."),
        ],
    ),
    (
        "subagent-patterns",
        "Subagent & Multi-agent Patterns",
        "These patterns compose agents as typed toolsets and durable child sessions.",
        [
            ("subagent-toolset", "Subagent Toolset", "Drive another agent through typed operations."),
            ("persistent-subagent-threads", "Persistent Subagent Threads", "Reusable durable threads per topic or user."),
            ("fanout-subagents", "Fan-Out Subagents", "Spawn many subagent sessions in parallel."),
            ("remote-subagent", "Remote Subagent", "Drive an agent hosted elsewhere via session HTTP."),
        ],
    ),
    (
        "code-mode-patterns",
        "Code Mode & Sandbox Patterns",
        "These patterns let a model orchestrate tools by writing scripts that call host APIs.",
        [
            ("code-mode-orchestrator", "Code Mode Orchestrator", "One run-code tool over many host tools."),
            ("tools-only-sandbox", "Tools-Only Sandbox", "Scripts may only call host tools."),
            ("type-checked-scripts", "Type-Checked Scripts", "Reject ill-typed scripts before execution."),
            ("script-fan-out", "Script Fan-Out", "Concurrent tool and subagent calls from one script."),
        ],
    ),
    (
        "safety-security-patterns",
        "Safety & Security Patterns",
        "These patterns label tools and environments so policy can gate or block unsafe calls.",
        [
            ("safety-profiled-tools", "Safety-Profiled Tools", "Declare inherently safe, idempotent, or non-idempotent tools."),
            ("security-profiles-per-agent", "Security Profiles per Agent", "Environment-specific tool and network allowances."),
            ("network-resource-sandboxing", "Network & Resource Sandboxing", "Bound sandboxes as data planes under Workflow control."),
        ],
    ),
    (
        "memory-state-patterns",
        "Memory & State Patterns",
        "These patterns keep conversation and knowledge durable across turns and sessions.",
        [
            ("session-memory", "Session Memory", "Store summaries in session state between turns."),
            ("cross-session-memory", "Cross-Session Memory", "Share bounded memory across sessions."),
            ("externalized-memory", "Externalized Memory", "Push large memory behind durable tools."),
        ],
    ),
    (
        "observability-patterns",
        "Observability & Operations Patterns",
        "These patterns make agent behavior reconstructable from events, traces, and metrics.",
        [
            ("standardized-event-stream", "Standardized Event Stream", "One ordered stream per session."),
            ("agent-tracing", "Agent Tracing", "Correlate spans with session and step IDs."),
            ("cost-token-accounting", "Cost & Token Accounting", "Aggregate usage per call, turn, and session."),
            ("eval-backed-behavior-checks", "Eval-Backed Behavior Checks", "Regression checks on recorded sessions."),
        ],
    ),
    (
        "channel-integration-patterns",
        "Channel & Integration Patterns",
        "These patterns bind agents to HTTP, messaging, and external tool catalogs.",
        [
            ("http-channel-agent", "HTTP Channel Agent", "Expose a session API over HTTP and SSE."),
            ("messaging-channel-agent", "Messaging Channel Agent", "Map Slack or email into sessions."),
            ("mcp-openapi-tooling", "MCP / OpenAPI Tooling", "Compile external tools into Activity tools."),
        ],
    ),
]

WAVE1 = {
    "session-workflow",
    "activity-tool",
    "workflow-tool",
    "approval-gated-tools",
    "operator-slash-commands",
    "callback-tool",
    "code-mode-orchestrator",
}


def vernacular_page(slug: str, title: str, blurb: str) -> str:
    return f"""\
# {title}

## Overview

{blurb}
This page defines the term as used across the catalog so pattern pages can stay concise.

## Problem

Without shared names for agent work units, teams invent conflicting models for conversations, tool calls, and approvals.
You then cannot compare designs or reconstruct what an agent did from a single record.

## Solution

Use a small vernacular that maps cleanly onto Temporal durability:

```mermaid
flowchart TB
    Session --> Turn
    Turn --> Step
    Step --> Events[Event stream]
```

The following describes each step in the diagram:

1. A Session is the long-lived unit that owns cross-turn state and the ordered event stream.
2. A Turn is one input and the agent work that follows until a reply, error, or cancel.
3. A Step is the smallest durable unit inside a turn (model call, tool call, approval wait, and similar).
4. Events record session, turn, and step lifecycle so observers can reconstruct the run.

## When to use

Read this page when you adopt a new pattern and need the definition of a term used in Overview or Solution.

## Benefits and trade-offs

Shared vernacular keeps pattern pages consistent.
The trade-off is that you must learn a small vocabulary before the catalog reads fluently.

## Comparison with alternatives

| Approach | Consistency | Cost |
| :--- | :--- | :--- |
| Shared vernacular | High | Learn a few terms |
| Ad-hoc per team | Low | Rework and confusion |

## Best practices

- **Reuse catalog terms.** Prefer Session, Turn, and Step over inventing synonyms.
- **Map to Temporal clearly.** Document which Workflow or Activity backs each term when durability matters.

## Common pitfalls

- **Treating turns as free-floating processes.** Turns belong to a Session so memory and approvals stay coherent.
- **Skipping events.** Without an event stream, UIs and audits cannot reconstruct the agent lifecycle.

## Related patterns

See the Agent & Session and Observability pattern sections.

## Sample code

See pattern pages that apply this vernacular, such as [Session Workflow](/session-workflow).

## References

- [Temporal Docs: Workflows](https://docs.temporal.io/workflows)
- [Temporal Docs: Activities](https://docs.temporal.io/activities)
"""


def category_page(slug: str, title: str, intro: str, patterns: list[tuple[str, str, str]]) -> str:
    tiles = []
    for pslug, pname, pdesc in patterns:
        tiles.append(
            f"""\
<div class="pattern-tile">
<a href="{pslug}">
<div class="pattern-tile-header">
<img src="{ICONS}" alt="{pname}">
<span>{pname}</span>
</div>
<p>{pdesc}</p>
</a>
</div>"""
        )
    choosing_lines = []
    for pslug, pname, pdesc in patterns:
        choosing_lines.append(
            f"**You need {pname.lower()} behavior:** {pdesc} Use [{pname}](/{pslug})."
        )
    choosing = "\n\n".join(choosing_lines)

    return f"""\
<h1>{title} <img src="{ICONS}" alt="{title}" class="pattern-page-icon"></h1>

{intro}

## Patterns in This Section

<div class="pattern-grid">
{chr(10).join(tiles)}
</div>

## Choosing a Pattern

{choosing}

## Related Sections

See Vernacular for Session, Turn, Step, and related terms used by these patterns.
"""


def pattern_stub(slug: str, title: str, blurb: str, full: bool = False) -> str:
    runner = f'\n<DaytonaRunner pattern="{slug}" />\n' if slug in WAVE1 else "\n"
    impl_note = (
        "The live runner executes a Python sample that demonstrates the pattern with a deterministic stub model."
        if slug in WAVE1
        else "A runnable sample may be added later; the Python sketches below show the structure."
    )
    return f"""\
<h1>{title} <img src="{ICONS}" alt="{title}" class="pattern-page-icon"></h1>

## Overview

{blurb}
You use Temporal Workflows and Activities under the hood so the agent can pause, retry, and resume without losing session state.

## Problem

Without this pattern, you risk losing mid-turn progress on worker restarts, double-executing side effects, or scattering session state across ad-hoc stores that are hard to audit.

## Solution

Structure the agent so the durable boundary matches the pattern:

```mermaid
flowchart LR
    Input[Input] --> Session
    Session --> Turn
    Turn --> Step
    Step --> Out[Reply or wait]
```

The following describes each step in the diagram:

1. An input arrives for a Session (message, channel event, or schedule).
2. The Session starts or continues a Turn.
3. The Turn runs Steps (model calls, tools, approvals) as durable units.
4. The Turn ends with a reply, an error, or a wait for an external decision.

```python
# agent/agent.py — structural sketch
from temporalio import workflow

@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str) -> None:
        # Own cross-turn state, approvals, and the event stream.
        ...
```

## Implementation
{runner}
{impl_note}

### Session ownership

Keep memory, approval overrides, and the ordered event stream on the Session Workflow so every Turn shares one durable context.

### Step boundaries

Run non-deterministic or side-effecting work in Activities so completed Steps replay from recorded results after a restart.

## When to use

This pattern fits when you need the behavior described in Overview and Problem.
It is not a good fit when a short-lived script without durability is enough.

## Benefits and trade-offs

You gain crash safety, clear observability, and a place to hang approvals.
You accept Workflow history growth and the need to Continue-As-New on long sessions.

## Comparison with alternatives

| Approach | Durability | Isolation |
| :--- | :--- | :--- |
| This pattern | High | Clear Session/Turn/Step boundaries |
| In-memory agent loop | None | Lost on restart |

## Best practices

- **Emit events at boundaries.** Record turn and step start/end so UIs can reconstruct the run.
- **Keep Workflows deterministic.** Put model and IO calls in Activities.
- **Name Sessions stably.** Use a Session ID that external channels can address.

## Common pitfalls

- **Doing IO in the Workflow.** Non-deterministic calls break replay.
- **Unbounded history.** Long sessions must Continue-As-New with a state snapshot.
- **Silent retries on non-idempotent tools.** Gate or key those tools before automatic retry.

## Related patterns

- [Session Workflow](/session-workflow)
- [Activity Tool](/activity-tool)
- [Standardized Event Stream](/standardized-event-stream)

## Sample code

See `sandbox-runner/patterns/{slug}/python/` when a live sample exists for this pattern.

## References

- [Temporal Docs: Workflows](https://docs.temporal.io/workflows)
- [Temporal Docs: Activities](https://docs.temporal.io/activities)
- [Temporal Docs: Continue-As-New](https://docs.temporal.io/workflow-execution/continue-as-new)
"""


def write_index() -> None:
    sections = []
    for slug, title, intro, patterns in CATEGORIES:
        tiles = []
        for pslug, pname, pdesc in patterns:
            tiles.append(
                f"""\
<div class="pattern-tile">
<a href="{pslug}">
<div class="pattern-tile-header">
<img src="{ICONS}" alt="{pname}">
<span>{pname}</span>
</div>
<p>{pdesc}</p>
</a>
</div>"""
            )
        overview_tile = f"""\
<div class="pattern-tile">
<a href="{slug}">
<div class="pattern-tile-header">
<img src="{ICONS}" alt="{title}">
<span>{title} Overview</span>
</div>
<p>{intro}</p>
</a>
</div>"""
        sections.append(
            f"""\
## {title.removesuffix(' Patterns')} patterns {{.pattern-section-title}}

<div class="pattern-grid">
{chr(10).join(tiles)}
{overview_tile}
</div>
"""
        )
    body = f"""\
# Temporal Agentic Patterns

> **Warning:** This catalog is under active development. Content and structure may change.

Temporal provides durable execution primitives that you can compose into common, reusable patterns for AI agents.
Having these patterns in your toolbox helps you keep sessions, tools, approvals, and subagents durable, observable, and safe.

{chr(10).join(sections)}
"""
    (DOCS / "index.md").write_text(body)


def write_docs() -> None:
    for slug, title, blurb in VERNACULAR:
        (DOCS / f"{slug}.md").write_text(vernacular_page(slug, title, blurb))
    for slug, title, intro, patterns in CATEGORIES:
        (DOCS / f"{slug}.md").write_text(category_page(slug, title, intro, patterns))
        for pslug, pname, pdesc in patterns:
            (DOCS / f"{pslug}.md").write_text(pattern_stub(pslug, pname, pdesc))


PYPROJECT = '''[project]
name = "{name}"
version = "0.1.0"
description = "Agentic pattern sample"
requires-python = ">=3.12"
dependencies = [
    "temporalio==1.9.0",
]

[tool.uv]
package = false
'''

PATTERN_JSON = '''{{
  "name": "{name}",
  "languages": {{
    "python": {{
      "label": "Python",
      "files": {files},
      "worker": "uv run python worker.py",
      "starter": "uv run python starter.py",
      "workerProcessPattern": "python worker.py"
    }}
  }}
}}
'''


def write_sample(pattern_id: str, files: dict[str, str]) -> None:
    base = PATTERNS / pattern_id
    py = base / "python"
    py.mkdir(parents=True, exist_ok=True)
    file_list = list(files.keys())
    (base / "pattern.json").write_text(
        PATTERN_JSON.format(name=pattern_id, files=str(file_list).replace("'", '"'))
    )
    (py / "pyproject.toml").write_text(PYPROJECT.format(name=pattern_id.replace("-", "_")))
    for rel, content in files.items():
        path = py / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


SHARED_WORKER = '''\
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import call_model, run_tool

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[call_model, run_tool],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
'''

SHARED_STARTER = '''\
import asyncio
import uuid

from temporalio.client import Client

from workflows import AgentSessionWorkflow

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "Hello from the catalog sample"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    result = await handle.result()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
'''


def wave1_samples() -> None:
    # Session Workflow + Activity Tool + durable model call stub
    write_sample(
        "session-workflow",
        {
            "shared.py": 'TASK_QUEUE = "agentic-patterns"\n',
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def call_model(prompt: str) -> str:
    # Deterministic stub — no external API key required.
    return f"stub-reply: {prompt[:80]}"


@activity.defn
async def run_tool(name: str, payload: str) -> str:
    return f"{name}:ok:{payload}"
''',
            "workflows.py": '''\
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import call_model, run_tool


@workflow.defn
class AgentSessionWorkflow:
    """Session Workflow: one durable Workflow owns turns for a session_id."""

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        events: list[str] = [f"session_started:{session_id}", "turn_started"]
        reply = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        events.append("model_call_completed")
        tool_result = await workflow.execute_activity(
            run_tool,
            args=["echo", reply],
            start_to_close_timeout=timedelta(seconds=30),
        )
        events.append(f"tool_call_completed:{tool_result}")
        events.append("turn_ended")
        events.append("session_ended")
        return " | ".join(events)
''',
            "worker.py": SHARED_WORKER,
            "starter.py": SHARED_STARTER,
        },
    )

    write_sample(
        "activity-tool",
        {
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def charge_card(amount_cents: int, idempotency_key: str) -> str:
    # Side-effecting tool body — retries must use the idempotency key.
    return f"charged:{amount_cents}:{idempotency_key}"


@activity.defn
async def call_model(prompt: str) -> str:
    return "charge 500 cents"
''',
            "workflows.py": '''\
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model, charge_card


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        decision = await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        # Activity Tool: durable, retried, observable step boundary.
        result = await workflow.execute_activity(
            charge_card,
            args=[500, f"{session_id}-charge-1"],
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"{decision} -> {result}"
''',
            "worker.py": SHARED_WORKER.replace(
                "from activities import call_model, run_tool",
                "from activities import call_model, charge_card",
            ).replace("activities=[call_model, run_tool]", "activities=[call_model, charge_card]"),
            "starter.py": SHARED_STARTER,
        },
    )

    write_sample(
        "workflow-tool",
        {
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def call_model(prompt: str) -> str:
    return "validate total 42"
''',
            "workflows.py": '''\
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import call_model


def validate_total(cents: int) -> str:
    """Workflow Tool: pure, deterministic, no Activity boundary."""
    if cents < 0:
        raise ValueError("negative total")
    return f"valid:{cents}"


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        await workflow.execute_activity(
            call_model,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return validate_total(42)
''',
            "worker.py": '''\
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import call_model

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[call_model],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
''',
            "starter.py": SHARED_STARTER,
        },
    )

    write_sample(
        "approval-gated-tools",
        {
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def transfer_funds(amount: int) -> str:
    return f"transferred:{amount}"
''',
            "workflows.py": '''\
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import transfer_funds


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._approved = False
        self._decision = ""

    @workflow.signal
    def approve(self, decision: str) -> None:
        self._decision = decision
        self._approved = decision == "granted"

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        # Emit approval_requested semantics by waiting for a Signal.
        await workflow.wait_condition(lambda: self._approved or self._decision == "denied")
        if self._decision == "denied":
            return "approval_denied"
        result = await workflow.execute_activity(
            transfer_funds,
            100,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return f"approval_granted:{result}"
''',
            "worker.py": '''\
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import transfer_funds

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[transfer_funds],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
''',
            "starter.py": '''\
import asyncio
import uuid

from temporalio.client import Client

from workflows import AgentSessionWorkflow

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "transfer 100"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentSessionWorkflow.approve, "granted")
    result = await handle.result()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
''',
        },
    )

    write_sample(
        "operator-slash-commands",
        {
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def noop(_: str) -> str:
    return "ok"
''',
            "workflows.py": '''\
from temporalio import workflow


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._commands: list[str] = []
        self._stop = False
        self._policy = "strict"

    @workflow.signal
    def slash(self, command: str) -> None:
        self._commands.append(command)
        if command.startswith("/approvals "):
            self._policy = command.split(" ", 1)[1]
        elif command == "/stop":
            self._stop = True

    @workflow.query
    def status(self) -> str:
        return f"policy={self._policy};commands={len(self._commands)}"

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        await workflow.wait_condition(lambda: self._stop or len(self._commands) > 0)
        if not self._stop:
            # Auto-stop after first command so the sample completes.
            self._stop = True
        return f"slash_command_invoked:{self._commands[-1]}:{self._policy}"
''',
            "worker.py": '''\
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import noop

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[noop],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
''',
            "starter.py": '''\
import asyncio
import uuid

from temporalio.client import Client

from workflows import AgentSessionWorkflow

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "hi"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    await handle.signal(AgentSessionWorkflow.slash, "/approvals safe")
    result = await handle.result()
    print(result)
    print(await handle.query(AgentSessionWorkflow.status))


if __name__ == "__main__":
    asyncio.run(main())
''',
        },
    )

    write_sample(
        "callback-tool",
        {
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def noop(_: str) -> str:
    return "ok"
''',
            "workflows.py": '''\
from temporalio import workflow


@workflow.defn
class AgentSessionWorkflow:
    def __init__(self) -> None:
        self._callback_result: str | None = None

    @workflow.signal
    def callback_completed(self, result: str) -> None:
        self._callback_result = result

    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        # callback_requested: park until the client posts a result.
        await workflow.wait_condition(lambda: self._callback_result is not None)
        return f"callback_completed:{self._callback_result}"
''',
            "worker.py": '''\
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import noop

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[noop],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
''',
            "starter.py": '''\
import asyncio
import uuid

from temporalio.client import Client

from workflows import AgentSessionWorkflow

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, "read local file"],
        id=session_id,
        task_queue=TASK_QUEUE,
    )
    # Simulates the attached client completing the callback tool.
    await handle.signal(AgentSessionWorkflow.callback_completed, "file://notes.md")
    result = await handle.result()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
''',
        },
    )

    write_sample(
        "code-mode-orchestrator",
        {
            "activities.py": '''\
from temporalio import activity


@activity.defn
async def host_search(query: str) -> list[str]:
    return [f"hit:{query}:1", f"hit:{query}:2"]


@activity.defn
async def host_summarize(items: list[str]) -> str:
    return f"summary({len(items)})"


@activity.defn
async def run_script(script_name: str) -> str:
    # Stub Code Mode: pretend the model wrote a script that fans out host calls.
    return f"script_ran:{script_name}"
''',
            "workflows.py": '''\
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import host_search, host_summarize, run_script


@workflow.defn
class AgentSessionWorkflow:
    @workflow.run
    async def run(self, session_id: str, user_message: str) -> str:
        # Code Mode Orchestrator: one script step, host calls remain Activities.
        await workflow.execute_activity(
            run_script,
            "orchestrate_search",
            start_to_close_timeout=timedelta(seconds=30),
        )
        hits = await workflow.execute_activity(
            host_search,
            user_message,
            start_to_close_timeout=timedelta(seconds=30),
        )
        summary = await workflow.execute_activity(
            host_summarize,
            hits,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return summary
''',
            "worker.py": '''\
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows import AgentSessionWorkflow
from activities import host_search, host_summarize, run_script

TASK_QUEUE = "agentic-patterns"


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[host_search, host_summarize, run_script],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
''',
            "starter.py": SHARED_STARTER,
        },
    )


def main() -> None:
    write_index()
    write_docs()
    wave1_samples()
    print("Scaffolded docs and wave-1 samples.")


if __name__ == "__main__":
    main()
