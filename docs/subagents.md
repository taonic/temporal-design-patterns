<h1>Subagents <img src="/images/child-workflows-icon.svg" alt="Subagents" class="pattern-page-icon"></h1>

Delegate work to child agents, fan-out, and remote agent boundaries.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="subagent-toolset">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Subagent Toolset">
<span>Subagent Toolset</span>
</div>
<p>Expose a child agent as a tool.</p>
</a>
</div>
<div class="pattern-tile">
<a href="root-mediated-subagent-approvals">
<div class="pattern-tile-header">
<img src="/images/approval-icon.svg" alt="Root-Mediated Subagent Approvals">
<span>Root-Mediated Subagent Approvals</span>
</div>
<p>Proxy child Approvals through the parent Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="persistent-subagent-threads">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Persistent Subagent Threads">
<span>Persistent Subagent Threads</span>
</div>
<p>Keep subagent Sessions across parent Turns.</p>
</a>
</div>
<div class="pattern-tile">
<a href="fanout-subagents">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Fan-Out Subagents">
<span>Fan-Out Subagents</span>
</div>
<p>Run many subagents in parallel.</p>
</a>
</div>
<div class="pattern-tile">
<a href="best-effort-parallel-tools">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Best-Effort Parallel Tools">
<span>Best-Effort Parallel Tools</span>
</div>
<p>Parallel tools with partial-success budgets.</p>
</a>
</div>
<div class="pattern-tile">
<a href="remote-subagent">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Remote Subagent">
<span>Remote Subagent</span>
</div>
<p>Cross-Namespace or remote agent delegation.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need to expose a child agent as a tool:** Use [Subagent Toolset](/subagent-toolset).

**You need subagent Sessions that survive parent Turns:** Use [Persistent Subagent Threads](/persistent-subagent-threads).

**You need many subagents in parallel:** Use [Fan-Out Subagents](/fanout-subagents).

**You need parallel tools with partial success:** Use [Best-Effort Parallel Tools](/best-effort-parallel-tools).

**You need cross-Namespace agent delegation:** Use [Remote Subagent](/remote-subagent).

**You need child Approvals on the parent human channel:** Use [Root-Mediated Subagent Approvals](/root-mediated-subagent-approvals).

## Related Sections

See [Tools](/tools) when a subagent is exposed as a tool, and [Sessions](/sessions) for parent Session lifecycle.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
