<h1>Observability & Operations Patterns <img src="/images/child-workflows-icon.svg" alt="Observability & Operations Patterns" class="pattern-page-icon"></h1>

These patterns make agent behavior reconstructable from events, traces, and metrics.

## Patterns in This Section

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
<a href="session-visibility-attributes">
<div class="pattern-tile-header">
<img src="/images/event-accumulator-icon.svg" alt="Session Visibility Attributes">
<span>Session Visibility Attributes</span>
</div>
<p>Search Attributes so ops can list Sessions by status and tenant.</p>
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
<a href="agent-step-retry-alerting">
<div class="pattern-tile-header">
<img src="/images/retry-metrics-icon.svg" alt="Agent Step Retry Alerting">
<span>Agent Step Retry Alerting</span>
</div>
<p>Page when model/tool attempts cross a threshold.</p>
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
</div>

## Choosing a Pattern

**You need standardized event stream behavior:** One ordered stream per session. Use [Standardized Event Stream](/standardized-event-stream).

**You need agent tracing behavior:** Correlate spans with session and step IDs. Use [Agent Tracing](/agent-tracing).

**You need to list Sessions by status/tenant in Temporal Visibility:** Use [Session Visibility Attributes](/session-visibility-attributes).

**You need cost & token accounting behavior:** Aggregate usage per call, turn, and session. Use [Cost & Token Accounting](/cost-token-accounting).

**You need paging on silent retry storms:** Use [Agent Step Retry Alerting](/agent-step-retry-alerting).

**You need eval-backed behavior checks behavior:** Regression checks on recorded sessions. Use [Eval-Backed Behavior Checks](/eval-backed-behavior-checks).

**You need live UI progress with reconnect:** use [Progress Streaming](/progress-streaming).
## Related Sections

See [QoS & Throughput Patterns](/qos-throughput-patterns) when you need fairness or priority controls that shape the same Worker capacity these metrics observe.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
