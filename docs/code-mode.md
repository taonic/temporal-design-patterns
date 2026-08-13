<h1>Code Mode <img src="/images/child-workflows-icon.svg" alt="Code Mode" class="pattern-page-icon"></h1>

Sandbox orchestration, typed scripts, and sticky Worker placement for code-running agents.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="code-mode-orchestrator">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Code Mode Orchestrator">
<span>Code Mode Orchestrator</span>
</div>
<p>Orchestrate sandboxed code execution from a Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tools-only-sandbox">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tools-Only Sandbox">
<span>Tools-Only Sandbox</span>
</div>
<p>Restrict sandboxes to approved tool surfaces.</p>
</a>
</div>
<div class="pattern-tile">
<a href="sandbox-profile-tiers">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Sandbox Profile Tiers">
<span>Sandbox Profile Tiers</span>
</div>
<p>Pin read-only, workspace-write, or full-access.</p>
</a>
</div>
<div class="pattern-tile">
<a href="type-checked-scripts">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Type-Checked Scripts">
<span>Type-Checked Scripts</span>
</div>
<p>Validate generated scripts before run.</p>
</a>
</div>
<div class="pattern-tile">
<a href="script-fan-out">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Script Fan-Out">
<span>Script Fan-Out</span>
</div>
<p>Fan out sandboxed script work.</p>
</a>
</div>
<div class="pattern-tile">
<a href="sticky-sandbox-task-queues">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Sticky Sandbox Task Queues">
<span>Sticky Sandbox Task Queues</span>
</div>
<p>Pin sandbox Workers with sticky queues.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need to orchestrate sandboxed code from a Session:** Use [Code Mode Orchestrator](/code-mode-orchestrator).

**You need to restrict sandboxes to approved tools:** Use [Tools-Only Sandbox](/tools-only-sandbox).

**You need to validate generated scripts before run:** Use [Type-Checked Scripts](/type-checked-scripts).

**You need to fan out sandboxed script work:** Use [Script Fan-Out](/script-fan-out).

**You need sticky queues for sandbox Workers:** Use [Sticky Sandbox Task Queues](/sticky-sandbox-task-queues).

**You need named isolation tiers for shell Tools:** Use [Sandbox Profile Tiers](/sandbox-profile-tiers).

## Related Sections

See [Safety](/safety) for sandbox bounds and [Tools](/tools) for Activity-backed execution.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
