
# Task orchestration patterns

Patterns for composing and coordinating multiple units of work within a Workflow.

<div class="pattern-grid">
<div class="pattern-tile">
<a href="child-workflows">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.png" alt="Child Workflows">
<span>Child Workflows</span>
</div>
<p>Decomposes complex Workflows into smaller, reusable units. Each child has an independent Workflow ID, history, and lifecycle.</p>
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
</div>
