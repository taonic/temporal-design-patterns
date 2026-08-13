<h1>Tools <img src="/images/child-workflows-icon.svg" alt="Tools" class="pattern-page-icon"></h1>

How agents invoke side effects: Activity, Workflow, Callback, Nexus, and tool-loop mechanics.

## Patterns in This Section

<div class="pattern-grid">
<div class="pattern-tile">
<a href="activity-tool">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Activity Tool">
<span>Activity Tool</span>
</div>
<p>Side-effecting tools as durable Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="workflow-tool">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Workflow Tool">
<span>Workflow Tool</span>
</div>
<p>Deterministic tools as in-Workflow code.</p>
</a>
</div>
<div class="pattern-tile">
<a href="callback-tool">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Callback Tool">
<span>Callback Tool</span>
</div>
<p>Tools that run on an attached client.</p>
</a>
</div>
<div class="pattern-tile">
<a href="nexus-tool">
<div class="pattern-tile-header">
<img src="/images/worker-specific-taskqueue-icon.svg" alt="Nexus Tool">
<span>Nexus Tool</span>
</div>
<p>Cross-Namespace tools via Temporal Nexus Operations.</p>
</a>
</div>
<div class="pattern-tile">
<a href="typed-agent-operations">
<div class="pattern-tile-header">
<img src="/images/request-response-icon.svg" alt="Typed Agent Operations">
<span>Typed Agent Operations</span>
</div>
<p>Versioned Update/Query contracts between agents.</p>
</a>
</div>
<div class="pattern-tile">
<a href="agent-tool-loop">
<div class="pattern-tile-header">
<img src="/images/polling-icon.svg" alt="Agent Tool Loop">
<span>Agent Tool Loop</span>
</div>
<p>Durable model↔tool loop until a final reply.</p>
</a>
</div>
<div class="pattern-tile">
<a href="on-demand-skill-load">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="On-Demand Skill Load">
<span>On-Demand Skill Load</span>
</div>
<p>Load Skill bodies into a Turn only when needed.</p>
</a>
</div>
<div class="pattern-tile">
<a href="effect-classified-tools">
<div class="pattern-tile-header">
<img src="/images/local-activities-icon.svg" alt="Effect-Classified Tools">
<span>Effect-Classified Tools</span>
</div>
<p>Declare pure, state, or external Tool effects.</p>
</a>
</div>
<div class="pattern-tile">
<a href="connection-discovery">
<div class="pattern-tile-header">
<img src="/images/signal-with-start-icon.svg" alt="Connection Discovery">
<span>Connection Discovery</span>
</div>
<p>Search connections then call qualified Tools.</p>
</a>
</div>
<div class="pattern-tile">
<a href="model-output-projection">
<div class="pattern-tile-header">
<img src="/images/event-accumulator-icon.svg" alt="Model-Output Projection">
<span>Model-Output Projection</span>
</div>
<p>Full Tool results for UI; projection for the model.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tool-retry-profiles">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tool Retry Profiles">
<span>Tool Retry Profiles</span>
</div>
<p>Per-tool retry and safety policies.</p>
</a>
</div>
<div class="pattern-tile">
<a href="poison-tool-quarantine">
<div class="pattern-tile-header">
<img src="/images/non-retryable-errors-icon.svg" alt="Poison Tool Quarantine">
<span>Poison Tool Quarantine</span>
</div>
<p>Stop poison tool retry storms with non-retryable classification.</p>
</a>
</div>
<div class="pattern-tile">
<a href="heartbeat-long-steps">
<div class="pattern-tile-header">
<img src="/images/long-running-activity-icon.svg" alt="Heartbeat Long Steps">
<span>Heartbeat Long Steps</span>
</div>
<p>Heartbeats for long-running tool/model Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="local-activity-tools">
<div class="pattern-tile-header">
<img src="/images/local-activities-icon.svg" alt="Local Activity Tools">
<span>Local Activity Tools</span>
</div>
<p>Low-latency tools as Local Activities.</p>
</a>
</div>
<div class="pattern-tile">
<a href="fast-slow-tool-retries">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Fast/Slow Tool Retries">
<span>Fast/Slow Tool Retries</span>
</div>
<p>Separate fast local retries from slow durable ones.</p>
</a>
</div>
<div class="pattern-tile">
<a href="external-tool-polling">
<div class="pattern-tile-header">
<img src="/images/polling-icon.svg" alt="External Tool Polling">
<span>External Tool Polling</span>
</div>
<p>Poll external jobs without blocking Workers forever.</p>
</a>
</div>
<div class="pattern-tile">
<a href="tool-compensation">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tool Compensation">
<span>Tool Compensation</span>
</div>
<p>Compensate or undo tool side effects.</p>
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

**You need durable side-effecting tools:** Use [Activity Tool](/activity-tool).

**You need deterministic in-Workflow tools:** Use [Workflow Tool](/workflow-tool).

**You need tools that run on an attached client:** Use [Callback Tool](/callback-tool).

**You need cross-Namespace tools:** Use [Nexus Tool](/nexus-tool).

**You need versioned Update/Query contracts:** Use [Typed Agent Operations](/typed-agent-operations).

**You need a durable model↔tool loop:** Use [Agent Tool Loop](/agent-tool-loop).

**You need per-tool retry and safety policies:** Use [Tool Retry Profiles](/tool-retry-profiles).

**You need to stop poison tool retry storms:** Use [Poison Tool Quarantine](/poison-tool-quarantine).

**You need heartbeats for long Steps:** Use [Heartbeat Long Steps](/heartbeat-long-steps).

**You need low-latency Local Activity tools:** Use [Local Activity Tools](/local-activity-tools).

**You need fast vs slow retry lanes:** Use [Fast/Slow Tool Retries](/fast-slow-tool-retries).

**You need to poll external jobs safely:** Use [External Tool Polling](/external-tool-polling).

**You need to undo tool side effects:** Use [Tool Compensation](/tool-compensation).

**You need to compile MCP/OpenAPI catalogs into Activities:** Use [MCP / OpenAPI Tooling](/mcp-openapi-tooling).

**You need progressive Skill bodies without bloating every Turn:** Use [On-Demand Skill Load](/on-demand-skill-load).

**You need pure/state/external Tool dispatch:** Use [Effect-Classified Tools](/effect-classified-tools).

**You need search-then-load connection Tools:** Use [Connection Discovery](/connection-discovery).

**You need rich channel Tool results and short model views:** Use [Model-Output Projection](/model-output-projection).

## Related Sections

See [Model Calls](/model-calls) for LLM Activities and [Safety](/safety) for tool safety profiles.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
