
# Worker configuration patterns

Patterns for configuring how Workers are set up, how work is routed, and how Activities access external dependencies.

<div class="pattern-grid">
<div class="pattern-tile">
<a href="worker-specific-taskqueue">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.png" alt="Worker-Specific Task Queues">
<span>Worker-Specific Task Queues</span>
</div>
<p>Routes Activities to specific Workers using unique Task Queues for Worker affinity and host-specific processing.</p>
</a>
</div>

<div class="pattern-tile">
<a href="activity-dependency-injection">
<div class="pattern-tile-header">
<img src="/images/activity-dependency-injection-icon.png" alt="Activity Dependency Injection">
<span>Activity Dependency Injection</span>
</div>
<p>Injects external dependencies into Activities at Worker startup, keeping Workflow code deterministic and Activities testable.</p>
</a>
</div>
</div>
