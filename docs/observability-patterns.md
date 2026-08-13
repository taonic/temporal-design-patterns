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
</div>

## Choosing a Pattern

**You need standardized event stream behavior:** One ordered stream per session. Use [Standardized Event Stream](/standardized-event-stream).

**You need agent tracing behavior:** Correlate spans with session and step IDs. Use [Agent Tracing](/agent-tracing).

**You need cost & token accounting behavior:** Aggregate usage per call, turn, and session. Use [Cost & Token Accounting](/cost-token-accounting).

**You need eval-backed behavior checks behavior:** Regression checks on recorded sessions. Use [Eval-Backed Behavior Checks](/eval-backed-behavior-checks).

**You need live UI progress with reconnect:** use [Progress Streaming](/progress-streaming).
## Related Sections

See Vernacular for Session, Turn, Step, and related terms used by these patterns.
