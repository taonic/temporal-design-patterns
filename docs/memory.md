<h1>Memory <img src="/images/child-workflows-icon.svg" alt="Memory" class="pattern-page-icon"></h1>

What a Session remembers, compacts, externalizes, and claim-checks.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="session-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Session Memory">
<span>Session Memory</span>
</div>
<p>Durable conversational state in the Session.</p>
</a>
</div>
<div class="pattern-tile">
<a href="context-compaction">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Context Compaction">
<span>Context Compaction</span>
</div>
<p>Summarize history to keep model context bounded.</p>
</a>
</div>
<div class="pattern-tile">
<a href="cross-session-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Cross-Session Memory">
<span>Cross-Session Memory</span>
</div>
<p>Share memory across Sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="externalized-memory">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Externalized Memory">
<span>Externalized Memory</span>
</div>
<p>Store large memory outside Workflow history.</p>
</a>
</div>
<div class="pattern-tile">
<a href="claim-check-payloads">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Claim-Check Payloads">
<span>Claim-Check Payloads</span>
</div>
<p>Pass large blobs by reference, not in history.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need durable conversational state in the Session:** Use [Session Memory](/session-memory).

**You need to summarize history for bounded context:** Use [Context Compaction](/context-compaction).

**You need memory shared across Sessions:** Use [Cross-Session Memory](/cross-session-memory).

**You need large memory outside Workflow history:** Use [Externalized Memory](/externalized-memory).

**You need to pass large blobs by reference:** Use [Claim-Check Payloads](/claim-check-payloads).

## Related Sections

See [Sessions](/sessions) for where memory lives and [Model Calls](/model-calls) for context that consumes it.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
