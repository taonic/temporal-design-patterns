<h1>Agentic Patterns <img src="/images/agentic-patterns-icon.svg" alt="Agentic Patterns" class="pattern-page-icon"></h1>

These patterns apply Temporal's durable execution to AI and agentic systems — pipelines built on model providers, tool calls, and multi-step reasoning where the underlying services are unreliable, non-deterministic, and metered.

Model providers fail in ways that ordinary services do not.
The same input can succeed on one provider and be rejected by another, capacity varies by the hour, and every call costs money.
These patterns give the Workflow control over how work is routed, retried, and abandoned so that an unreliable model layer becomes a dependable pipeline.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="provider-fallback">
<div class="pattern-tile-header">
<img src="/images/provider-fallback-icon.svg" alt="Model Provider Fallback">
<span>Model Provider Fallback</span>
</div>
<p>Sweeps a preference-ordered list of model providers, classifying each failure so the Workflow retries the same provider, fails over to the next, or aborts when no provider can help.</p>
</a>
</div>
</div>

## Related Sections

- [Error Handling & Retry Patterns](/error-handling-patterns) — the retry and non-retryable-error mechanisms these patterns build on
- [QoS & Throughput Patterns](/qos-throughput-patterns) — rate limiting and fairness for metered provider APIs
- [Worker Configuration Patterns](/worker-configuration-patterns) — routing provider calls to dedicated Worker pools

## References

- [Temporal Retry Policies](https://docs.temporal.io/encyclopedia/retry-policies)
- [Failure Handling in Practice](https://temporal.io/blog/failure-handling-in-practice)
