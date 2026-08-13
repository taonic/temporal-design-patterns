# Temporal Agentic Patterns

> **Warning:** This catalog is under active development. Content and structure may change.

Temporal provides durable execution primitives that you can compose into common, reusable patterns for AI agents.
This catalog is meant to be the practical DX guide for building agentic workflows on Temporal—sessions, tools, approvals, subagents, QoS, and operations—without renaming Temporal into a new framework.

## Sessions {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="session-workflow">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session Workflow">
<span>Session Workflow</span>
</div>
<p>One Workflow owns a session, memory, and event stream.</p>
</a>
</div>
<div class="pattern-tile">
<a href="turn-workflow">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Turn Workflow">
<span>Turn Workflow</span>
</div>
<p>Isolate each turn as a child Workflow or sub-state.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cancel-in-flight-turn">
<div class="pattern-tile-header">
<img src="/images/long-running-activity-icon.svg" alt="Cancel In-Flight Turn">
<span>Cancel In-Flight Turn</span>
</div>
<p>Abort a Turn's model and tool Steps without killing the Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-signal-and-start">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session with Signal-and-Start">
<span>Session with Signal-and-Start</span>
</div>
<p>Create or signal a session from the first message.</p>
</a>
</div>
<div class="pattern-tile">
<a href="eager-interactive-session-start">
<div class="pattern-tile-header">
<img src="/images/eager-workflow-start-icon.svg" alt="Eager Interactive Session Start">
<span>Eager Interactive Session Start</span>
</div>
<p>Cut first-Turn latency with Eager Workflow Start.</p>
</a>
</div>
<div class="pattern-tile">
<a href="entity-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Entity Agent">
<span>Entity Agent</span>
</div>
<p>One long-lived agent Workflow per business entity.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-idle-eviction">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.svg" alt="Session Idle Eviction">
<span>Session Idle Eviction</span>
</div>
<p>Close or park Sessions after a durable idle timeout.</p>
</a>
</div>
<div class="pattern-tile">
<a href="continue-as-new-session">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Continue-As-New Session">
<span>Continue-As-New Session</span>
</div>
<p>Reset history while preserving session identity.</p>
</a>
</div>
<div class="pattern-tile">
<a href="scheduled-agent-turns">
<div class="pattern-tile-header">
<img src="/images/delayed-start-icon.svg" alt="Scheduled Agent Turns">
<span>Scheduled Agent Turns</span>
</div>
<p>Wake proactive Turns with Temporal Schedules.</p>
</a>
</div>
<div class="pattern-tile">
<a href="task-mode-session">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Task-Mode Session">
<span>Task-Mode Session</span>
</div>
<p>Pin Sessions to finish without parking for humans.</p>
</a>
</div>
<div class="pattern-tile">
<a href="operator-session-reset">
<div class="pattern-tile-header">
<img src="/images/resumable-activity-icon.svg" alt="Operator Session Reset">
<span>Operator Session Reset</span>
</div>
<p>Recover stuck Sessions without orphaning session_id.</p>
</a>
</div>
<div class="pattern-tile">
<a href="sessions">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Sessions">
<span>Sessions Overview</span>
</div>
<p>Long-lived agent Sessions, Turns, and lifecycle controls.</p>
</a>
</div>
</div>

## Versioning {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="agent-definition-versioning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Agent Definition Versioning">
<span>Agent Definition Versioning</span>
</div>
<p>Pin definition and binding revisions per Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="catalog-snapshot-pinning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Catalog Snapshot Pinning">
<span>Catalog Snapshot Pinning</span>
</div>
<p>Pin tool/prompt catalog bytes so park cannot drift.</p>
</a>
</div>
<div class="pattern-tile">
<a href="dynamic-capability-resolution">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Dynamic Capability Resolution">
<span>Dynamic Capability Resolution</span>
</div>
<p>Resolve Tools/Skills from principal then snapshot.</p>
</a>
</div>
<div class="pattern-tile">
<a href="binding-readiness-gate">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Binding Readiness Gate">
<span>Binding Readiness Gate</span>
</div>
<p>Fail closed when pinned queues or Nexus bindings are down.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-worker-versioning">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Agent Worker Versioning">
<span>Agent Worker Versioning</span>
</div>
<p>Pin Worker build / Deployment Version separately from config.</p>
</a>
</div>
<div class="pattern-tile">
<a href="patched-agent-workflow-evolution">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Patched Agent Workflow Evolution">
<span>Patched Agent Workflow Evolution</span>
</div>
<p>Evolve Session/Turn branching with workflow.patched.</p>
</a>
</div>
<div class="pattern-tile">
<a href="prompt-versioning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Versioning">
<span>Prompt Versioning</span>
</div>
<p>Version prompts separately from Workflow code.</p>
</a>
</div>
<div class="pattern-tile">
<a href="prompt-experiment-pins">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Experiment Pins">
<span>Prompt Experiment Pins</span>
</div>
<p>Pin experiment variants for the life of a Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="versioning">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Versioning">
<span>Versioning Overview</span>
</div>
<p>Pin definition, catalog, binding, Worker, and prompt revisions so parks and rollouts stay reproducible.</p>
</a>
</div>
</div>

## Tools {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="activity-tool">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Activity Tool">
<span>Activity Tool</span>
</div>
<p>Side-effecting tools as durable Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="workflow-tool">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Workflow Tool">
<span>Workflow Tool</span>
</div>
<p>Deterministic tools as in-Workflow code.</p>
</a>
</div>
<div class="pattern-tile">
<a href="callback-tool">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Callback Tool">
<span>Callback Tool</span>
</div>
<p>Tools that run on an attached client.</p>
</a>
</div>
<div class="pattern-tile">
<a href="nexus-tool">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Nexus Tool">
<span>Nexus Tool</span>
</div>
<p>Cross-Namespace tools via Temporal Nexus Operations.</p>
</a>
</div>
<div class="pattern-tile">
<a href="typed-agent-operations">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Typed Agent Operations">
<span>Typed Agent Operations</span>
</div>
<p>Versioned Update/Query contracts between agents.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-tool-loop">
<div class="pattern-tile-header">
<img src="/images/polling-icon.svg" alt="Agent Tool Loop">
<span>Agent Tool Loop</span>
</div>
<p>Durable model↔tool loop until a final reply.</p>
</a>
</div>
<div class="pattern-tile">
<a href="on-demand-skill-load">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="On-Demand Skill Load">
<span>On-Demand Skill Load</span>
</div>
<p>Load Skill bodies into a Turn only when needed.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tool-retry-profiles">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tool Retry Profiles">
<span>Tool Retry Profiles</span>
</div>
<p>Per-tool retry and safety policies.</p>
</a>
</div>
<div class="pattern-tile">
<a href="poison-tool-quarantine">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Poison Tool Quarantine">
<span>Poison Tool Quarantine</span>
</div>
<p>Stop poison tool retry storms with non-retryable classification.</p>
</a>
</div>
<div class="pattern-tile">
<a href="heartbeat-long-steps">
<div class="pattern-tile-header">
<img src="/images/long-running-activity-icon.svg" alt="Heartbeat Long Steps">
<span>Heartbeat Long Steps</span>
</div>
<p>Heartbeats for long-running tool/model Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="local-activity-tools">
<div class="pattern-tile-header">
<img src="/images/local-activities-icon.svg" alt="Local Activity Tools">
<span>Local Activity Tools</span>
</div>
<p>Low-latency tools as Local Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="fast-slow-tool-retries">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Fast/Slow Tool Retries">
<span>Fast/Slow Tool Retries</span>
</div>
<p>Separate fast local retries from slow durable ones.</p>
</a>
</div>
<div class="pattern-tile">
<a href="external-tool-polling">
<div class="pattern-tile-header">
<img src="/images/polling-icon.svg" alt="External Tool Polling">
<span>External Tool Polling</span>
</div>
<p>Poll external jobs without blocking Workers forever.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tool-compensation">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tool Compensation">
<span>Tool Compensation</span>
</div>
<p>Compensate or undo tool side effects.</p>
</a>
</div>
<div class="pattern-tile">
<a href="mcp-openapi-tooling">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="MCP / OpenAPI Tooling">
<span>MCP / OpenAPI Tooling</span>
</div>
<p>Compile external tools into Activity tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tools">
<span>Tools Overview</span>
</div>
<p>How agents invoke side effects: Activity, Workflow, Callback, Nexus, and tool-loop mechanics.</p>
</a>
</div>
</div>

## Model Calls {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="durable-model-call">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Durable Model Call">
<span>Durable Model Call</span>
</div>
<p>LLM calls as first-class Activity steps.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cached-model-call">
<div class="pattern-tile-header">
<img src="/images/local-activities-icon.svg" alt="Cached Model Call">
<span>Cached Model Call</span>
</div>
<p>Activity-boundary cache for identical model inputs.</p>
</a>
</div>
<div class="pattern-tile">
<a href="structured-model-output">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Structured Model Output">
<span>Structured Model Output</span>
</div>
<p>Schema-validated model responses.</p>
</a>
</div>
<div class="pattern-tile">
<a href="provider-retry-delegation">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Provider Retry Delegation">
<span>Provider Retry Delegation</span>
</div>
<p>Let the provider retry transient errors inside one Activity.</p>
</a>
</div>
<div class="pattern-tile">
<a href="model-error-classification">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Model Error Classification">
<span>Model Error Classification</span>
</div>
<p>Map provider errors to retryable vs terminal.</p>
</a>
</div>
<div class="pattern-tile">
<a href="rate-limit-aware-model-calls">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Rate-Limit Aware Model Calls">
<span>Rate-Limit Aware Model Calls</span>
</div>
<p>Back off when providers throttle.</p>
</a>
</div>
<div class="pattern-tile">
<a href="model-timeout-profiles">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.svg" alt="Model Timeout Profiles">
<span>Model Timeout Profiles</span>
</div>
<p>Timeout budgets for model Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="model-calls">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Model Calls">
<span>Model Calls Overview</span>
</div>
<p>Durable LLM Steps: caching, structure, timeouts, and provider-aware retries.</p>
</a>
</div>
</div>

## Human Interaction {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="approval-gated-tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Approval-Gated Tools">
<span>Approval-Gated Tools</span>
</div>
<p>Require approval before risky tools run.</p>
</a>
</div>
<div class="pattern-tile">
<a href="ask-user-wait">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Ask-User Wait">
<span>Ask-User Wait</span>
</div>
<p>Park a Turn for clarifying user input mid-loop.</p>
</a>
</div>
<div class="pattern-tile">
<a href="connection-auth-wait">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Connection Auth Wait">
<span>Connection Auth Wait</span>
</div>
<p>Park for OAuth/connection consent; store tokens off-history.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-scoped-approvals">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session-Scoped Approvals">
<span>Session-Scoped Approvals</span>
</div>
<p>Approve a tool for the rest of a session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="updatable-approval-timer">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.svg" alt="Updatable Approval Timer">
<span>Updatable Approval Timer</span>
</div>
<p>Extendable SLA deadlines for approval waits.</p>
</a>
</div>
<div class="pattern-tile">
<a href="resumable-correction">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Resumable Correction">
<span>Resumable Correction</span>
</div>
<p>Park after repeated failures until a human fixes inputs.</p>
</a>
</div>
<div class="pattern-tile">
<a href="operator-slash-commands">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Operator Slash Commands">
<span>Operator Slash Commands</span>
</div>
<p>Deterministic textual commands inside the session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="human-interaction">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Human Interaction">
<span>Human Interaction Overview</span>
</div>
<p>Pause Turns for approvals, clarifying answers, connection grants, and operator commands.</p>
</a>
</div>
</div>

## Subagents {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="subagent-toolset">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Subagent Toolset">
<span>Subagent Toolset</span>
</div>
<p>Expose a child agent as a tool.</p>
</a>
</div>
<div class="pattern-tile">
<a href="root-mediated-subagent-approvals">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Root-Mediated Subagent Approvals">
<span>Root-Mediated Subagent Approvals</span>
</div>
<p>Proxy child Approvals through the parent Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="persistent-subagent-threads">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Persistent Subagent Threads">
<span>Persistent Subagent Threads</span>
</div>
<p>Keep subagent Sessions across parent Turns.</p>
</a>
</div>
<div class="pattern-tile">
<a href="fanout-subagents">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Fan-Out Subagents">
<span>Fan-Out Subagents</span>
</div>
<p>Run many subagents in parallel.</p>
</a>
</div>
<div class="pattern-tile">
<a href="best-effort-parallel-tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Best-Effort Parallel Tools">
<span>Best-Effort Parallel Tools</span>
</div>
<p>Parallel tools with partial-success budgets.</p>
</a>
</div>
<div class="pattern-tile">
<a href="remote-subagent">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Remote Subagent">
<span>Remote Subagent</span>
</div>
<p>Cross-Namespace or remote agent delegation.</p>
</a>
</div>
<div class="pattern-tile">
<a href="subagents">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Subagents">
<span>Subagents Overview</span>
</div>
<p>Delegate work to child agents, fan-out, and remote agent boundaries.</p>
</a>
</div>
</div>

## Code Mode {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="code-mode-orchestrator">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Code Mode Orchestrator">
<span>Code Mode Orchestrator</span>
</div>
<p>Orchestrate sandboxed code execution from a Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tools-only-sandbox">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tools-Only Sandbox">
<span>Tools-Only Sandbox</span>
</div>
<p>Restrict sandboxes to approved tool surfaces.</p>
</a>
</div>
<div class="pattern-tile">
<a href="type-checked-scripts">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Type-Checked Scripts">
<span>Type-Checked Scripts</span>
</div>
<p>Validate generated scripts before run.</p>
</a>
</div>
<div class="pattern-tile">
<a href="script-fan-out">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Script Fan-Out">
<span>Script Fan-Out</span>
</div>
<p>Fan out sandboxed script work.</p>
</a>
</div>
<div class="pattern-tile">
<a href="sticky-sandbox-task-queues">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Sticky Sandbox Task Queues">
<span>Sticky Sandbox Task Queues</span>
</div>
<p>Pin sandbox Workers with sticky queues.</p>
</a>
</div>
<div class="pattern-tile">
<a href="code-mode">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Code Mode">
<span>Code Mode Overview</span>
</div>
<p>Sandbox orchestration, typed scripts, and sticky Worker placement for code-running agents.</p>
</a>
</div>
</div>

## Safety {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="safety-profiled-tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Safety-Profiled Tools">
<span>Safety-Profiled Tools</span>
</div>
<p>Declare inherently safe, idempotent, or non-idempotent tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="guardrail-steps">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Guardrail Steps">
<span>Guardrail Steps</span>
</div>
<p>Durable pre/post policy checks around model and tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="security-profiles-per-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Security Profiles per Agent">
<span>Security Profiles per Agent</span>
</div>
<p>Environment-specific tool and network allowances.</p>
</a>
</div>
<div class="pattern-tile">
<a href="network-resource-sandboxing">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Network & Resource Sandboxing">
<span>Network & Resource Sandboxing</span>
</div>
<p>Bound sandboxes as data planes under Workflow control.</p>
</a>
</div>
<div class="pattern-tile">
<a href="safety">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Safety">
<span>Safety Overview</span>
</div>
<p>Label tools and environments so policy can gate or block unsafe calls.</p>
</a>
</div>
</div>

## Memory {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="session-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session Memory">
<span>Session Memory</span>
</div>
<p>Durable conversational state in the Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="context-compaction">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Context Compaction">
<span>Context Compaction</span>
</div>
<p>Summarize history to keep model context bounded.</p>
</a>
</div>
<div class="pattern-tile">
<a href="compaction-tool-state-continuity">
<div class="pattern-tile-header">
<img src="/images/event-accumulator-icon.svg" alt="Compaction Tool-State Continuity">
<span>Compaction Tool-State Continuity</span>
</div>
<p>Preserve todos and Approvals across compaction.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cross-session-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Cross-Session Memory">
<span>Cross-Session Memory</span>
</div>
<p>Share memory across Sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="externalized-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Externalized Memory">
<span>Externalized Memory</span>
</div>
<p>Store large memory outside Workflow history.</p>
</a>
</div>
<div class="pattern-tile">
<a href="claim-check-payloads">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Claim-Check Payloads">
<span>Claim-Check Payloads</span>
</div>
<p>Pass large blobs by reference, not in history.</p>
</a>
</div>
<div class="pattern-tile">
<a href="memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Memory">
<span>Memory Overview</span>
</div>
<p>What a Session remembers, compacts, externalizes, and claim-checks.</p>
</a>
</div>
</div>

## Observability {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="standardized-event-stream">
<div class="pattern-tile-header">
<img src="/images/event-accumulator-icon.svg" alt="Standardized Event Stream">
<span>Standardized Event Stream</span>
</div>
<p>A stable event schema for Sessions and Turns.</p>
</a>
</div>
<div class="pattern-tile">
<a href="progress-streaming">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Progress Streaming">
<span>Progress Streaming</span>
</div>
<p>Stream tokens and Step progress to clients.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-tracing">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Agent Tracing">
<span>Agent Tracing</span>
</div>
<p>Correlate Session/Turn/Step traces.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-visibility-attributes">
<div class="pattern-tile-header">
<img src="/images/event-accumulator-icon.svg" alt="Session Visibility Attributes">
<span>Session Visibility Attributes</span>
</div>
<p>Search Attributes for listing Sessions in Visibility.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cost-token-accounting">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Cost & Token Accounting">
<span>Cost & Token Accounting</span>
</div>
<p>Record model and tool spend per Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-spend-caps">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session Spend Caps">
<span>Session Spend Caps</span>
</div>
<p>Hard caps that stop Turns when budget is exhausted.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-step-retry-alerting">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Agent Step Retry Alerting">
<span>Agent Step Retry Alerting</span>
</div>
<p>Alert when Steps retry past a threshold.</p>
</a>
</div>
<div class="pattern-tile">
<a href="eval-backed-behavior-checks">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Eval-Backed Behavior Checks">
<span>Eval-Backed Behavior Checks</span>
</div>
<p>Regression gates for agent behavior.</p>
</a>
</div>
<div class="pattern-tile">
<a href="observability">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Observability">
<span>Observability Overview</span>
</div>
<p>Events, streams, traces, Visibility, cost, and eval gates for agent work.</p>
</a>
</div>
</div>

## Throughput {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="fairness">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Fairness">
<span>Fairness</span>
</div>
<p>Share Worker capacity fairly across tenants.</p>
</a>
</div>
<div class="pattern-tile">
<a href="priority-task-queues">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Priority Task Queues">
<span>Priority Task Queues</span>
</div>
<p>Route urgent work to higher-priority queues.</p>
</a>
</div>
<div class="pattern-tile">
<a href="downstream-tool-rate-limiting">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Downstream Tool Rate Limiting">
<span>Downstream Tool Rate Limiting</span>
</div>
<p>Limit calls to fragile downstream APIs.</p>
</a>
</div>
<div class="pattern-tile">
<a href="throughput">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Throughput">
<span>Throughput Overview</span>
</div>
<p>Fairness, priority, and downstream rate limits across shared Workers.</p>
</a>
</div>
</div>

## Channels {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="http-channel-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="HTTP Channel Agent">
<span>HTTP Channel Agent</span>
</div>
<p>Expose a session API over HTTP and SSE.</p>
</a>
</div>
<div class="pattern-tile">
<a href="messaging-channel-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Messaging Channel Agent">
<span>Messaging Channel Agent</span>
</div>
<p>Map Slack or email into sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="idempotent-delivery">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Idempotent Delivery">
<span>Idempotent Delivery</span>
</div>
<p>Dedupe channel retries with a durable delivery ledger.</p>
</a>
</div>
<div class="pattern-tile">
<a href="validated-session-ingress">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Validated Session Ingress">
<span>Validated Session Ingress</span>
</div>
<p>Reject bad deliveries in Update validators before Turns.</p>
</a>
</div>
<div class="pattern-tile">
<a href="split-resume-observe-handles">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Split Resume and Observe Handles">
<span>Split Resume and Observe Handles</span>
</div>
<p>Separate write tokens from observe/stream credentials.</p>
</a>
</div>
<div class="pattern-tile">
<a href="delivery-authorization-timing">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Delivery Authorization Timing">
<span>Delivery Authorization Timing</span>
</div>
<p>Re-check auth at apply, not only at channel accept.</p>
</a>
</div>
<div class="pattern-tile">
<a href="mid-turn-delivery-coalescing">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Mid-Turn Delivery Coalescing">
<span>Mid-Turn Delivery Coalescing</span>
</div>
<p>Fold queued same-initiator Deliveries into the next Turn.</p>
</a>
</div>
<div class="pattern-tile">
<a href="channels">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Channels">
<span>Channels Overview</span>
</div>
<p>HTTP and messaging ingress, delivery ledgers, and capability-separated handles.</p>
</a>
</div>
</div>
