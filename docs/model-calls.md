<h1>Model Calls <img src="/images/child-workflows-icon.svg" alt="Model Calls" class="pattern-page-icon"></h1>

Durable LLM Steps: caching, structure, timeouts, and provider-aware retries.

## Patterns in This Section

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
</div>

## Choosing a Pattern

**You need LLM calls as durable Activities:** Use [Durable Model Call](/durable-model-call).

**You need to skip duplicate provider calls:** Use [Cached Model Call](/cached-model-call).

**You need schema-validated model responses:** Use [Structured Model Output](/structured-model-output).

**You need provider-level retries inside one Activity:** Use [Provider Retry Delegation](/provider-retry-delegation).

**You need to classify provider errors for retry policy:** Use [Model Error Classification](/model-error-classification).

**You need to back off on provider throttles:** Use [Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls).

**You need timeout budgets for model Activities:** Use [Model Timeout Profiles](/model-timeout-profiles).

## Related Sections

See [Tools](/tools) for the tool loop and [Versioning](/versioning) for prompt/experiment pins.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
