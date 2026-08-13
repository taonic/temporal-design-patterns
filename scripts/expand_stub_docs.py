#!/usr/bin/env python3
"""Replace generic scaffold pattern pages with unique full catalog pages."""
from __future__ import annotations

from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"

PAGES: dict[str, dict[str, str]] = {
    "turn-workflow": {
        "title": "Turn Workflow",
        "icon": "child-workflows-icon.svg",
        "overview": (
            "The Turn Workflow pattern represents each agent turn (input → reply) as its own "
            "Child Workflow or explicitly tracked sub-state.\n"
            "A turn encapsulates model reasoning, tool calls, and subagents, and emits a "
            "self-contained slice of the event stream.\n"
            "Primitives used: Turn, TurnId, Step, Child Workflow (optional), turn events."
        ),
        "problem": (
            "When every turn shares one undifferentiated Workflow path, a stuck tool call or "
            "heavy child can block the whole session.\n"
            "You also lose a clean unit for cancellation, timeouts, and per-turn metrics."
        ),
        "solution": (
            "Model each Turn as a bounded unit: either a Child Workflow started by the Session, "
            "or a Session sub-state with its own `turn_id`, step list, and timeout.\n"
            "The Session remains the owner of memory and approvals; the Turn owns the work for one input."
        ),
        "mermaid": """flowchart TB
    Session --> Turn1[Turn Child or sub-state]
    Turn1 --> Steps[Model and tool Steps]
    Steps --> Events[turn_* events]
    Turn1 --> Session""",
        "walk": [
            "The Session receives an input and allocates a `turn_id`.",
            "It starts a Turn Child Workflow or enters turn sub-state.",
            "The Turn runs model and tool Steps, then returns a reply or error.",
            "The Session merges results into memory and continues waiting for the next input.",
        ],
        "code": '''# Session starts an isolated turn
handle = await workflow.start_child_workflow(
    AgentTurnWorkflow.run,
    args=[session_id, turn_id, user_message],
    id=f"{session_id}-{turn_id}",
)
reply = await handle''',
        "impl": (
            "### Child Workflow turns\n\n"
            "Use Child Workflows when turns need strong isolation, independent timeouts, or "
            "parallelism with other turns.\n\n"
            "### Embedded turns\n\n"
            "Keep turns in Session state when isolation overhead is unnecessary, but still emit "
            "`turn_started` / `turn_ended` and track Steps explicitly."
        ),
        "when": (
            "Use Turn Workflows when turns are independent, need cancellation, or must be metered separately.\n"
            "Prefer embedded turns for short, tightly coupled chat loops."
        ),
        "benefits": (
            "You gain per-turn isolation and clearer observability.\n"
            "You accept Child Workflow overhead or the discipline of explicit sub-state."
        ),
        "table": (
            "| Approach | Isolation | Overhead |\n"
            "| :--- | :--- | :--- |\n"
            "| Turn as Child Workflow | High | Higher |\n"
            "| Turn as Session sub-state | Medium | Lower |\n"
            "| No turn boundary | Low | Lowest |"
        ),
        "practices": [
            "**Always assign `turn_id`.** Search attributes and events depend on it.",
            "**Bound turn duration.** Use timeouts so a hung tool cannot stall the session forever.",
            "**Return typed outcomes.** Reply, error, and cancel should be explicit.",
        ],
        "pitfalls": [
            "**Starting unbounded parallel turns.** Cap concurrency on the Session.",
            "**Duplicating session memory in every child.** Pass summaries, not full history.",
            "**Forgetting Parent Close Policy.** Decide whether children survive session stop.",
        ],
        "related": [
            "[Session Workflow](/session-workflow)",
            "[Fan-Out Subagents](/fanout-subagents)",
            "[Standardized Event Stream](/standardized-event-stream)",
        ],
        "refs": [
            "[Temporal Docs: Child Workflows](https://docs.temporal.io/child-workflows)",
        ],
    },
    "entity-agent": {
        "title": "Entity Agent",
        "icon": "entity-workflow-icon.svg",
        "overview": (
            "The Entity Agent pattern models a long-lived business entity as an agent.\n"
            "One Workflow per entity (account, workspace, user) owns its tools, policies, and subagents.\n"
            "All agentic work for that entity routes through the same Workflow for the entity lifetime.\n"
            "Primitives used: Session bound to entity ID, Entity Workflow lifetime, Continue-As-New Session."
        ),
        "problem": (
            "If each request spins a new agent session, entity policies, memory, and in-flight approvals scatter.\n"
            "Operators cannot ask one durable address what the entity agent is doing."
        ),
        "solution": (
            "Set `session_id` (or Workflow ID) to the entity ID.\n"
            "Route every channel message, schedule, and subagent call for that entity through the same Session Workflow.\n"
            "Use Continue-As-New to keep history bounded over months or years."
        ),
        "mermaid": """flowchart LR
    Channels --> Entity[Entity Agent Session]
    Schedules --> Entity
    Entity --> Tools[Tools and subagents]
    Entity --> Memory[Entity memory]""",
        "walk": [
            "An entity ID (account, workspace) becomes the durable Session ID.",
            "All inputs for that entity signal or update the same Workflow.",
            "The agent applies entity-scoped policies, memory, and tools.",
            "Continue-As-New preserves identity while resetting history.",
        ],
        "code": '''# Workflow ID == entity id
await client.start_workflow(
    EntityAgentWorkflow.run,
    args=[account_id],
    id=f"account-{account_id}",
    task_queue=TASK_QUEUE,
    start_signal="user_message",
    start_signal_args=[text],
)''',
        "impl": (
            "### Routing\n\n"
            "HTTP and messaging channels must derive the entity ID deterministically so retries "
            "hit the same Workflow.\n\n"
            "### Lifecycle\n\n"
            "Define when the entity agent completes (account closed) versus idles durably forever."
        ),
        "when": (
            "Use Entity Agents for per-account or per-workspace assistants with ongoing state.\n"
            "Use short Session Workflows for one-off jobs without an entity lifetime."
        ),
        "benefits": (
            "You get one source of truth for entity agent state and policy.\n"
            "You must operate long-lived Workflows carefully (Continue-As-New, visibility)."
        ),
        "table": (
            "| Approach | Continuity | Addressability |\n"
            "| :--- | :--- | :--- |\n"
            "| Entity Agent | High | Stable entity ID |\n"
            "| New session per chat | Low | Ephemeral |\n"
            "| Shared global agent | Medium | Contended |"
        ),
        "practices": [
            "**Align IDs with the business key.** Avoid random UUIDs for entity sessions.",
            "**Scope tools to the entity.** Prevent cross-tenant data access in tool arguments.",
            "**Idle durably.** Prefer signals over busy loops while waiting.",
        ],
        "pitfalls": [
            "**One Workflow for all entities.** Creates a hotspot and mixes tenancy.",
            "**Never Continue-As-New.** History grows without bound.",
            "**Caching Run IDs in clients.** Breaks after Continue-As-New.",
        ],
        "related": [
            "[Session Workflow](/session-workflow)",
            "[Continue-As-New Session](/continue-as-new-session)",
            "[Session with Signal-and-Start](/session-signal-and-start)",
        ],
        "refs": [
            "[Temporal Docs: Workflow ID](https://docs.temporal.io/workflow-execution/workflowid-runid)",
            "[Temporal Docs: Continue-As-New](https://docs.temporal.io/workflow-execution/continue-as-new)",
        ],
    },
    "durable-model-call": {
        "title": "Durable Model Call",
        "icon": "long-running-activity-icon.svg",
        "overview": (
            "The Durable Model Call pattern treats each LLM or model invocation as a first-class Activity "
            "with clear step boundaries and telemetry.\n"
            "Inputs and outputs are recorded in the event stream; retries and timeouts follow the same "
            "policies as other tools.\n"
            "Primitives used: ModelCallStep, model_call_* events, token_usage_reported."
        ),
        "problem": (
            "Calling a model SDK inside the Workflow breaks determinism.\n"
            "Calling it in an Activity without event boundaries makes cost, retries, and partial "
            "failures hard to observe."
        ),
        "solution": (
            "Wrap each provider call in an Activity.\n"
            "Emit `model_call_started` / `model_call_completed` / `model_call_failed` with provider, "
            "model name, timing, and token usage.\n"
            "Keep prompts and credentials out of the Workflow code path except as Activity inputs."
        ),
        "mermaid": """flowchart LR
    Turn --> Start[model_call_started]
    Start --> Act[Model Activity]
    Act --> End[model_call_completed]
    End --> Usage[token_usage_reported]""",
        "walk": [
            "The Turn decides a model call is required and emits start metadata.",
            "An Activity invokes the provider SDK with timeouts and retries.",
            "On success, the Turn records output summary and token usage.",
            "On failure, the Turn records error classification and decides retry or escalate.",
        ],
        "code": '''@activity.defn
async def call_model(prompt: str, model: str) -> dict:
    # Provider SDK runs only inside the Activity.
    text, usage = await provider.complete(prompt, model=model)
    return {"text": text, "usage": usage}''',
        "impl": (
            "### Stubbing for demos\n\n"
            "Catalog samples may return deterministic stub text so Daytona runs without API keys.\n"
            "Production Activities call the real provider.\n\n"
            "### Payload size\n\n"
            "Prefer storing large prompts or completions outside Workflow history when needed; "
            "keep summaries on the event stream."
        ),
        "when": (
            "Use Durable Model Calls for every production LLM invocation in an agent Turn.\n"
            "Avoid in-Workflow SDK calls entirely."
        ),
        "benefits": (
            "You gain retries, heartbeats, and cost visibility.\n"
            "Each call schedules an Activity; batching may be needed for tiny calls."
        ),
        "table": (
            "| Approach | Deterministic Workflow | Telemetry |\n"
            "| :--- | :--- | :--- |\n"
            "| Durable Model Call | Yes | Per call |\n"
            "| SDK in Workflow | No | Broken replay |\n"
            "| Fire-and-forget thread | No | Weak |"
        ),
        "practices": [
            "**Record token usage events.** Feed Cost & Token Accounting.",
            "**Classify retryable errors.** Rate limits vs invalid requests differ.",
            "**Heartbeat streaming calls.** Long generations need progress.",
        ],
        "pitfalls": [
            "**Putting API keys in Workflow arguments permanently.** Prefer worker-side env config.",
            "**Omitting model name in events.** Breaks cost attribution.",
            "**Retrying non-idempotent side-effect tools after a model retry.** Separate policies.",
        ],
        "related": [
            "[Activity Tool](/activity-tool)",
            "[Cost & Token Accounting](/cost-token-accounting)",
            "[Standardized Event Stream](/standardized-event-stream)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "tool-retry-profiles": {
        "title": "Tool Retry Profiles",
        "icon": "fixed-count-retries-icon.svg",
        "overview": (
            "The Tool Retry Profiles pattern assigns retry and safety profiles per tool.\n"
            "Read-only or idempotent tools can retry automatically; non-idempotent tools require "
            "approvals or idempotency keys.\n"
            "Primitives used: StepPolicy, SafetyProfile, ToolDefinition defaults."
        ),
        "problem": (
            "A single global retry policy either double-executes payments or gives up too early on "
            "transient read failures."
        ),
        "solution": (
            "Attach a default StepPolicy and SafetyProfile to each ToolDefinition.\n"
            "When the Turn schedules an Activity tool, apply that policy: attempt counts, backoff, "
            "and whether approval is required before the first attempt."
        ),
        "mermaid": """flowchart TD
    Tool[Tool selected] --> Profile{Safety profile}
    Profile -->|inherently_safe| Retry[Automatic retries]
    Profile -->|idempotent_side_effect| Key[Retries with idempotency key]
    Profile -->|non_idempotent| Gate[Approval or single attempt]""",
        "walk": [
            "Each tool declares safety and retry defaults.",
            "The Turn loads the profile when scheduling the Step.",
            "Safe tools retry; non-idempotent tools gate or require keys.",
            "Failures emit classified tool_call_failed events.",
        ],
        "code": '''TOOL_POLICIES = {
    "search": {"maximum_attempts": 5, "safety": "inherently_safe"},
    "charge": {"maximum_attempts": 1, "safety": "non_idempotent"},
}

policy = TOOL_POLICIES[tool_name]
await workflow.execute_activity(
    run_tool,
    args=[tool_name, payload],
    start_to_close_timeout=timedelta(seconds=30),
    retry_policy=RetryPolicy(maximum_attempts=policy["maximum_attempts"]),
)''',
        "impl": (
            "### Mapping to Temporal\n\n"
            "Encode profiles as RetryPolicy and timeouts on `execute_activity`.\n"
            "Keep the profile table next to tool definitions so authors cannot forget it.\n\n"
            "### Interaction with approvals\n\n"
            "Non-idempotent tools should usually combine a strict retry profile with Approval-Gated Tools."
        ),
        "when": (
            "Use per-tool profiles whenever an agent has mixed read and mutate tools.\n"
            "A single shared RetryPolicy is enough only for uniform read-only agents."
        ),
        "benefits": (
            "You avoid double side effects while still absorbing transient faults.\n"
            "You must maintain profile metadata as tools evolve."
        ),
        "table": (
            "| Profile | Retries | Typical tools |\n"
            "| :--- | :--- | :--- |\n"
            "| inherently_safe | Many | Search, fetch |\n"
            "| idempotent_side_effect | Few + key | Upserts |\n"
            "| non_idempotent | One or gated | Payments |"
        ),
        "practices": [
            "**Default deny for unknown tools.** Missing profile should fail closed.",
            "**Document idempotency keys.** Put key fields in the tool schema.",
            "**Align metrics.** Tag retries by tool_id and profile.",
        ],
        "pitfalls": [
            "**Copy-pasting payment retries from search tools.**",
            "**Silent profile overrides in one Turn.** Keep overrides explicit and evented.",
        ],
        "related": [
            "[Safety-Profiled Tools](/safety-profiled-tools)",
            "[Approval-Gated Tools](/approval-gated-tools)",
            "[Activity Tool](/activity-tool)",
        ],
        "refs": [
            "[Temporal Docs: Retry policies](https://docs.temporal.io/encyclopedia/retry-policies)",
        ],
    },
    "session-scoped-approvals": {
        "title": "Session-Scoped Approvals",
        "icon": "approval-icon.svg",
        "overview": (
            "The Session-Scoped Approvals pattern lets operators approve a tool for the rest of a "
            "session (“approve and stop asking”).\n"
            "The first call is gated; subsequent calls in the same session proceed automatically, "
            "with the decision recorded in session state.\n"
            "Primitives used: ApprovalDecision(scope=session), Session state, approval events."
        ),
        "problem": (
            "Requiring approval on every repeated call to the same tool fatigues operators and "
            "slows the agent without adding new information."
        ),
        "solution": (
            "On grant, record `{tool_id: granted}` in Session state for the session lifetime "
            "(or until revoked).\n"
            "Emit `approval_granted` with scope `session`.\n"
            "Later Turns skip the wait for that tool while the override remains."
        ),
        "mermaid": """flowchart TD
    Call1[First gated call] --> Wait[approval_requested]
    Wait --> Grant[approval_granted scope=session]
    Grant --> State[Session allow list]
    Call2[Later call] --> State
    State --> Run[Run tool without wait]""",
        "walk": [
            "The first gated tool call parks for approval.",
            "The operator grants with session scope (or uses a slash command allow-list).",
            "The Session stores the override durably.",
            "Later calls to that tool proceed until stop, revoke, or Continue-As-New snapshot drops it.",
        ],
        "code": '''# Session Workflow fields
self._session_allow: set[str] = set()

@workflow.signal
def approve_session_tool(self, tool_id: str) -> None:
    self._session_allow.add(tool_id)

def requires_approval(self, tool_id: str) -> bool:
    return tool_id not in self._session_allow and tool_id in self._gated''',
        "impl": (
            "### Slash command integration\n\n"
            "Commands such as `/allow-tools charge_card` should update the same Session allow list "
            "and emit `slash_command_invoked` plus approval events.\n\n"
            "### Continue-As-New\n\n"
            "Include the allow list in the session snapshot so overrides survive history reset."
        ),
        "when": (
            "Use session scope for repeated trusted actions inside one conversation.\n"
            "Keep one-off approvals for rare high-risk operations."
        ),
        "benefits": (
            "You reduce approval fatigue while keeping an audit trail.\n"
            "A stolen session Signal path becomes more powerful—authorize operators carefully."
        ),
        "table": (
            "| Scope | Asks again | Best for |\n"
            "| :--- | :--- | :--- |\n"
            "| Single call | Yes | Rare risky ops |\n"
            "| Session | No until revoke | Repeated tools |\n"
            "| Global policy change | No | Fleet-wide |"
        ),
        "practices": [
            "**Name the tool in the event.** Audits must see which tool was unlocked.",
            "**Support revoke.** Operators need `/deny-tools` or equivalent.",
            "**Do not widen scope silently.** Session grant must be explicit.",
        ],
        "pitfalls": [
            "**Persisting session grants into global config.** Leaks trust across sessions.",
            "**Forgetting to snapshot grants on Continue-As-New.**",
        ],
        "related": [
            "[Approval-Gated Tools](/approval-gated-tools)",
            "[Operator Slash Commands](/operator-slash-commands)",
            "[Continue-As-New Session](/continue-as-new-session)",
        ],
        "refs": [
            "[Temporal Docs: Signals](https://docs.temporal.io/encyclopedia/workflow-message-passing#sending-signals)",
        ],
    },
    "resumable-correction": {
        "title": "Resumable Correction",
        "icon": "resumable-activity-icon.svg",
        "overview": (
            "The Resumable Correction pattern combines retries and approvals.\n"
            "When a tool repeatedly fails (bad input, missing record), the agent parks in a "
            "resumable state, emits an event describing the error, and waits for a human to "
            "correct inputs or environment before resuming from the last safe step.\n"
            "Primitives used: Step failure classification, ApprovalWait/human wait, Session resume."
        ),
        "problem": (
            "Blind retries waste tokens and can worsen bad writes.\n"
            "Failing the whole session loses successful prior Steps."
        ),
        "solution": (
            "After a retry budget is exhausted on a retryable-but-stuck error, transition the Turn "
            "or Session into a correction wait.\n"
            "Emit an event with the error and suggested fix fields.\n"
            "On human correction Signal/Update, resume from the failed Step without replaying "
            "completed Steps."
        ),
        "mermaid": """flowchart TD
    Step[Tool Step] -->|fail| Retry{Budget left?}
    Retry -->|yes| Step
    Retry -->|no| Park[correction_requested]
    Park --> Human[Human fixes input]
    Human --> Resume[Resume from Step]""",
        "walk": [
            "A tool Step fails with a classified error.",
            "Retries follow the tool profile until the budget is spent.",
            "The Session parks and asks for correction instead of aborting everything.",
            "A human supplies corrected args or confirms environment fix; the Step runs again.",
        ],
        "code": '''if attempts >= max_attempts:
    self._correction = {"tool": tool_id, "error": err, "args": args}
    await workflow.wait_condition(lambda: self._corrected_args is not None)
    args = self._corrected_args
# execute Activity again with corrected args''',
        "impl": (
            "### What humans can change\n\n"
            "Allow argument patches, environment acknowledgements, or skip/cancel decisions.\n"
            "Validate corrected args against the tool schema before resume.\n\n"
            "### Completed Steps\n\n"
            "Rely on Workflow history / recorded results so successful prior Steps are not re-executed."
        ),
        "when": (
            "Use when failures are often fixable by humans (bad IDs, missing tickets).\n"
            "Fail fast when errors are permanent and uncorrectable."
        ),
        "benefits": (
            "You preserve partial progress and reduce wasted model loops.\n"
            "You add operational waits that need clear SLAs."
        ),
        "table": (
            "| Approach | Preserves progress | Human load |\n"
            "| :--- | :--- | :--- |\n"
            "| Resumable Correction | Yes | On stuck failures |\n"
            "| Abort session | No | Low |\n"
            "| Infinite auto-retry | Maybe | Hidden cost |"
        ),
        "practices": [
            "**Classify errors.** Only park on correction-eligible classes.",
            "**Show last args and error.** Operators cannot guess.",
            "**Cap park duration.** Expire or escalate.",
        ],
        "pitfalls": [
            "**Re-running non-idempotent success paths after resume.**",
            "**Parking on every transient 503.** Use retry profiles first.",
        ],
        "related": [
            "[Tool Retry Profiles](/tool-retry-profiles)",
            "[Approval-Gated Tools](/approval-gated-tools)",
            "[Session Workflow](/session-workflow)",
        ],
        "refs": [
            "[Temporal Docs: Activity retries](https://docs.temporal.io/encyclopedia/retry-policies)",
        ],
    },
    "subagent-toolset": {
        "title": "Subagent Toolset",
        "icon": "child-workflows-icon.svg",
        "overview": (
            "The Subagent Toolset pattern treats another agent as a typed toolset.\n"
            "A parent agent starts a subagent session and calls its operations through tools, "
            "while the subagent runs its own Workflow and tools.\n"
            "Primitives used: SubagentDefinition, SubagentHandle, ToolCalls into child operations, subagent events."
        ),
        "problem": (
            "Multi-agent systems that pass only free-text between agents lose structure, "
            "approvals, and clear parent/child audit trails."
        ),
        "solution": (
            "Expose the child agent's operations as tools on the parent.\n"
            "Starting the child creates a SubagentHandle (`parent_session_id`, `child_session_id`).\n"
            "Each operation call is a ToolCall Step that drives the child Session and emits "
            "`subagent_*` events."
        ),
        "mermaid": """flowchart LR
    Parent[Parent Session] -->|start| Child[Child Session]
    Parent -->|operation tool| Child
    Child --> ChildTools[Child tools]
    Parent --> Events[subagent_* events]""",
        "walk": [
            "The parent selects a subagent toolset.",
            "It starts or attaches a child Session and records `subagent_started`.",
            "Operation calls become tool Steps against the child.",
            "Completion or failure emits `subagent_completed` / `subagent_failed`.",
        ],
        "code": '''# Parent Workflow sketch
child = await workflow.start_child_workflow(
    ResearcherAgent.run,
    args=[child_session_id],
    id=child_session_id,
)
result = await workflow.execute_child_workflow(
    # or signal/update the child operation surface
    ResearcherAgent.run_research,
    args=[query],
    id=f"{child_session_id}-op-1",
)''',
        "impl": (
            "### Typed operations\n\n"
            "Prefer schema-validated operation inputs/outputs over raw chat strings "
            "when the parent is composing programmatically.\n\n"
            "### Approvals\n\n"
            "Parent policy may still gate starting a subagent or calling sensitive child operations."
        ),
        "when": (
            "Use for specialization (planner → researcher → executor).\n"
            "Keep a single agent when one toolset is enough."
        ),
        "benefits": (
            "You compose agents with contracts and durable isolation.\n"
            "You must design failure and cancellation across parent and child."
        ),
        "table": (
            "| Approach | Contract | Durability |\n"
            "| :--- | :--- | :--- |\n"
            "| Subagent Toolset | Typed ops | Child Session |\n"
            "| Prompt chaining only | Text | Weak |\n"
            "| Shared threads | Informal | Contended |"
        ),
        "practices": [
            "**Link IDs in events.** UI trees need parent/child edges.",
            "**Bound child lifetime.** Close or idle children explicitly.",
            "**Propagate cancellation.** Parent abort should stop children when appropriate.",
        ],
        "pitfalls": [
            "**Treating child chat text as the only API.**",
            "**Orphan children after parent Continue-As-New without handles in the snapshot.**",
        ],
        "related": [
            "[Fan-Out Subagents](/fanout-subagents)",
            "[Persistent Subagent Threads](/persistent-subagent-threads)",
            "[Remote Subagent](/remote-subagent)",
        ],
        "refs": [
            "[Temporal Docs: Child Workflows](https://docs.temporal.io/child-workflows)",
        ],
    },
    "persistent-subagent-threads": {
        "title": "Persistent Subagent Threads",
        "icon": "entity-workflow-icon.svg",
        "overview": (
            "The Persistent Subagent Threads pattern gives each user, project, or topic a durable "
            "subagent thread with its own context.\n"
            "The root agent creates and reuses these threads, which idle durably and periodically "
            "Continue-As-New.\n"
            "Primitives used: SubagentHandle reuse, Entity-like child Sessions, Continue-As-New."
        ),
        "problem": (
            "Starting a fresh subagent every time drops specialized context.\n"
            "Keeping everything in the parent Session mixes concerns and grows history faster."
        ),
        "solution": (
            "Allocate stable child session IDs such as `{parent}-researcher-{topic}`.\n"
            "Reuse signal-with-start against that ID.\n"
            "Children idle on Signals and Continue-As-New independently of the parent."
        ),
        "mermaid": """flowchart TB
    Parent --> T1[Thread topic-A]
    Parent --> T2[Thread topic-B]
    T1 -->|idle + signal| T1
    T2 -->|Continue-As-New| T2""",
        "walk": [
            "The parent maps a topic or user to a child session ID.",
            "It starts or signals that child for work.",
            "The child retains its own memory and tools across invocations.",
            "Each thread Continues-As-New on its own schedule.",
        ],
        "code": '''thread_id = f"{session_id}-topic-{topic}"
await client.start_workflow(
    TopicAgent.run,
    args=[thread_id],
    id=thread_id,
    task_queue=TASK_QUEUE,
    start_signal="user_message",
    start_signal_args=[text],
)''',
        "impl": (
            "### Directory of threads\n\n"
            "Keep a map of topic → thread_id in parent Session state or an external index.\n\n"
            "### Idle cost\n\n"
            "Durable idle is cheap; avoid polling loops inside children."
        ),
        "when": (
            "Use for ongoing specialists tied to entities or topics.\n"
            "Use one-shot subagents for disposable tasks."
        ),
        "benefits": (
            "You preserve specialized context without bloating the parent.\n"
            "You operate more long-lived Workflows."
        ),
        "table": (
            "| Approach | Context retention | Lifecycle |\n"
            "| :--- | :--- | :--- |\n"
            "| Persistent threads | High | Long-lived |\n"
            "| New subagent each call | None | Ephemeral |\n"
            "| All in parent | High | Parent hotspot |"
        ),
        "practices": [
            "**Stable thread IDs.** Deterministic from parent + topic.",
            "**Close unused threads.** Avoid unbounded idle agents.",
            "**Isolate secrets.** Thread tools should not see other topics' data.",
        ],
        "pitfalls": [
            "**Leaking thread IDs across tenants.**",
            "**Never Continue-As-New on busy threads.**",
        ],
        "related": [
            "[Subagent Toolset](/subagent-toolset)",
            "[Entity Agent](/entity-agent)",
            "[Continue-As-New Session](/continue-as-new-session)",
        ],
        "refs": [
            "[Temporal Docs: Signal-With-Start](https://docs.temporal.io/encyclopedia/workflow-message-passing#signal-with-start)",
        ],
    },
    "remote-subagent": {
        "title": "Remote Subagent",
        "icon": "webhooks-icon.svg",
        "overview": (
            "The Remote Subagent pattern drives an agent hosted in another runtime or cluster "
            "via its session HTTP API, while representing it locally as a subagent toolset.\n"
            "Parent and child still exchange events and approvals through the shared session protocol.\n"
            "Primitives used: HTTP Session client, SubagentHandle, remote session IDs, subagent events."
        ),
        "problem": (
            "Not every specialist can run as a Child Workflow in the same worker process or cluster.\n"
            "You still need durable parent orchestration and a unified audit story."
        ),
        "solution": (
            "Implement subagent tools as Activities that call the remote session HTTP API "
            "(create session, send message, stream events).\n"
            "Record remote `session_id` on the SubagentHandle and mirror important remote events "
            "into the parent stream."
        ),
        "mermaid": """flowchart LR
    Parent[Parent Session] --> Act[Activity client]
    Act --> HTTP[Remote session API]
    HTTP --> Remote[Remote agent Session]
    Act --> Events[subagent_* on parent]""",
        "walk": [
            "The parent starts a remote session through an Activity.",
            "Operation calls become HTTP turns against that session.",
            "The Activity streams or polls events until the operation completes.",
            "The parent emits linked subagent events for local observers.",
        ],
        "code": '''@activity.defn
async def remote_subagent_call(base_url: str, session_id: str, message: str) -> str:
    # HTTP client to remote session API — runs in Activity only.
    ...
    return reply_text''',
        "impl": (
            "### Durability\n\n"
            "The Activity must be restart-safe: resume streaming from a cursor, or reconcile "
            "with remote status on retry.\n\n"
            "### Trust boundary\n\n"
            "Authenticate to the remote API; do not embed long-lived secrets in Workflow history."
        ),
        "when": (
            "Use when the child must run in another cluster, language, or scaling domain.\n"
            "Prefer local Child Workflows when both agents share a Temporal namespace."
        ),
        "benefits": (
            "You compose across deployment boundaries.\n"
            "You take on distributed failure modes and schema drift between sides."
        ),
        "table": (
            "| Approach | Location | Coupling |\n"
            "| :--- | :--- | :--- |\n"
            "| Remote Subagent | Other cluster | HTTP protocol |\n"
            "| Local subagent | Same Temporal | Child Workflow |\n"
            "| Ad-hoc webhook | Other cluster | Weak semantics |"
        ),
        "practices": [
            "**Mirror IDs.** Parent events should include remote session_id.",
            "**Timeouts on both sides.** Avoid eternal Activities.",
            "**Version the session API.** Breaking changes need explicit migration.",
        ],
        "pitfalls": [
            "**Calling HTTP from the Workflow.**",
            "**Losing cursor on Activity retry and double-sending messages.**",
        ],
        "related": [
            "[Subagent Toolset](/subagent-toolset)",
            "[HTTP Channel Agent](/http-channel-agent)",
            "[HTTP and Client](/http-and-client)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "tools-only-sandbox": {
        "title": "Tools-Only Sandbox",
        "icon": "parallel-execution-icon.svg",
        "overview": (
            "The Tools-Only Sandbox pattern runs model-authored scripts in a locked-down sandbox "
            "where the only side effects are calls to host tools.\n"
            "No direct filesystem or network; all real actions flow through Activity tools and "
            "their approval policies.\n"
            "Primitives used: SandboxProfile `tools_only`, ScriptExecution, host ToolCallSteps."
        ),
        "problem": (
            "Giving a model a general code interpreter with network access bypasses tool approvals "
            "and safety profiles."
        ),
        "solution": (
            "Configure the sandbox so imports and syscalls cannot reach the network or host FS.\n"
            "Expose only async host functions that dispatch back into durable tool Steps."
        ),
        "mermaid": """flowchart TB
    Script[Model script] --> Sandbox[tools_only sandbox]
    Sandbox -->|blocked| Net[Network/FS]
    Sandbox -->|allowed| Host[Host tool Activities]""",
        "walk": [
            "The Code Mode Step selects the tools_only profile.",
            "The script runs with host function stubs only.",
            "Any real IO is a host tool Activity with events and approvals.",
            "Direct network or filesystem use fails inside the sandbox.",
        ],
        "code": '''# Pseudocode profile
SANDBOX_PROFILES = {
    "tools_only": {
        "allow_network": False,
        "allow_filesystem": False,
        "host_tools": ["search", "book"],
    }
}''',
        "impl": (
            "### Separating compute_only\n\n"
            "Use `compute_only` when the script must not call host tools either "
            "(pure calculation).\n\n"
            "### Enforcement\n\n"
            "Enforcement belongs in the sandbox runtime, not in prompt instructions alone."
        ),
        "when": (
            "Use tools_only for Code Mode in production.\n"
            "Use richer profiles only in controlled development environments."
        ),
        "benefits": (
            "You keep approval and observability on the real side effects.\n"
            "You must maintain a capable sandbox implementation."
        ),
        "table": (
            "| Profile | Host tools | Network |\n"
            "| :--- | :--- | :--- |\n"
            "| tools_only | Yes | No |\n"
            "| compute_only | No | No |\n"
            "| unrestricted | Yes | Yes |"
        ),
        "practices": [
            "**Fail closed on policy violations.**",
            "**Pass explicit allow lists of host tools into each Code Mode tool.**",
            "**Test escape attempts in CI.**",
        ],
        "pitfalls": [
            "**Relying on the model to obey sandbox rules.**",
            "**Exposing a shell host tool that reopens the network.**",
        ],
        "related": [
            "[Code Mode Orchestrator](/code-mode-orchestrator)",
            "[Type-Checked Scripts](/type-checked-scripts)",
            "[Network & Resource Sandboxing](/network-resource-sandboxing)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "type-checked-scripts": {
        "title": "Type-Checked Scripts",
        "icon": "non-retryable-errors-icon.svg",
        "overview": (
            "The Type-Checked Scripts pattern generates type stubs from ToolDefinitions and checks "
            "model-authored scripts against them before execution.\n"
            "Scripts that call tools with wrong arguments or shapes fail fast with clear errors "
            "instead of running partial workflows.\n"
            "Primitives used: ScriptDefinition, ToolDefinition schemas, pre-exec validation Step."
        ),
        "problem": (
            "Invalid scripts can call tools halfway, leave partial side effects, or waste a Turn "
            "on avoidable mistakes."
        ),
        "solution": (
            "Before sandbox execution, generate stubs from tool input/output schemas and run a "
            "static check.\n"
            "On failure, return errors to the model or operator without executing host calls."
        ),
        "mermaid": """flowchart LR
    Script --> Check[Type check vs stubs]
    Check -->|ok| Run[Sandbox run]
    Check -->|fail| Err[Error to model]
    Run --> Host[Host tool Steps]""",
        "walk": [
            "ToolDefinitions produce type stubs for host functions.",
            "The script is checked before any host call.",
            "Failures short-circuit with actionable diagnostics.",
            "Passing scripts proceed to tools_only execution.",
        ],
        "code": '''# Structural sketch
stubs = generate_stubs(tool_definitions)
errors = typecheck(script_text, stubs)
if errors:
    return {"ok": False, "errors": errors}
return run_in_sandbox(script_text, host_dispatcher)''',
        "impl": (
            "### Where it runs\n\n"
            "Validation can be an Activity Step before sandbox run, or part of the Code Mode Activity "
            "before side effects.\n"
            "Either way, emit events that distinguish check failure from host tool failure."
        ),
        "when": (
            "Use whenever Code Mode is enabled.\n"
            "Skipping checks is acceptable only in throwaway experiments."
        ),
        "benefits": (
            "You prevent many partial side-effect runs.\n"
            "Stub generation must stay in sync with tool schemas."
        ),
        "table": (
            "| Approach | Catches bad args | Side effects before fail |\n"
            "| :--- | :--- | :--- |\n"
            "| Type-Checked Scripts | Early | No |\n"
            "| Runtime tool errors only | Late | Possible |\n"
            "| Prompt-only instructions | Weak | Possible |"
        ),
        "practices": [
            "**Regenerate stubs when tools change.**",
            "**Return model-readable errors.**",
            "**Do not execute host calls during check.**",
        ],
        "pitfalls": [
            "**Checking a different script than you execute.**",
            "**Allowing dynamic getattr to bypass stubs.**",
        ],
        "related": [
            "[Code Mode Orchestrator](/code-mode-orchestrator)",
            "[Tools-Only Sandbox](/tools-only-sandbox)",
            "[Tools and Operations](/tools-and-operations)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "script-fan-out": {
        "title": "Script Fan-Out",
        "icon": "fanout-child-workflows-icon.svg",
        "overview": (
            "The Script Fan-Out pattern lets a single script coordinate subagents and tools "
            "concurrently, turning many one-by-one calls into a tree of concurrent invocations.\n"
            "Temporal still governs each call’s retries, approvals, and observability.\n"
            "Primitives used: SandboxScriptStep, concurrent host ToolCalls, optional subagent tools."
        ),
        "problem": (
            "Sequential tool loops make multi-item work slow and token-heavy even when items are independent."
        ),
        "solution": (
            "In Code Mode, allow `asyncio.gather` (or equivalent) over host tool calls and subagent "
            "operations.\n"
            "Each concurrent call remains its own durable Step."
        ),
        "mermaid": """flowchart TB
    Script --> G[gather]
    G --> T1[Tool A]
    G --> T2[Tool B]
    G --> S1[Subagent]""",
        "walk": [
            "The model writes a script that fans out independent calls.",
            "The sandbox schedules host calls concurrently.",
            "Each call is an Activity/subagent Step with its own policy.",
            "The script joins results and optionally continues.",
        ],
        "code": '''# Model-authored script shape
async def main():
    a, b = await asyncio.gather(
        search({"q": "alpha"}),
        search({"q": "beta"}),
    )
    return {"a": a, "b": b}''',
        "impl": (
            "### Limits\n\n"
            "Enforce max concurrent host calls per script and per session.\n\n"
            "### Ordering\n\n"
            "Do not assume completion order; join explicitly in the script."
        ),
        "when": (
            "Use when items are independent and latency matters.\n"
            "Stay sequential when later calls need earlier results."
        ),
        "benefits": (
            "You cut wall-clock time for embarrassingly parallel tool work.\n"
            "You increase burst load on downstream systems."
        ),
        "table": (
            "| Approach | Parallelism | Control flow |\n"
            "| :--- | :--- | :--- |\n"
            "| Script Fan-Out | High | In script |\n"
            "| Sequential tool loop | Low | Model turns |\n"
            "| Fan-Out Subagents | High | Child sessions |"
        ),
        "practices": [
            "**Cap concurrency.** Protect dependencies.",
            "**Keep gather sets independent.** Avoid hidden shared mutable state.",
            "**Surface partial failures.** Decide all-or-nothing vs best-effort.",
        ],
        "pitfalls": [
            "**Fan-out of non-idempotent tools without keys.**",
            "**Unbounded gather over huge lists.**",
        ],
        "related": [
            "[Code Mode Orchestrator](/code-mode-orchestrator)",
            "[Fan-Out Subagents](/fanout-subagents)",
            "[Tools-Only Sandbox](/tools-only-sandbox)",
        ],
        "refs": [
            "[Temporal Docs: Activity concurrent execution](https://docs.temporal.io/activities)",
        ],
    },
    "safety-profiled-tools": {
        "title": "Safety-Profiled Tools",
        "icon": "saga-icon.svg",
        "overview": (
            "The Safety-Profiled Tools pattern labels each tool with a safety profile "
            "(`inherently_safe`, `idempotent_side_effect`, `non_idempotent`) and enforces matching policies.\n"
            "The runtime blocks or gates calls that do not match their expected profile and environment.\n"
            "Primitives used: SafetyProfile on ToolDefinition, build/startup validation, ApprovalPolicy defaults."
        ),
        "problem": (
            "Without labels, every tool looks the same to retries and approvals, so policy engines guess wrong."
        ),
        "solution": (
            "Require a SafetyProfile on every ToolDefinition.\n"
            "At build or worker start, fail if a mutating tool lacks a profile or if profile and "
            "retry settings contradict.\n"
            "At runtime, ApprovalPolicy and StepPolicy read the label."
        ),
        "mermaid": """flowchart TD
    Def[ToolDefinition] --> Label[SafetyProfile]
    Label --> Build[Validate at build]
    Label --> Runtime[Approvals and retries]""",
        "walk": [
            "Authors declare a safety profile next to each tool.",
            "Startup validation rejects missing or contradictory configs.",
            "Runtime policies use the label to gate or retry.",
            "Events can include the profile for audits.",
        ],
        "code": '''TOOLS = {
    "search": {"safety": "inherently_safe"},
    "charge": {"safety": "non_idempotent", "idempotency_key_field": "key"},
}

def assert_profiles(tools: dict) -> None:
    for name, meta in tools.items():
        if "safety" not in meta:
            raise ValueError(f"{name} missing safety profile")''',
        "impl": (
            "### Defaults\n\n"
            "Prefer safe-by-default: unknown tools are treated as non_idempotent and gated.\n\n"
            "### Documentation\n\n"
            "Pattern pages and tool READMEs should state the profile next to the schema."
        ),
        "when": (
            "Use for every multi-tool agent.\n"
            "Skip only for prototypes with a single read-only tool."
        ),
        "benefits": (
            "You make policy mechanical instead of prompt-based.\n"
            "Authors must classify tools honestly."
        ),
        "table": (
            "| Profile | Meaning |\n"
            "| :--- | :--- |\n"
            "| inherently_safe | Read-only / pure |\n"
            "| idempotent_side_effect | Safe to retry with key |\n"
            "| non_idempotent | Do not auto-retry |"
        ),
        "practices": [
            "**Fail build on missing labels.**",
            "**Pair non_idempotent with approvals or keys.**",
            "**Re-review profiles when tool behavior changes.**",
        ],
        "pitfalls": [
            "**Marking writes as inherently_safe.**",
            "**Profile only in comments, not enforced config.**",
        ],
        "related": [
            "[Tool Retry Profiles](/tool-retry-profiles)",
            "[Approval-Gated Tools](/approval-gated-tools)",
            "[Security Profiles per Agent](/security-profiles-per-agent)",
        ],
        "refs": [
            "[Temporal Docs: Retry policies](https://docs.temporal.io/encyclopedia/retry-policies)",
        ],
    },
    "security-profiles-per-agent": {
        "title": "Security Profiles per Agent",
        "icon": "priority-task-queues-icon.svg",
        "overview": (
            "The Security Profiles per Agent pattern defines security profiles (development, staging, "
            "production) that control which tools, sandboxes, and networks are available to an agent.\n"
            "Profiles are declared alongside the agent and validated at build time.\n"
            "Primitives used: SecurityProfile, tool allow/deny lists, SandboxProfile binding."
        ),
        "problem": (
            "The same agent code often runs in dev with loose tools and in prod with strict ones.\n"
            "If the difference is only environment folklore, production can accidentally enable dangerous tools."
        ),
        "solution": (
            "Declare a SecurityProfile next to the agent (for example allow lists, sandbox profile, "
            "channel auth requirements).\n"
            "Select the active profile via deployment config and validate that every enabled tool "
            "is permitted."
        ),
        "mermaid": """flowchart TD
    Agent[Agent project] --> Profiles[dev / staging / prod]
    Profiles --> Validate[Build validation]
    Validate --> Worker[Worker runtime]""",
        "walk": [
            "Authors maintain named security profiles with the agent.",
            "Deployment selects prod/staging/dev.",
            "Build or startup validates tool and sandbox permissions.",
            "Runtime refuses tools outside the active profile.",
        ],
        "code": '''PROFILES = {
    "prod": {"tools": ["search"], "sandbox": "tools_only"},
    "dev": {"tools": ["search", "shell"], "sandbox": "tools_only"},
}

active = PROFILES[os.environ["AGENT_SECURITY_PROFILE"]]
assert set(registered_tools) <= set(active["tools"])''',
        "impl": (
            "### Separation from SafetyProfile\n\n"
            "SafetyProfile is per tool; SecurityProfile is per agent/environment.\n"
            "Both must pass before a call runs."
        ),
        "when": (
            "Use whenever an agent has more than one deployment environment.\n"
            "A single locked profile is enough for a prod-only private agent."
        ),
        "benefits": (
            "You prevent environment drift with validation.\n"
            "You maintain profile matrices as tools grow."
        ),
        "table": (
            "| Control | Scope |\n"
            "| :--- | :--- |\n"
            "| SafetyProfile | Per tool |\n"
            "| SecurityProfile | Per agent/env |\n"
            "| ApprovalPolicy | Per session/runtime |"
        ),
        "practices": [
            "**Fail closed in prod.** Missing profile aborts startup.",
            "**Diff profiles in CI.** Catch accidental widenings.",
            "**Require auth on prod channels.**",
        ],
        "pitfalls": [
            "**Copying dev profile to prod.**",
            "**Allowing shell tools in prod security profiles.**",
        ],
        "related": [
            "[Safety-Profiled Tools](/safety-profiled-tools)",
            "[Network & Resource Sandboxing](/network-resource-sandboxing)",
            "[Filesystem Authoring](/filesystem-authoring)",
        ],
        "refs": [
            "[Temporal Docs: Workers](https://docs.temporal.io/workers)",
        ],
    },
    "network-resource-sandboxing": {
        "title": "Network & Resource Sandboxing",
        "icon": "downstream-rate-limiting-icon.svg",
        "overview": (
            "The Network & Resource Sandboxing pattern uses sandbox backends (containers, "
            "microsandboxes, restricted Python) to enforce network, filesystem, and resource "
            "limits for model-authored code and tools.\n"
            "The Workflow is the control plane; sandboxes are bounded data planes.\n"
            "Primitives used: SandboxProfile limits, ScriptExecution isolation, Activity-hosted sandboxes."
        ),
        "problem": (
            "Model-authored code and some tools can exhaust CPU, memory, or reach unexpected networks "
            "if they share the worker's privileges."
        ),
        "solution": (
            "Run untrusted execution inside a sandbox Activity with explicit CPU, memory, time, "
            "import, and egress controls.\n"
            "The Session Workflow only schedules and awaits those Activities."
        ),
        "mermaid": """flowchart LR
    Workflow[Session Workflow] -->|schedule| Act[Sandbox Activity]
    Act --> Box[Bounded sandbox]
    Box -->|host tools only| Tools[Tool Activities]""",
        "walk": [
            "The Turn needs Code Mode or an untrusted tool.",
            "An Activity starts a sandbox with the selected profile limits.",
            "The script or tool runs inside the box.",
            "Host tool calls leave the box through controlled callbacks to Activities.",
        ],
        "code": '''@activity.defn
async def run_sandboxed(script: str, profile: str) -> str:
    # Enforce time/memory/network from profile inside this Activity.
    return execute_restricted(script, profile)''',
        "impl": (
            "### Control vs data plane\n\n"
            "Never run untrusted code inside the Workflow process.\n"
            "Keep credentials on the trusted worker side and broker them only at tool boundaries."
        ),
        "when": (
            "Use for Code Mode and any tool that executes model-influenced code.\n"
            "Trusted pure Activity tools may run without a nested sandbox if the worker is already locked down."
        ),
        "benefits": (
            "You contain blast radius for untrusted execution.\n"
            "You operate another moving part (sandbox backend)."
        ),
        "table": (
            "| Layer | Responsibility |\n"
            "| :--- | :--- |\n"
            "| Workflow | Schedule, wait, approvals |\n"
            "| Sandbox Activity | Isolate untrusted code |\n"
            "| Host tool Activities | Real side effects |"
        ),
        "practices": [
            "**Set hard timeouts and memory caps.**",
            "**Deny egress by default.**",
            "**Separate sandbox images from worker images when possible.**",
        ],
        "pitfalls": [
            "**Running Code Mode in-process with the Workflow worker.**",
            "**Passing broad credentials into the sandbox environment.**",
        ],
        "related": [
            "[Tools-Only Sandbox](/tools-only-sandbox)",
            "[Code Mode Orchestrator](/code-mode-orchestrator)",
            "[Security Profiles per Agent](/security-profiles-per-agent)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "session-memory": {
        "title": "Session Memory",
        "icon": "event-accumulator-icon.svg",
        "overview": (
            "The Session Memory pattern stores summary or vectorized memory in session state, "
            "updated at safe points between turns.\n"
            "The agent reads this durable memory before each new turn to preserve context across "
            "long conversations or jobs.\n"
            "Primitives used: Session state, Turn boundaries, Continue-As-New snapshots."
        ),
        "problem": (
            "Relying only on the raw event transcript makes prompts huge and history heavy.\n"
            "Process memory disappears on worker restart."
        ),
        "solution": (
            "Keep a compact memory document on the Session Workflow.\n"
            "Update it after turns complete (or via a memory tool Activity), and pass it into the "
            "next Durable Model Call.\n"
            "Include memory in Continue-As-New snapshots."
        ),
        "mermaid": """flowchart LR
    Turn --> Update[Update memory]
    Update --> State[Session memory]
    State --> Next[Next Turn prompt]""",
        "walk": [
            "A Turn completes with new facts.",
            "The Session updates a summary memory structure.",
            "The next Turn reads memory before calling the model.",
            "Continue-As-New carries memory forward.",
        ],
        "code": '''self._memory = {"summary": "...", "facts": []}

# after turn
self._memory = await workflow.execute_activity(
    compact_memory,
    args=[self._memory, turn_transcript],
    start_to_close_timeout=timedelta(seconds=60),
)''',
        "impl": (
            "### Safe points\n\n"
            "Prefer updating memory between turns, not mid-tool, so partial failures do not corrupt it.\n\n"
            "### Size\n\n"
            "If memory grows large, externalize blobs and keep pointers in Session state "
            "(see Externalized Memory)."
        ),
        "when": (
            "Use for multi-turn agents that must remember decisions.\n"
            "Skip for single-turn request/response agents."
        ),
        "benefits": (
            "You preserve context without replaying entire histories into the model.\n"
            "Summaries can drop detail—design refresh paths."
        ),
        "table": (
            "| Store | Durability | Size |\n"
            "| :--- | :--- | :--- |\n"
            "| Session memory | High | Bounded |\n"
            "| Full transcript only | High | Grows fast |\n"
            "| Process RAM | None | Fast |"
        ),
        "practices": [
            "**Version memory schemas.**",
            "**Record memory updates as events when material.**",
            "**Do not put secrets in memory summaries.**",
        ],
        "pitfalls": [
            "**Unbounded append-only notes in Workflow state.**",
            "**Updating memory inside failed turns without rollback rules.**",
        ],
        "related": [
            "[Cross-Session Memory](/cross-session-memory)",
            "[Externalized Memory](/externalized-memory)",
            "[Continue-As-New Session](/continue-as-new-session)",
        ],
        "refs": [
            "[Temporal Docs: Continue-As-New](https://docs.temporal.io/workflow-execution/continue-as-new)",
        ],
    },
    "cross-session-memory": {
        "title": "Cross-Session Memory",
        "icon": "batch-iterator-icon.svg",
        "overview": (
            "The Cross-Session Memory pattern shares bounded, structured memory across sessions "
            "(for example per-user or per-team knowledge), while each session retains its own "
            "local context and approvals.\n"
            "Access is always mediated by the agent’s tools and policies.\n"
            "Primitives used: External memory tools, Session Memory composition, Safety/Approval on writes."
        ),
        "problem": (
            "Some knowledge should outlive a single session, but writing it ad hoc from Activities "
            "without policy creates silent cross-talk and tenancy bugs."
        ),
        "solution": (
            "Provide explicit memory tools (read/write) backed by Activities.\n"
            "Sessions pull relevant slices into Session Memory at turn start and write back only "
            "through those tools under approval rules."
        ),
        "mermaid": """flowchart TB
    S1[Session A] -->|memory tool| Store[Shared store]
    S2[Session B] -->|memory tool| Store
    S1 --> Local1[Session memory]
    S2 --> Local2[Session memory]""",
        "walk": [
            "A Session loads shared memory via a tool Activity.",
            "It merges a bounded slice into local Session Memory.",
            "Writes go back through a gated memory tool.",
            "Other sessions see updates only through the same tools.",
        ],
        "code": '''shared = await workflow.execute_activity(
    memory_read,
    args=[user_id, "preferences"],
    start_to_close_timeout=timedelta(seconds=30),
)
self._memory["shared"] = shared''',
        "impl": (
            "### Tenancy\n\n"
            "Keys must include tenant/user/team IDs.\n"
            "Tools enforce authorization using worker-side identity, not model claims alone."
        ),
        "when": (
            "Use for preferences, org knowledge, or long-term facts.\n"
            "Keep purely conversational scratch state in Session Memory only."
        ),
        "benefits": (
            "You share knowledge without merging sessions.\n"
            "You must operate a store and write policies."
        ),
        "table": (
            "| Memory | Lifetime | Sharing |\n"
            "| :--- | :--- | :--- |\n"
            "| Session | One session | No |\n"
            "| Cross-Session | Across sessions | Yes, mediated |\n"
            "| Externalized index | Long | Via tools |"
        ),
        "practices": [
            "**Gate writes.** Shared memory is a side effect.",
            "**Bound payloads.** Prefer structured records over free-text dumps.",
            "**Audit reads/writes in the event stream.**",
        ],
        "pitfalls": [
            "**Letting the model invent store keys that cross tenants.**",
            "**Writing shared memory from Workflow code without an Activity.**",
        ],
        "related": [
            "[Session Memory](/session-memory)",
            "[Externalized Memory](/externalized-memory)",
            "[Approval-Gated Tools](/approval-gated-tools)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "externalized-memory": {
        "title": "Externalized Memory",
        "icon": "mapreduce-tree-icon.svg",
        "overview": (
            "The Externalized Memory pattern pushes large or specialized memory (search indexes, "
            "logs, vector stores) behind tools and Activities.\n"
            "The agent never mutates external memory in-place without going through a durable, "
            "approval-aware tool call.\n"
            "Primitives used: Activity Tools for memory IO, Session pointers, evented tool calls."
        ),
        "problem": (
            "Vector indexes and large corpora do not fit in Workflow state.\n"
            "Direct SDK access from random code paths skips retries and approvals."
        ),
        "solution": (
            "Expose `memory_search`, `memory_upsert`, and similar as Activity tools.\n"
            "Session state holds only handles, cursors, and small summaries."
        ),
        "mermaid": """flowchart LR
    Session -->|pointer| Tool[Memory Activity tool]
    Tool --> Index[Vector/DB index]
    Tool --> Events[tool_call events]""",
        "walk": [
            "The Turn needs large-context retrieval or storage.",
            "It calls a memory tool Activity with a schema-validated query or record.",
            "The Activity talks to the external index.",
            "The Session stores only the returned IDs or snippets it needs.",
        ],
        "code": '''hits = await workflow.execute_activity(
    memory_search,
    args=[collection, query, 5],
    start_to_close_timeout=timedelta(seconds=30),
)
self._memory["last_hits"] = [h["id"] for h in hits]''',
        "impl": (
            "### Approvals\n\n"
            "Treat upserts/deletes as non-idempotent or idempotent_side_effect with keys.\n\n"
            "### Replay\n\n"
            "Completed retrievals replay from Activity results; do not re-query inside the Workflow."
        ),
        "when": (
            "Use for search indexes, document stores, and bulky artifacts.\n"
            "Keep tiny summaries in Session Memory."
        ),
        "benefits": (
            "You scale memory beyond Workflow limits with durable calls.\n"
            "External systems add their own failure modes."
        ),
        "table": (
            "| Store location | Fits Workflow history | Policy surface |\n"
            "| :--- | :--- | :--- |\n"
            "| Externalized via tools | No need | Tool profiles |\n"
            "| Inline Session state | Only if small | Limited |\n"
            "| Hidden global client | Risky | None |"
        ),
        "practices": [
            "**Return IDs + short snippets.**",
            "**Idempotency keys on upserts.**",
            "**Redact sensitive hits in events.**",
        ],
        "pitfalls": [
            "**Embedding full documents in Activity results forever.**",
            "**Bypassing tools with a shared singleton client in Workflow imports.**",
        ],
        "related": [
            "[Session Memory](/session-memory)",
            "[Activity Tool](/activity-tool)",
            "[Safety-Profiled Tools](/safety-profiled-tools)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "agent-tracing": {
        "title": "Agent Tracing",
        "icon": "retry-metrics-icon.svg",
        "overview": (
            "The Agent Tracing pattern wraps model calls, tools, and subagents with OpenTelemetry "
            "spans that carry session, turn, step, and tool IDs.\n"
            "Temporal search attributes mirror these IDs so operators can jump between traces, "
            "logs, and Workflow histories.\n"
            "Primitives used: Identity IDs, OTel spans, Temporal search attributes."
        ),
        "problem": (
            "Without correlated IDs, a failed tool in logs cannot be found in Temporal Web or the "
            "session UI."
        ),
        "solution": (
            "Propagate `session_id`, `turn_id`, `step_id`, `agent_id`, and `tool_id` into span "
            "attributes and search attributes.\n"
            "Create spans around model Activities, tool Activities, and subagent operations."
        ),
        "mermaid": """flowchart LR
    IDs[session/turn/step IDs] --> OTel[OTel spans]
    IDs --> SA[Search attributes]
    IDs --> UI[Session UI]""",
        "walk": [
            "Each Turn allocates IDs for its Steps.",
            "Activities set span attributes from those IDs.",
            "Workflow upserts search attributes for session status.",
            "Operators pivot from UI → Temporal → traces using the same IDs.",
        ],
        "code": '''# Activity side
with tracer.start_as_current_span("tool_call") as span:
    span.set_attribute("session_id", session_id)
    span.set_attribute("turn_id", turn_id)
    span.set_attribute("tool_id", tool_id)
    return await invoke_tool(...)''',
        "impl": (
            "### Workflow vs Activity instrumentation\n\n"
            "Prefer heavy instrumentation in Activities.\n"
            "Workflows should stay deterministic; use upsert_search_attributes for queryable fields."
        ),
        "when": (
            "Use for any production agent.\n"
            "Omit only in local teaching samples."
        ),
        "benefits": (
            "You debug across systems with one ID space.\n"
            "You must keep attribute schemas consistent."
        ),
        "table": (
            "| Signal | System |\n"
            "| :--- | :--- |\n"
            "| Event stream | Product UI |\n"
            "| Search attributes | Temporal visibility |\n"
            "| OTel spans | APM |"
        ),
        "practices": [
            "**One ID vocabulary everywhere.**",
            "**Sample carefully.** High-cardinality labels need care.",
            "**Link parent/child spans for subagents.**",
        ],
        "pitfalls": [
            "**New random IDs in each Activity retry.** Use Workflow-supplied step IDs.",
            "**PII in span attributes.**",
        ],
        "related": [
            "[Standardized Event Stream](/standardized-event-stream)",
            "[Identity](/identity)",
            "[Cost & Token Accounting](/cost-token-accounting)",
        ],
        "refs": [
            "[Temporal Docs: Visibility](https://docs.temporal.io/visibility)",
        ],
    },
    "cost-token-accounting": {
        "title": "Cost & Token Accounting",
        "icon": "retry-metrics-icon.svg",
        "overview": (
            "The Cost & Token Accounting pattern aggregates token usage and cost per model call, "
            "per turn, and per session, and emits them as events and metrics.\n"
            "Use it to identify expensive agents, tools, or prompts.\n"
            "Primitives used: token_usage_reported events, Durable Model Call outputs, metrics."
        ),
        "problem": (
            "Without per-call usage on the event stream, finance and engineering cannot attribute "
            "spend to sessions or features."
        ),
        "solution": (
            "Require Durable Model Call Activities to return usage.\n"
            "Emit `token_usage_reported` and roll up counters on the Session.\n"
            "Export metrics labeled by `agent_id` and model name."
        ),
        "mermaid": """flowchart LR
    Model[Model Activity] --> Usage[usage payload]
    Usage --> Event[token_usage_reported]
    Usage --> Rollup[Session totals]
    Rollup --> Metrics[Metrics export]""",
        "walk": [
            "A model Activity returns token counts (and optional cost).",
            "The Turn emits a usage event.",
            "The Session increments totals.",
            "Dashboards aggregate by agent, model, and session.",
        ],
        "code": '''usage = result["usage"]
self._tokens_in += usage["input"]
self._tokens_out += usage["output"]
events.append({
    "type": "token_usage_reported",
    "turn_id": turn_id,
    "usage": usage,
})''',
        "impl": (
            "### Cost calculation\n\n"
            "Prefer recording raw tokens in events and applying price tables in analytics, "
            "unless the provider returns cost directly.\n\n"
            "### Tool costs\n\n"
            "Extend the same pattern for billable tools when applicable."
        ),
        "when": (
            "Use whenever model calls are in the critical path of production agents.\n"
            "Teaching stubs may omit real usage fields."
        ),
        "benefits": (
            "You see expensive turns before invoices surprise you.\n"
            "You must keep price tables and model names accurate."
        ),
        "table": (
            "| Grain | Question answered |\n"
            "| :--- | :--- |\n"
            "| Call | Which prompt blew up? |\n"
            "| Turn | Which user message was costly? |\n"
            "| Session | Which conversation should we cap? |"
        ),
        "practices": [
            "**Always bind usage to turn_id and session_id.**",
            "**Alert on session budgets.**",
            "**Include model name in events.**",
        ],
        "pitfalls": [
            "**Counting only successful calls.** Failed calls still cost money.",
            "**Aggregating only in logs without session rollups.**",
        ],
        "related": [
            "[Durable Model Call](/durable-model-call)",
            "[Standardized Event Stream](/standardized-event-stream)",
            "[Agent Tracing](/agent-tracing)",
        ],
        "refs": [
            "[Temporal Docs: Metrics](https://docs.temporal.io/production-deployment/metrics)",
        ],
    },
    "eval-backed-behavior-checks": {
        "title": "Eval-Backed Behavior Checks",
        "icon": "fixed-wall-time-retries-icon.svg",
        "overview": (
            "The Eval-Backed Behavior Checks pattern runs model-backed or rule-backed evals against "
            "recorded sessions or synthetic scenarios.\n"
            "Evals look for regressions (unsafe actions, wrong answers, missing approvals) and "
            "integrate with CI/CD as part of agent rollout.\n"
            "Primitives used: recorded Event Stream, eval suite under `evals/`, CI gates."
        ),
        "problem": (
            "Agents change behavior when prompts, tools, or models change.\n"
            "Unit tests alone cannot catch missing approvals or unsafe tool use."
        ),
        "solution": (
            "Keep scenario fixtures and scorers next to the agent.\n"
            "Replay or simulate sessions, score the event stream, and fail the build on regressions."
        ),
        "mermaid": """flowchart LR
    Fixtures[Scenarios] --> Run[Session run or replay]
    Run --> Stream[Event stream]
    Stream --> Score[Eval scorers]
    Score --> CI[CI gate]""",
        "walk": [
            "Authors add scenarios that expect approvals, refusals, or answers.",
            "CI runs the agent (often with stub models) or replays recorded streams.",
            "Scorers inspect events for required patterns.",
            "Failures block rollout.",
        ],
        "code": '''def test_payment_requires_approval(events):
    assert any(e["type"] == "approval_requested" for e in events)
    assert not any(
        e["type"] == "tool_call_completed" and e["tool_id"] == "charge"
        for e in events
        if not approval_granted_before(e, events)
    )''',
        "impl": (
            "### Stub models\n\n"
            "Prefer deterministic stub models in CI for speed and stability; run a smaller suite "
            "against live models nightly if needed.\n\n"
            "### Event-first scoring\n\n"
            "Score the Standardized Event Stream so evals stay UI-agnostic."
        ),
        "when": (
            "Use before promoting agent changes that touch tools, policies, or prompts.\n"
            "Skip only for experimental spikes that never ship."
        ),
        "benefits": (
            "You catch safety regressions early.\n"
            "You maintain fixtures as product behavior evolves."
        ),
        "table": (
            "| Check type | Strength |\n"
            "| :--- | :--- |\n"
            "| Event rule scorers | Stable, fast |\n"
            "| Model-as-judge | Flexible, flaky |\n"
            "| Manual QA only | Slow |"
        ),
        "practices": [
            "**Assert approvals for dangerous tools.**",
            "**Keep golden event sequences small and focused.**",
            "**Version fixtures with tool schema changes.**",
        ],
        "pitfalls": [
            "**Scoring free-text only.** Prefer events.",
            "**Live-model CI without flake budgets.**",
        ],
        "related": [
            "[Standardized Event Stream](/standardized-event-stream)",
            "[Approval-Gated Tools](/approval-gated-tools)",
            "[Filesystem Authoring](/filesystem-authoring)",
        ],
        "refs": [
            "[Temporal Docs: Testing](https://docs.temporal.io/develop/testing-suite)",
        ],
    },
    "http-channel-agent": {
        "title": "HTTP Channel Agent",
        "icon": "webhooks-icon.svg",
        "overview": (
            "The HTTP Channel Agent pattern exposes an agent as an HTTP session API.\n"
            "Clients create sessions, send messages, and stream events over NDJSON or SSE, while "
            "agent logic stays in Workflows and Activities.\n"
            "Primitives used: SessionDescriptor, MessageRequest/Response, EventStream, Session Workflow."
        ),
        "problem": (
            "If HTTP handlers embed agent loops, you lose durability and duplicate protocol logic "
            "per service."
        ),
        "solution": (
            "HTTP only translates to Temporal signals/starts and streams the session event log.\n"
            "The Session Workflow owns turns and tools."
        ),
        "mermaid": """flowchart LR
    Client --> HTTP[Session HTTP API]
    HTTP --> Temporal[Start/Signal Session]
    Temporal --> Session[Session Workflow]
    Session --> Stream[SSE/NDJSON events]
    Stream --> Client""",
        "walk": [
            "Client creates a session and receives session_id.",
            "Client posts a message; API signal-with-starts the Session.",
            "The Session runs Turns and appends events.",
            "Client reads events until turn_ended.",
        ],
        "code": '''# API handler sketch
async def post_message(session_id: str, text: str):
    await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id],
        id=session_id,
        task_queue=TASK_QUEUE,
        start_signal="user_message",
        start_signal_args=[text],
    )''',
        "impl": (
            "### AuthN/Z\n\n"
            "Protect create/message/stream routes; authorize per session.\n\n"
            "### Streaming\n\n"
            "Support cursors so clients reconnect without losing events."
        ),
        "when": (
            "Use as the default integration surface for web and service clients.\n"
            "Pair with messaging channels for Slack/email frontends."
        ),
        "benefits": (
            "You keep HTTP thin and agents durable.\n"
            "You must operate an API tier in front of Temporal."
        ),
        "table": (
            "| Layer | Responsibility |\n"
            "| :--- | :--- |\n"
            "| HTTP API | Auth, session IO, SSE |\n"
            "| Session Workflow | Agent logic |\n"
            "| Activities | Model/tools |"
        ),
        "practices": [
            "**Stable session_id in responses.**",
            "**Cursored event streams.**",
            "**Do not run model SDKs in the API process.**",
        ],
        "pitfalls": [
            "**Embedding the agent loop in FastAPI handlers.**",
            "**Forgetting auth on stream endpoints.**",
        ],
        "related": [
            "[Session with Signal-and-Start](/session-signal-and-start)",
            "[HTTP and Client](/http-and-client)",
            "[Messaging Channel Agent](/messaging-channel-agent)",
        ],
        "refs": [
            "[Temporal Docs: Signal-With-Start](https://docs.temporal.io/encyclopedia/workflow-message-passing#signal-with-start)",
        ],
    },
    "messaging-channel-agent": {
        "title": "Messaging Channel Agent",
        "icon": "signal-with-start-icon.svg",
        "overview": (
            "The Messaging Channel Agent pattern binds an agent to messaging platforms "
            "(Slack, Teams, email) by mapping incoming messages to Session/Turn inputs and "
            "outgoing replies to channel-specific payloads.\n"
            "Durable timers and retries shield the channel from transient failures.\n"
            "Primitives used: Channel adapter Activities/workers, Session with Signal-and-Start, Event Stream."
        ),
        "problem": (
            "Chat platforms retry webhooks, reorder events, and rate-limit replies.\n"
            "A naive bot process loses sessions on deploy."
        ),
        "solution": (
            "Channel workers verify signatures, derive `session_id`, and signal-with-start the "
            "Session.\n"
            "Outbound replies are Activities with retries; the Session remains channel-agnostic."
        ),
        "mermaid": """flowchart LR
    Slack[Slack/email] --> Adapter[Channel worker]
    Adapter --> Session[Session Workflow]
    Session --> ReplyAct[Reply Activity]
    ReplyAct --> Slack""",
        "walk": [
            "A platform webhook hits the channel adapter.",
            "The adapter maps thread/user to session_id and signals the Session.",
            "The Session runs the Turn and emits events.",
            "A reply Activity posts back to the platform with retries.",
        ],
        "code": '''async def on_slack_message(team: str, channel: str, thread: str, text: str):
    session_id = f"slack:{team}:{channel}:{thread}"
    await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id],
        id=session_id,
        task_queue=TASK_QUEUE,
        start_signal="user_message",
        start_signal_args=[text],
    )''',
        "impl": (
            "### Idempotency\n\n"
            "Deduplicate platform event IDs before signaling.\n\n"
            "### Typing indicators and slash commands\n\n"
            "Map operator commands to Session Signals; keep user chat as ordinary turns."
        ),
        "when": (
            "Use for human chat surfaces.\n"
            "Use HTTP Channel Agent for first-party apps and services."
        ),
        "benefits": (
            "You absorb platform quirks outside the Session.\n"
            "You maintain per-channel adapters."
        ),
        "table": (
            "| Concern | Owner |\n"
            "| :--- | :--- |\n"
            "| Signature verify | Channel adapter |\n"
            "| Agent logic | Session |\n"
            "| Send message | Reply Activity |"
        ),
        "practices": [
            "**Deterministic session IDs from thread keys.**",
            "**Retry outbound posts in Activities.**",
            "**Keep channel formatting out of core tools when possible.**",
        ],
        "pitfalls": [
            "**Using channel event timestamps as Workflow logic without side-effect APIs.**",
            "**One global Workflow for all Slack threads.**",
        ],
        "related": [
            "[HTTP Channel Agent](/http-channel-agent)",
            "[Session with Signal-and-Start](/session-signal-and-start)",
            "[Operator Slash Commands](/operator-slash-commands)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "mcp-openapi-tooling": {
        "title": "MCP / OpenAPI Tooling",
        "icon": "activity-dependency-injection-icon.svg",
        "overview": (
            "The MCP / OpenAPI Tooling pattern discovers external tools and services "
            "(via MCP servers or OpenAPI descriptions) and compiles them into typed Activity tools.\n"
            "The agent calls them as first-class tools with schemas, retries, approvals, and telemetry.\n"
            "Primitives used: ToolDefinition generation, Activity Tools, SafetyProfile assignment."
        ),
        "problem": (
            "Hand-writing Activity wrappers for every external API does not scale and drifts from "
            "the upstream schema."
        ),
        "solution": (
            "At build or startup, ingest MCP/OpenAPI descriptions, generate ToolDefinitions "
            "(JSON Schema → Pydantic), and register Activity bodies that call the remote API.\n"
            "Assign safety profiles and approval defaults during compilation."
        ),
        "mermaid": """flowchart LR
    Spec[MCP/OpenAPI] --> Compile[Compile ToolDefinitions]
    Compile --> Tools[Activity tools]
    Tools --> Agent[Agent Session]""",
        "walk": [
            "A connector spec is fetched or vendored.",
            "Compilation produces typed tools with IDs and schemas.",
            "Workers register generated Activities.",
            "The agent uses them like any other Activity Tool under policy.",
        ],
        "code": '''# Structural sketch
defs = compile_openapi(spec_path)
for d in defs:
    register_activity_tool(d.name, d.input_model, d.output_model, d.endpoint)''',
        "impl": (
            "### Freshness\n\n"
            "Pin specs in-repo or validate digests so tool IDs do not churn silently.\n\n"
            "### Auth\n\n"
            "Broker credentials in the Activity layer; never ask the model for secrets."
        ),
        "when": (
            "Use when integrating many external APIs or MCP servers.\n"
            "Hand-write tools when you need custom semantics beyond the spec."
        ),
        "benefits": (
            "You scale tool ingestion with schema fidelity.\n"
            "Generated tools still need safety review."
        ),
        "table": (
            "| Source | Output |\n"
            "| :--- | :--- |\n"
            "| OpenAPI | HTTP Activity tools |\n"
            "| MCP | ToolDefinitions from server list |\n"
            "| Hand-written | Custom tools |"
        ),
        "practices": [
            "**Review safety profiles after generation.**",
            "**Stable tool IDs.** Avoid renaming on every spec refresh.",
            "**Contract tests against the real API in CI.**",
        ],
        "pitfalls": [
            "**Auto-enabling all generated tools in prod.**",
            "**Passing raw user tokens to the model context.**",
        ],
        "related": [
            "[Activity Tool](/activity-tool)",
            "[Safety-Profiled Tools](/safety-profiled-tools)",
            "[Security Profiles per Agent](/security-profiles-per-agent)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
}


def render(slug: str, p: dict[str, str]) -> str:
    walk = "\n".join(f"{i}. {line}" for i, line in enumerate(p["walk"], 1))
    practices = "\n".join(f"- {x}" for x in p["practices"])
    pitfalls = "\n".join(f"- **{x.split('.',1)[0]}.**{x.split('.',1)[1]}" if '.' in x else f"- {x}" for x in p["pitfalls"])
    # Simpler pitfalls formatting
    pitfalls = "\n".join(f"- {x}" if x.startswith("**") else f"- {x}" for x in p["pitfalls"])
    related = "\n".join(f"- {x}" for x in p["related"])
    refs = "\n".join(f"- {x}" for x in p["refs"])
    return f"""\
<h1>{p['title']} <img src="/images/{p['icon']}" alt="{p['title']}" class="pattern-page-icon"></h1>

## Overview

{p['overview']}

## Problem

{p['problem']}

## Solution

{p['solution']}

```mermaid
{p['mermaid']}
```

The following describes each step in the diagram:

{walk}

```python
{p['code']}
```

## Implementation

{p['impl']}

## When to use

{p['when']}

## Benefits and trade-offs

{p['benefits']}

## Comparison with alternatives

{p['table']}

## Best practices

{practices}

## Common pitfalls

{pitfalls}

## Related patterns

{related}

## Sample code

See related runnable samples under `sandbox-runner/patterns/` when this pattern builds on Session Workflow, Activity Tool, or Code Mode.

## References

{refs}
"""


def main() -> None:
    for slug, page in PAGES.items():
        path = DOCS / f"{slug}.md"
        path.write_text(render(slug, page))
        print("wrote", path.name)
    print(f"expanded {len(PAGES)} pages")


if __name__ == "__main__":
    main()
