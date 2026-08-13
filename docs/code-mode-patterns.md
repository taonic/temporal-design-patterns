<h1>Code Mode & Sandbox Patterns <img src="/images/child-workflows-icon.svg" alt="Code Mode & Sandbox Patterns" class="pattern-page-icon"></h1>

These patterns let a model orchestrate tools by writing scripts that call host APIs.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="code-mode-orchestrator">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Code Mode Orchestrator">
<span>Code Mode Orchestrator</span>
</div>
<p>One run-code tool over many host tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tools-only-sandbox">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tools-Only Sandbox">
<span>Tools-Only Sandbox</span>
</div>
<p>Scripts may only call host tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="type-checked-scripts">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Type-Checked Scripts">
<span>Type-Checked Scripts</span>
</div>
<p>Reject ill-typed scripts before execution.</p>
</a>
</div>
<div class="pattern-tile">
<a href="script-fan-out">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Script Fan-Out">
<span>Script Fan-Out</span>
</div>
<p>Concurrent tool and subagent calls from one script.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need code mode orchestrator behavior:** One run-code tool over many host tools. Use [Code Mode Orchestrator](/code-mode-orchestrator).

**You need tools-only sandbox behavior:** Scripts may only call host tools. Use [Tools-Only Sandbox](/tools-only-sandbox).

**You need type-checked scripts behavior:** Reject ill-typed scripts before execution. Use [Type-Checked Scripts](/type-checked-scripts).

**You need script fan-out behavior:** Concurrent tool and subagent calls from one script. Use [Script Fan-Out](/script-fan-out).

## Related Sections

See Concepts for Session, Turn, Step, and related terms used by these patterns.
