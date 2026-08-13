# Temporal Agentic Patterns

> **Warning:** This catalog is under active development. Content and structure may change.

Temporal provides durable execution primitives that you can compose into common, reusable patterns for AI agents.
Having these patterns in your toolbox helps you keep sessions, tools, approvals, and subagents durable, observable, and safe.

## Agent & Session patterns {.pattern-section-title}

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
<a href="session-signal-and-start">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session with Signal-and-Start">
<span>Session with Signal-and-Start</span>
</div>
<p>Create or signal a session from the first message.</p>
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
<a href="continue-as-new-session">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Continue-As-New Session">
<span>Continue-As-New Session</span>
</div>
<p>Reset history while preserving session identity.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-session-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Agent & Session Patterns">
<span>Agent & Session Patterns Overview</span>
</div>
<p>These patterns model long-lived agent sessions and how turns attach to them.</p>
</a>
</div>
</div>

## Tool & Model Call patterns {.pattern-section-title}

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
<a href="durable-model-call">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Durable Model Call">
<span>Durable Model Call</span>
</div>
<p>LLM calls as first-class Activity steps.</p>
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
<a href="agent-tool-loop">
<div class="pattern-tile-header">
<img src="/images/polling-icon.svg" alt="Agent Tool Loop">
<span>Agent Tool Loop</span>
</div>
<p>Durable model↔tool loop until a final reply.</p>
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
<img src="/images/fixed-count-retries-icon.svg" alt="Provider Retry Delegation">
<span>Provider Retry Delegation</span>
</div>
<p>Disable provider SDK retries; Temporal owns backoff.</p>
</a>
</div>
<div class="pattern-tile">
<a href="model-error-classification">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Model Error Classification">
<span>Model Error Classification</span>
</div>
<p>Retryable vs non-retryable provider errors.</p>
</a>
</div>
<div class="pattern-tile">
<a href="rate-limit-aware-model-calls">
<div class="pattern-tile-header">
<img src="/images/downstream-rate-limiting-icon.svg" alt="Rate-Limit Aware Model Calls">
<span>Rate-Limit Aware Model Calls</span>
</div>
<p>Honor Retry-After via next_retry_delay.</p>
</a>
</div>
<div class="pattern-tile">
<a href="model-timeout-profiles">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.svg" alt="Model Timeout Profiles">
<span>Model Timeout Profiles</span>
</div>
<p>Timeouts by chat, reasoning, search, and tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="prompt-versioning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Versioning">
<span>Prompt Versioning</span>
</div>
<p>Pin reproducible prompt IDs for in-flight sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tool-model-call-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tool & Model Call Patterns">
<span>Tool & Model Call Patterns Overview</span>
</div>
<p>These patterns make model and tool calls durable Temporal Activities or deterministic Workflow code.</p>
</a>
</div>
</div>

## Human-in-the-loop patterns {.pattern-section-title}

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
<a href="session-scoped-approvals">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session-Scoped Approvals">
<span>Session-Scoped Approvals</span>
</div>
<p>Approve a tool for the rest of a session.</p>
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
<a href="human-in-the-loop-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Human-in-the-loop Patterns">
<span>Human-in-the-loop Patterns Overview</span>
</div>
<p>These patterns pause agents for approvals, corrections, and operator commands.</p>
</a>
</div>
</div>

## Subagent & Multi-agent patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="subagent-toolset">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Subagent Toolset">
<span>Subagent Toolset</span>
</div>
<p>Drive another agent through typed operations.</p>
</a>
</div>
<div class="pattern-tile">
<a href="persistent-subagent-threads">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Persistent Subagent Threads">
<span>Persistent Subagent Threads</span>
</div>
<p>Reusable durable threads per topic or user.</p>
</a>
</div>
<div class="pattern-tile">
<a href="fanout-subagents">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Fan-Out Subagents">
<span>Fan-Out Subagents</span>
</div>
<p>Spawn many subagent sessions in parallel.</p>
</a>
</div>
<div class="pattern-tile">
<a href="remote-subagent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Remote Subagent">
<span>Remote Subagent</span>
</div>
<p>Drive an agent hosted elsewhere via session HTTP.</p>
</a>
</div>
<div class="pattern-tile">
<a href="best-effort-parallel-tools">
<div class="pattern-tile-header">
<img src="/images/parallel-execution-icon.svg" alt="Best-Effort Parallel Tools">
<span>Best-Effort Parallel Tools</span>
</div>
<p>Parallel tools that continue with partial successes.</p>
</a>
</div>
<div class="pattern-tile">
<a href="subagent-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Subagent & Multi-agent Patterns">
<span>Subagent & Multi-agent Patterns Overview</span>
</div>
<p>These patterns compose agents as typed toolsets and durable child sessions.</p>
</a>
</div>
</div>

## Code Mode & Sandbox patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="code-mode-orchestrator">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Code Mode Orchestrator">
<span>Code Mode Orchestrator</span>
</div>
<p>One run-code tool over many host tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tools-only-sandbox">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tools-Only Sandbox">
<span>Tools-Only Sandbox</span>
</div>
<p>Scripts may only call host tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="type-checked-scripts">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Type-Checked Scripts">
<span>Type-Checked Scripts</span>
</div>
<p>Reject ill-typed scripts before execution.</p>
</a>
</div>
<div class="pattern-tile">
<a href="script-fan-out">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Script Fan-Out">
<span>Script Fan-Out</span>
</div>
<p>Concurrent tool and subagent calls from one script.</p>
</a>
</div>
<div class="pattern-tile">
<a href="code-mode-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Code Mode & Sandbox Patterns">
<span>Code Mode & Sandbox Patterns Overview</span>
</div>
<p>These patterns let a model orchestrate tools by writing scripts that call host APIs.</p>
</a>
</div>
</div>

## Safety & Security patterns {.pattern-section-title}

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
<a href="safety-security-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Safety & Security Patterns">
<span>Safety & Security Patterns Overview</span>
</div>
<p>These patterns label tools and environments so policy can gate or block unsafe calls.</p>
</a>
</div>
</div>

## Memory & State patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="session-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session Memory">
<span>Session Memory</span>
</div>
<p>Store summaries in session state between turns.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cross-session-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Cross-Session Memory">
<span>Cross-Session Memory</span>
</div>
<p>Share bounded memory across sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="externalized-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Externalized Memory">
<span>Externalized Memory</span>
</div>
<p>Push large memory behind durable tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="claim-check-payloads">
<div class="pattern-tile-header">
<img src="/images/batch-iterator-icon.svg" alt="Claim-Check Payloads">
<span>Claim-Check Payloads</span>
</div>
<p>Store large model/tool blobs by reference, not in history.</p>
</a>
</div>
<div class="pattern-tile">
<a href="memory-state-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Memory & State Patterns">
<span>Memory & State Patterns Overview</span>
</div>
<p>These patterns keep conversation and knowledge durable across turns and sessions.</p>
</a>
</div>
</div>

## Observability & Operations patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="standardized-event-stream">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Standardized Event Stream">
<span>Standardized Event Stream</span>
</div>
<p>One ordered stream per session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-tracing">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Agent Tracing">
<span>Agent Tracing</span>
</div>
<p>Correlate spans with session and step IDs.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cost-token-accounting">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Cost & Token Accounting">
<span>Cost & Token Accounting</span>
</div>
<p>Aggregate usage per call, turn, and session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="eval-backed-behavior-checks">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Eval-Backed Behavior Checks">
<span>Eval-Backed Behavior Checks</span>
</div>
<p>Regression checks on recorded sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="progress-streaming">
<div class="pattern-tile-header">
<img src="/images/event-accumulator-icon.svg" alt="Progress Streaming">
<span>Progress Streaming</span>
</div>
<p>Durable cursored live progress for agent UIs.</p>
</a>
</div>
<div class="pattern-tile">
<a href="observability-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Observability & Operations Patterns">
<span>Observability & Operations Patterns Overview</span>
</div>
<p>These patterns make agent behavior reconstructable from events, traces, and metrics.</p>
</a>
</div>
</div>

## QoS & Throughput patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="fairness">
<div class="pattern-tile-header">
<img src="/images/fairness-icon.svg" alt="Fairness">
<span>Fairness</span>
</div>
<p>Proportional Worker share per tenant on one queue.</p>
</a>
</div>
<div class="pattern-tile">
<a href="priority-task-queues">
<div class="pattern-tile-header">
<img src="/images/priority-task-queues-icon.svg" alt="Priority Task Queues">
<span>Priority Task Queues</span>
</div>
<p>Interactive Turns ahead of batch and eval Sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="qos-throughput-patterns">
<div class="pattern-tile-header">
<img src="/images/fairness-icon.svg" alt="QoS & Throughput Patterns">
<span>QoS & Throughput Patterns Overview</span>
</div>
<p>These patterns control how multi-tenant agent Sessions and Steps share Worker capacity.</p>
</a>
</div>
</div>

## Channel & Integration patterns {.pattern-section-title}

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
<a href="mcp-openapi-tooling">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="MCP / OpenAPI Tooling">
<span>MCP / OpenAPI Tooling</span>
</div>
<p>Compile external tools into Activity tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="channel-integration-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Channel & Integration Patterns">
<span>Channel & Integration Patterns Overview</span>
</div>
<p>These patterns bind agents to HTTP, messaging, and external tool catalogs.</p>
</a>
</div>
</div>

