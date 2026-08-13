<h1>Agent & Session Patterns <img src="/images/child-workflows-icon.svg" alt="Agent & Session Patterns" class="pattern-page-icon"></h1>

These patterns model long-lived agent sessions and how turns attach to them.

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
<a href="agent-definition-versioning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Agent Definition Versioning">
<span>Agent Definition Versioning</span>
</div>
<p>Pin definition and binding revisions per Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="catalog-snapshot-pinning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Catalog Snapshot Pinning">
<span>Catalog Snapshot Pinning</span>
</div>
<p>Pin tool/prompt catalog bytes so park cannot drift.</p>
</a>
</div>
<div class="pattern-tile">
<a href="binding-readiness-gate">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Binding Readiness Gate">
<span>Binding Readiness Gate</span>
</div>
<p>Fail closed when pinned queues or Nexus bindings are down.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-worker-versioning">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Agent Worker Versioning">
<span>Agent Worker Versioning</span>
</div>
<p>Pin Worker build / Deployment Version separately from config.</p>
</a>
</div>
<div class="pattern-tile">
<a href="patched-agent-workflow-evolution">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Patched Agent Workflow Evolution">
<span>Patched Agent Workflow Evolution</span>
</div>
<p>Evolve Session/Turn branching with workflow.patched.</p>
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

**You need session workflow behavior:** One Workflow owns a session, memory, and event stream. Use [Session Workflow](/session-workflow).

**You need turn workflow behavior:** Isolate each turn as a child Workflow or sub-state. Use [Turn Workflow](/turn-workflow).

**You need to abort an open Turn without ending the Session:** Use [Cancel In-Flight Turn](/cancel-in-flight-turn).

**You need session with signal-and-start behavior:** Create or signal a session from the first message. Use [Session with Signal-and-Start](/session-signal-and-start).

**You need lower first-Turn start latency:** Use [Eager Interactive Session Start](/eager-interactive-session-start).

**You need entity agent behavior:** One long-lived agent Workflow per business entity. Use [Entity Agent](/entity-agent).

**You need to release idle chat Sessions / sandboxes:** Use [Session Idle Eviction](/session-idle-eviction).

**You need continue-as-new session behavior:** Reset history while preserving session identity. Use [Continue-As-New Session](/continue-as-new-session).

**You need proactive or recurring agent cycles:** Use [Scheduled Agent Turns](/scheduled-agent-turns).

**You need reproducible agent config vs placement:** Use [Agent Definition Versioning](/agent-definition-versioning).

**You need catalog bytes pinned so long parks cannot drift:** Use [Catalog Snapshot Pinning](/catalog-snapshot-pinning).

**You need Session start/resume to fail closed when bindings are down:** Use [Binding Readiness Gate](/binding-readiness-gate).

**You need replay-safe Worker code rollouts for open Sessions:** Use [Agent Worker Versioning](/agent-worker-versioning).

**You need to change Workflow branching under open histories:** Use [Patched Agent Workflow Evolution](/patched-agent-workflow-evolution).

**You need an operator playbook for stuck Sessions:** Use [Operator Session Reset](/operator-session-reset).

## Related Sections

See Concepts for Session, Turn, Step, and related terms used by these patterns.
