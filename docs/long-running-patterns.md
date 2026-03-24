
# Long-running and operational patterns

Patterns for long-running Activities, polling, retries, and operational concerns.

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
<a href="parallel-execution">
<div class="pattern-tile-header">
<img src="/images/parallel-execution-icon.png" alt="Parallel Execution">
<span>Parallel Execution</span>
</div>
<p>Executes multiple Activities concurrently for maximum throughput with error handling and controlled parallelism.</p>
</a>
</div>

<div class="pattern-tile">
<a href="pick-first">
<div class="pattern-tile-header">
<img src="/images/pick-first-icon.png" alt="Pick First">
<span>Pick First (Race)</span>
</div>
<p>Starts multiple Activities in parallel and uses the first result, cancelling the rest.</p>
</a>
</div>

<div class="pattern-tile">
<a href="worker-specific-taskqueue">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.png" alt="Worker-Specific Task Queues">
<span>Worker-Specific Task Queues</span>
</div>
<p>Routes Activities to specific Workers using unique Task Queues for Worker affinity and host-specific processing.</p>
</a>
</div>
</div>
