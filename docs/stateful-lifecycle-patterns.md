
# Stateful / lifecycle patterns

Patterns for managing Workflow state and lifecycle.

<div class="pattern-grid">
<div class="pattern-tile">
<a href="entity-workflow">
<div class="pattern-tile-header">
<img src="/images/entity-workflow-icon.png" alt="Entity Workflow">
<span>Entity Workflow</span>
</div>
<p>Models long-lived business entities as individual Workflows that persist for the entity's entire lifetime, handling all state transitions through Signals and Updates.</p>
</a>
</div>

<div class="pattern-tile">
<a href="request-response-via-updates">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.png" alt="Request-Response via Updates">
<span>Request-Response via Updates</span>
</div>
<p>Synchronous request-response with validation. Updates modify state and return results directly.</p>
</a>
</div>

<div class="pattern-tile">
<a href="continue-as-new">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.png" alt="Continue-As-New">
<span>Continue-As-New</span>
</div>
<p>Prevents unbounded history growth by completing the current execution and starting a new one with fresh history.</p>
</a>
</div>

<div class="pattern-tile">
<a href="child-workflows">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.png" alt="Child Workflows">
<span>Child Workflows</span>
</div>
<p>Decomposes complex Workflows into smaller, reusable units. Each child has an independent Workflow ID, history, and lifecycle.</p>
</a>
</div>
</div>
