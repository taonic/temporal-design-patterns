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
</div>

## Choosing a Pattern

**You need activity tool behavior:** Side-effecting tools as durable Activities. Use [Activity Tool](/activity-tool).

**You need workflow tool behavior:** Deterministic tools as in-Workflow code. Use [Workflow Tool](/workflow-tool).

**You need callback tool behavior:** Tools that run on an attached client. Use [Callback Tool](/callback-tool).

**You need durable model call behavior:** LLM calls as first-class Activity steps. Use [Durable Model Call](/durable-model-call).

**You need tool retry profiles behavior:** Per-tool retry and safety policies. Use [Tool Retry Profiles](/tool-retry-profiles).

## Related Sections

See Vernacular for Session, Turn, Step, and related terms used by these patterns.
