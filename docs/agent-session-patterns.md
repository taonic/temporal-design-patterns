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
<a href="session-signal-and-start">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session with Signal-and-Start">
<span>Session with Signal-and-Start</span>
</div>
<p>Create or signal a session from the first message.</p>
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
<a href="continue-as-new-session">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Continue-As-New Session">
<span>Continue-As-New Session</span>
</div>
<p>Reset history while preserving session identity.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need session workflow behavior:** One Workflow owns a session, memory, and event stream. Use [Session Workflow](/session-workflow).

**You need turn workflow behavior:** Isolate each turn as a child Workflow or sub-state. Use [Turn Workflow](/turn-workflow).

**You need session with signal-and-start behavior:** Create or signal a session from the first message. Use [Session with Signal-and-Start](/session-signal-and-start).

**You need entity agent behavior:** One long-lived agent Workflow per business entity. Use [Entity Agent](/entity-agent).

**You need continue-as-new session behavior:** Reset history while preserving session identity. Use [Continue-As-New Session](/continue-as-new-session).

## Related Sections

See Vernacular for Session, Turn, Step, and related terms used by these patterns.
