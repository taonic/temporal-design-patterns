
# External interaction patterns

Patterns for waiting on or interacting with systems and actors outside the Workflow, including external APIs, human decisions, and scheduled delays.

<div class="pattern-grid">
<div class="pattern-tile">
<a href="polling">
<div class="pattern-tile-header">
<img src="/images/polling-icon.png" alt="Polling">
<span>Polling External Services</span>
</div>
<p>Strategies for polling external resources with varying frequencies: frequent, infrequent, and periodic patterns.</p>
</a>
</div>

<div class="pattern-tile">
<a href="long-running-activity">
<div class="pattern-tile-header">
<img src="/images/long-running-activity-icon.png" alt="Long-Running Activity">
<span>Long-Running Activity</span>
</div>
<p>Long-running Activities report progress via heartbeats and enable resumption after failures with cancellation support.</p>
</a>
</div>

<div class="pattern-tile">
<a href="approval">
<div class="pattern-tile-header">
<img src="/images/approval-icon.png" alt="Approval">
<span>Approval</span>
</div>
<p>Human-in-the-loop Workflows that block until external approval decisions are made. Uses Signals to capture approval data with metadata.</p>
</a>
</div>

<div class="pattern-tile">
<a href="delayed-start">
<div class="pattern-tile-header">
<img src="/images/delayed-start-icon.png" alt="Delayed Start">
<span>Delayed Start</span>
</div>
<p>Creates Workflows immediately but defers execution until a specified delay expires. Fits one-time scheduled operations and grace periods.</p>
</a>
</div>
</div>
