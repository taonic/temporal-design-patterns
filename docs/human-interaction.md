<h1>Human Interaction <img src="/images/child-workflows-icon.svg" alt="Human Interaction" class="pattern-page-icon"></h1>

Pause Turns for approvals, clarifying answers, connection grants, and operator commands.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="approval-gated-tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Approval-Gated Tools">
<span>Approval-Gated Tools</span>
</div>
<p>Require approval before risky tools run.</p>
</a>
</div>
<div class="pattern-tile">
<a href="failure-triggered-approval">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Failure-Triggered Approval">
<span>Failure-Triggered Approval</span>
</div>
<p>Escalate only after sandboxed Tool denials.</p>
</a>
</div>
<div class="pattern-tile">
<a href="ask-user-wait">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Ask-User Wait">
<span>Ask-User Wait</span>
</div>
<p>Park a Turn for clarifying user input mid-loop.</p>
</a>
</div>
<div class="pattern-tile">
<a href="connection-auth-wait">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Connection Auth Wait">
<span>Connection Auth Wait</span>
</div>
<p>Park for OAuth/connection consent; store tokens off-history.</p>
</a>
</div>
<div class="pattern-tile">
<a href="session-scoped-approvals">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session-Scoped Approvals">
<span>Session-Scoped Approvals</span>
</div>
<p>Approve a tool for the rest of a session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="updatable-approval-timer">
<div class="pattern-tile-header">
<img src="/images/updatable-timer-icon.svg" alt="Updatable Approval Timer">
<span>Updatable Approval Timer</span>
</div>
<p>Extendable SLA deadlines for approval waits.</p>
</a>
</div>
<div class="pattern-tile">
<a href="resumable-correction">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Resumable Correction">
<span>Resumable Correction</span>
</div>
<p>Park after repeated failures until a human fixes inputs.</p>
</a>
</div>
<div class="pattern-tile">
<a href="operator-slash-commands">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Operator Slash Commands">
<span>Operator Slash Commands</span>
</div>
<p>Deterministic textual commands inside the session.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need approval before risky tools run:** Use [Approval-Gated Tools](/approval-gated-tools).

**You need clarifying answers mid-Turn:** Use [Ask-User Wait](/ask-user-wait).

**You need OAuth/connection consent without secrets in history:** Use [Connection Auth Wait](/connection-auth-wait).

**You need to approve a tool for the rest of a Session:** Use [Session-Scoped Approvals](/session-scoped-approvals).

**You need extendable approval SLAs:** Use [Updatable Approval Timer](/updatable-approval-timer).

**You need to park until a human fixes bad inputs:** Use [Resumable Correction](/resumable-correction).

**You need deterministic textual operator commands:** Use [Operator Slash Commands](/operator-slash-commands).

**You need Approvals only after Sandbox denials:** Use [Failure-Triggered Approval](/failure-triggered-approval).

## Related Sections

See [Channels](/channels) for delivery of answers and [Tools](/tools) for approval-gated execution.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
