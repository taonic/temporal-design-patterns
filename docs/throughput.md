<h1>Throughput <img src="/images/child-workflows-icon.svg" alt="Throughput" class="pattern-page-icon"></h1>

Fairness, priority, and downstream rate limits across shared Workers.

## Patterns in This Section

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
</div>

## Choosing a Pattern

**You need fair Worker capacity across tenants:** Use [Fairness](/fairness).

**You need higher-priority queues for urgent work:** Use [Priority Task Queues](/priority-task-queues).

**You need to limit calls to fragile downstream APIs:** Use [Downstream Tool Rate Limiting](/downstream-tool-rate-limiting).

## Related Sections

See [Model Calls](/model-calls) and [Tools](/tools) for Activities that consume Worker capacity, and [Observability](/observability) for metrics.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
