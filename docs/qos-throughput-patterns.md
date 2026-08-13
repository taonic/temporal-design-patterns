<h1>QoS & Throughput Patterns <img src="/images/fairness-icon.svg" alt="QoS & Throughput Patterns" class="pattern-page-icon"></h1>

These patterns control how multi-tenant agent Sessions and Steps share Worker capacity on a Task Queue.

## Patterns in This Section

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
</div>

## Choosing a Pattern

**You need fairness across tenants:** One hot tenant's Sessions must not starve others on a shared Task Queue. Use [Fairness](/fairness).

**You need urgency ordering:** Interactive agent Turns must beat batch, eval, or background Sessions on the same queue. Use [Priority Task Queues](/priority-task-queues).

**You need both:** Set `priority_key` and `fairness_key` together so urgency wins first, then tenants share capacity within each priority level.

## Related Sections

See [Tool & Model Call Patterns](/tool-model-call-patterns) for durable model Activities, timeout profiles, and rate-limit-aware retries that consume the same Worker capacity these QoS controls allocate.

See [Observability & Operations Patterns](/observability-patterns) for event streams, tracing, and cost metrics you can break down by tenant or priority level.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
