# Temporal Design Patterns

> **Warning:** This catalog is under active development. Content and structure may change.
>
> **Personal project by [@taonic](https://github.com/taonic).**

Temporal provides a set of durable execution primitives that you can compose into common, reusable, and proven patterns.
Having these patterns in your toolbox helps you solve recurring problems in a battle-tested way.

## Distributed transaction patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="saga-pattern">
<div class="pattern-tile-header">
<img src="/images/saga-icon.png" alt="Saga Pattern">
<span>Saga Pattern</span>
</div>
<p>Manages distributed transactions with compensating actions. Each step has a compensation that undoes its effects if subsequent steps fail.</p>
</a>
</div>

<div class="pattern-tile">
<a href="early-return">
<div class="pattern-tile-header">
<img src="/images/early-return-icon.png" alt="Early Return">
<span>Early Return</span>
</div>
<p>Synchronous initialization with asynchronous completion. Returns results immediately while processing continues in the background.</p>
</a>
</div>
</div>

## Entity & lifecycle patterns {.pattern-section-title}

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

## Workflow messaging patterns {.pattern-section-title}

<div class="pattern-grid">
<div class="pattern-tile">
<a href="signal-with-start">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.png" alt="Signal with Start">
<span>Signal with Start</span>
</div>
<p>Starts a Workflow when Signaling it if it does not already exist. If already running, it receives the Signal directly.</p>
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
</div>

## Task orchestration patterns {.pattern-section-title}

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

## External interaction patterns {.pattern-section-title}

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

## Worker configuration patterns {.pattern-section-title}

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
