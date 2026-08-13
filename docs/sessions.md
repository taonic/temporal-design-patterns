<h1>Sessions <img src="/images/child-workflows-icon.svg" alt="Sessions" class="pattern-page-icon"></h1>

Long-lived agent Sessions, Turns, and lifecycle controls.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="session-workflow">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session Workflow">
<span>Session Workflow</span>
</div>
<p>One Workflow owns a session, memory, and event stream.</p>
</a>
</div>
<div class="pattern-tile">
<a href="turn-workflow">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Turn Workflow">
<span>Turn Workflow</span>
</div>
<p>Isolate each turn as a child Workflow or sub-state.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cancel-in-flight-turn">
<div class="pattern-tile-header">
<img src="/images/long-running-activity-icon.svg" alt="Cancel In-Flight Turn">
<span>Cancel In-Flight Turn</span>
</div>
<p>Abort a Turn's model and tool Steps without killing the Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-signal-and-start">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session with Signal-and-Start">
<span>Session with Signal-and-Start</span>
</div>
<p>Create or signal a session from the first message.</p>
</a>
</div>
<div class="pattern-tile">
<a href="eager-interactive-session-start">
<div class="pattern-tile-header">
<img src="/images/eager-workflow-start-icon.svg" alt="Eager Interactive Session Start">
<span>Eager Interactive Session Start</span>
</div>
<p>Cut first-Turn latency with Eager Workflow Start.</p>
</a>
</div>
<div class="pattern-tile">
<a href="entity-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Entity Agent">
<span>Entity Agent</span>
</div>
<p>One long-lived agent Workflow per business entity.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-idle-eviction">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.svg" alt="Session Idle Eviction">
<span>Session Idle Eviction</span>
</div>
<p>Close or park Sessions after a durable idle timeout.</p>
</a>
</div>
<div class="pattern-tile">
<a href="continue-as-new-session">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Continue-As-New Session">
<span>Continue-As-New Session</span>
</div>
<p>Reset history while preserving session identity.</p>
</a>
</div>
<div class="pattern-tile">
<a href="scheduled-agent-turns">
<div class="pattern-tile-header">
<img src="/images/delayed-start-icon.svg" alt="Scheduled Agent Turns">
<span>Scheduled Agent Turns</span>
</div>
<p>Wake proactive Turns with Temporal Schedules.</p>
</a>
</div>
<div class="pattern-tile">
<a href="task-mode-session">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Task-Mode Session">
<span>Task-Mode Session</span>
</div>
<p>Pin Sessions to finish without parking for humans.</p>
</a>
</div>
<div class="pattern-tile">
<a href="initiator-vs-current-principal">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Initiator vs Current Principal">
<span>Initiator vs Current Principal</span>
</div>
<p>Pin Session owner separately from Delivery caller.</p>
</a>
</div>
<div class="pattern-tile">
<a href="operator-session-reset">
<div class="pattern-tile-header">
<img src="/images/resumable-activity-icon.svg" alt="Operator Session Reset">
<span>Operator Session Reset</span>
</div>
<p>Recover stuck Sessions without orphaning session_id.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need a Workflow that owns memory and the event stream:** Use [Session Workflow](/session-workflow).

**You need to isolate each Turn as a child Workflow or sub-state:** Use [Turn Workflow](/turn-workflow).

**You need to abort an open Turn without ending the Session:** Use [Cancel In-Flight Turn](/cancel-in-flight-turn).

**You need create-or-signal on the first message:** Use [Session with Signal-and-Start](/session-signal-and-start).

**You need lower first-Turn start latency:** Use [Eager Interactive Session Start](/eager-interactive-session-start).

**You need one agent Workflow per business entity:** Use [Entity Agent](/entity-agent).

**You need to release idle chat Sessions or sandboxes:** Use [Session Idle Eviction](/session-idle-eviction).

**You need to reset history while keeping session identity:** Use [Continue-As-New Session](/continue-as-new-session).

**You need proactive or recurring agent cycles:** Use [Scheduled Agent Turns](/scheduled-agent-turns).

**You need an operator playbook for stuck Sessions:** Use [Operator Session Reset](/operator-session-reset).

**You need Sessions that must finish without parking for a human:** Use [Task-Mode Session](/task-mode-session).

**You need Session owner ≠ latest Delivery caller:** Use [Initiator vs Current Principal](/initiator-vs-current-principal).

## Related Sections

See [Versioning](/versioning) for pins and rollouts, and [Channels](/channels) for how messages enter a Session.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
