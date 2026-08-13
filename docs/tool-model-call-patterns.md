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
<p>Timeouts by operation class.</p>
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
</div>

## Choosing a Pattern

**You need activity tool behavior:** Side-effecting tools as durable Activities. Use [Activity Tool](/activity-tool).

**You need workflow tool behavior:** Deterministic tools as in-Workflow code. Use [Workflow Tool](/workflow-tool).

**You need callback tool behavior:** Tools that run on an attached client. Use [Callback Tool](/callback-tool).

**You need durable model call behavior:** LLM calls as first-class Activity steps. Use [Durable Model Call](/durable-model-call).

**You need tool retry profiles behavior:** Per-tool retry and safety policies. Use [Tool Retry Profiles](/tool-retry-profiles).

**You need a multi-step tool-using turn:** use [Agent Tool Loop](/agent-tool-loop).
**You need typed model fields:** use [Structured Model Output](/structured-model-output).
**You need Temporal to own retries:** use [Provider Retry Delegation](/provider-retry-delegation).
**You need correct retry vs fail behavior:** use [Model Error Classification](/model-error-classification).
**You need Retry-After support:** use [Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls).
**You mix fast and slow models/tools:** use [Model Timeout Profiles](/model-timeout-profiles).
**You need reproducible prompts:** use [Prompt Versioning](/prompt-versioning).
## Related Sections

See Concepts for Session, Turn, Step, and related terms used by these patterns.
