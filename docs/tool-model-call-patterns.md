<h1>Tool & Model Call Patterns <img src="/images/child-workflows-icon.svg" alt="Tool & Model Call Patterns" class="pattern-page-icon"></h1>

These patterns make model and tool calls durable Temporal Activities or deterministic Workflow code.

## Patterns in This Section

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
<p>Timeouts by operation class.</p>
</a>
</div>
<div class="pattern-tile">
<a href="heartbeat-long-steps">
<div class="pattern-tile-header">
<img src="/images/long-running-activity-icon.svg" alt="Heartbeat Long Steps">
<span>Heartbeat Long Steps</span>
</div>
<p>Liveness, cancel, and checkpoints for long Steps.</p>
</a>
</div>
<div class="pattern-tile">
<a href="local-activity-tools">
<div class="pattern-tile-header">
<img src="/images/local-activities-icon.svg" alt="Local Activity Tools">
<span>Local Activity Tools</span>
</div>
<p>Tiny helpers as Local Activities; keep IO regular.</p>
</a>
</div>
<div class="pattern-tile">
<a href="fast-slow-tool-retries">
<div class="pattern-tile-header">
<img src="/images/fast-slow-retries-icon.svg" alt="Fast/Slow Tool Retries">
<span>Fast/Slow Tool Retries</span>
</div>
<p>Blip recovery then patient outage waits.</p>
</a>
</div>
<div class="pattern-tile">
<a href="external-tool-polling">
<div class="pattern-tile-header">
<img src="/images/polling-icon.svg" alt="External Tool Polling">
<span>External Tool Polling</span>
</div>
<p>Wait on job-based APIs without webhooks.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tool-compensation">
<div class="pattern-tile-header">
<img src="/images/saga-icon.svg" alt="Tool Compensation">
<span>Tool Compensation</span>
</div>
<p>Undo non-idempotent tool writes on failure.</p>
</a>
</div>
<div class="pattern-tile">
<a href="poison-tool-quarantine">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Poison Tool Quarantine">
<span>Poison Tool Quarantine</span>
</div>
<p>Stop poison tool payloads from retrying forever.</p>
</a>
</div>
<div class="pattern-tile">
<a href="prompt-versioning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Versioning">
<span>Prompt Versioning</span>
</div>
<p>Pin reproducible prompt versions.</p>
</a>
</div>
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
<a href="prompt-experiment-pins">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Experiment Pins">
<span>Prompt Experiment Pins</span>
</div>
<p>Sticky A/B prompt or model variant per Session.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need activity tool behavior:** Side-effecting tools as durable Activities. Use [Activity Tool](/activity-tool).

**You need workflow tool behavior:** Deterministic tools as in-Workflow code. Use [Workflow Tool](/workflow-tool).

**You need callback tool behavior:** Tools that run on an attached client. Use [Callback Tool](/callback-tool).

**You need a Temporal-native tool in another Namespace:** use [Nexus Tool](/nexus-tool).

**You need a typed Update/Query contract between agents or clients:** use [Typed Agent Operations](/typed-agent-operations).

**You need durable model call behavior:** LLM calls as first-class Activity steps. Use [Durable Model Call](/durable-model-call).

**You need to skip duplicate provider calls:** Use [Cached Model Call](/cached-model-call).

**You need tool retry profiles behavior:** Per-tool retry and safety policies. Use [Tool Retry Profiles](/tool-retry-profiles).

**You need a multi-step tool-using turn:** use [Agent Tool Loop](/agent-tool-loop).
**You need typed model fields:** use [Structured Model Output](/structured-model-output).
**You need Temporal to own retries:** use [Provider Retry Delegation](/provider-retry-delegation).
**You need correct retry vs fail behavior:** use [Model Error Classification](/model-error-classification).
**You need Retry-After support:** use [Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls).
**You mix fast and slow models/tools:** use [Model Timeout Profiles](/model-timeout-profiles).
**You need heartbeats on long model/tool Steps:** use [Heartbeat Long Steps](/heartbeat-long-steps).
**You measured overhead from tiny helper Activities:** use [Local Activity Tools](/local-activity-tools).
**You need blip-fast then outage-slow retries:** use [Fast/Slow Tool Retries](/fast-slow-tool-retries).
**You must poll a job API with no webhook:** use [External Tool Polling](/external-tool-polling).
**You need undo for multi-write tool Turns:** use [Tool Compensation](/tool-compensation).
**You need reproducible prompts:** use [Prompt Versioning](/prompt-versioning).
**You need definition vs binding pins for whole agents:** use [Agent Definition Versioning](/agent-definition-versioning).
**You need sticky A/B prompt variants:** use [Prompt Experiment Pins](/prompt-experiment-pins).
**You need to stop poison tool retry storms:** use [Poison Tool Quarantine](/poison-tool-quarantine).

## Related Sections

See Concepts for Session, Turn, Step, and related terms used by these patterns.
