<h1>Channels <img src="/images/child-workflows-icon.svg" alt="Channels" class="pattern-page-icon"></h1>

HTTP and messaging ingress, delivery ledgers, and capability-separated handles.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="http-channel-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="HTTP Channel Agent">
<span>HTTP Channel Agent</span>
</div>
<p>Expose a session API over HTTP and SSE.</p>
</a>
</div>
<div class="pattern-tile">
<a href="messaging-channel-agent">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Messaging Channel Agent">
<span>Messaging Channel Agent</span>
</div>
<p>Map Slack or email into sessions.</p>
</a>
</div>
<div class="pattern-tile">
<a href="idempotent-delivery">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Idempotent Delivery">
<span>Idempotent Delivery</span>
</div>
<p>Dedupe channel retries with a durable delivery ledger.</p>
</a>
</div>
<div class="pattern-tile">
<a href="validated-session-ingress">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Validated Session Ingress">
<span>Validated Session Ingress</span>
</div>
<p>Reject bad deliveries in Update validators before Turns.</p>
</a>
</div>
<div class="pattern-tile">
<a href="split-resume-observe-handles">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Split Resume and Observe Handles">
<span>Split Resume and Observe Handles</span>
</div>
<p>Separate write tokens from observe/stream credentials.</p>
</a>
</div>
<div class="pattern-tile">
<a href="delivery-authorization-timing">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Delivery Authorization Timing">
<span>Delivery Authorization Timing</span>
</div>
<p>Re-check auth at apply, not only at channel accept.</p>
</a>
</div>
<div class="pattern-tile">
<a href="mid-turn-delivery-coalescing">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Mid-Turn Delivery Coalescing">
<span>Mid-Turn Delivery Coalescing</span>
</div>
<p>Fold queued same-initiator Deliveries into the next Turn.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need a session API over HTTP and SSE:** Use [HTTP Channel Agent](/http-channel-agent).

**You need to map Slack or email into Sessions:** Use [Messaging Channel Agent](/messaging-channel-agent).

**You need retry-safe channel posts without double Turns:** Use [Idempotent Delivery](/idempotent-delivery).

**You need schema/auth rejection before Turn enqueue:** Use [Validated Session Ingress](/validated-session-ingress).

**You need write credentials separate from stream/watch links:** Use [Split Resume and Observe Handles](/split-resume-observe-handles).

**You need auth re-checked when a queued Delivery applies:** Use [Delivery Authorization Timing](/delivery-authorization-timing).

**You need mid-Turn messages folded into the next Turn:** Use [Mid-Turn Delivery Coalescing](/mid-turn-delivery-coalescing).

## Related Sections

See [Human Interaction](/human-interaction) for connection-auth waits and [Sessions](/sessions) for Session create semantics.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
