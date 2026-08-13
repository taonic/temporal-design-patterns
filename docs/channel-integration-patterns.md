<h1>Channel & Integration Patterns <img src="/images/child-workflows-icon.svg" alt="Channel & Integration Patterns" class="pattern-page-icon"></h1>

These patterns bind agents to HTTP, messaging, and external tool catalogs.

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
<a href="mcp-openapi-tooling">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="MCP / OpenAPI Tooling">
<span>MCP / OpenAPI Tooling</span>
</div>
<p>Compile external tools into Activity tools.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need http channel agent behavior:** Expose a session API over HTTP and SSE. Use [HTTP Channel Agent](/http-channel-agent).

**You need messaging channel agent behavior:** Map Slack or email into sessions. Use [Messaging Channel Agent](/messaging-channel-agent).

**You need retry-safe channel posts without double Turns:** Use [Idempotent Delivery](/idempotent-delivery).

**You need schema/auth rejection before Turn enqueue:** Use [Validated Session Ingress](/validated-session-ingress).

**You need mcp / openapi tooling behavior:** Compile external tools into Activity tools. Use [MCP / OpenAPI Tooling](/mcp-openapi-tooling).

## Related Sections

See Concepts for Session, Turn, Step, and related terms used by these patterns.
