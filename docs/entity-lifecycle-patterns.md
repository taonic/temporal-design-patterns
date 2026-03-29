
# Entity & lifecycle patterns

Patterns for modeling long-lived stateful entities and managing Workflow history growth over time.

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
<a href="continue-as-new">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.png" alt="Continue-As-New">
<span>Continue-As-New</span>
</div>
<p>Prevents unbounded history growth by completing the current execution and starting a new one with fresh history.</p>
</a>
</div>

<div class="pattern-tile">
<a href="updatable-timer">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.png" alt="Updatable Timer">
<span>Updatable Timer</span>
</div>
<p>Dynamically adjustable timers that respond to Signals or Updates. Extend, shorten, or cancel timers based on external events.</p>
</a>
</div>
</div>
