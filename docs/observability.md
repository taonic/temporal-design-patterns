<h1>Observability <img src="/images/child-workflows-icon.svg" alt="Observability" class="pattern-page-icon"></h1>

Events, streams, traces, Visibility, cost, and eval gates for agent work.

## Patterns in This Section

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
</div>

## Choosing a Pattern

**You need a stable event schema for Sessions and Turns:** Use [Standardized Event Stream](/standardized-event-stream).

**You need to stream tokens and Step progress:** Use [Progress Streaming](/progress-streaming).

**You need correlated Session/Turn/Step traces:** Use [Agent Tracing](/agent-tracing).

**You need to list Sessions in Temporal Visibility:** Use [Session Visibility Attributes](/session-visibility-attributes).

**You need to record model and tool spend:** Use [Cost & Token Accounting](/cost-token-accounting).

**You need hard caps when budget is exhausted:** Use [Session Spend Caps](/session-spend-caps).

**You need alerts when Steps retry past a threshold:** Use [Agent Step Retry Alerting](/agent-step-retry-alerting).

**You need regression gates for agent behavior:** Use [Eval-Backed Behavior Checks](/eval-backed-behavior-checks).

## Related Sections

See [Throughput](/throughput) for fairness/priority that shapes the same Worker capacity these metrics observe.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
