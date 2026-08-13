<h1>Safety <img src="/images/child-workflows-icon.svg" alt="Safety" class="pattern-page-icon"></h1>

Label tools and environments so policy can gate or block unsafe calls.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="safety-profiled-tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Safety-Profiled Tools">
<span>Safety-Profiled Tools</span>
</div>
<p>Declare inherently safe, idempotent, or non-idempotent tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="guardrail-steps">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Guardrail Steps">
<span>Guardrail Steps</span>
</div>
<p>Durable pre/post policy checks around model and tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="security-profiles-per-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Security Profiles per Agent">
<span>Security Profiles per Agent</span>
</div>
<p>Environment-specific tool and network allowances.</p>
</a>
</div>
<div class="pattern-tile">
<a href="network-resource-sandboxing">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Network & Resource Sandboxing">
<span>Network & Resource Sandboxing</span>
</div>
<p>Bound sandboxes as data planes under Workflow control.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need to declare tool safety classes:** Use [Safety-Profiled Tools](/safety-profiled-tools).

**You need durable content/policy checks around model and tools:** Use [Guardrail Steps](/guardrail-steps).

**You need environment-specific tool and network allowances:** Use [Security Profiles per Agent](/security-profiles-per-agent).

**You need to bound sandboxes as Workflow-controlled data planes:** Use [Network & Resource Sandboxing](/network-resource-sandboxing).

## Related Sections

See [Channels](/channels) for resume/observe handles and delivery auth timing, and [Tools](/tools) for safety-profiled tools.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
