<h1>Versioning <img src="/images/child-workflows-icon.svg" alt="Versioning" class="pattern-page-icon"></h1>

Pin definition, catalog, binding, Worker, and prompt revisions so parks and rollouts stay reproducible.

## Patterns in This Section

<div class="pattern-grid">
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
<a href="dynamic-capability-resolution">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Dynamic Capability Resolution">
<span>Dynamic Capability Resolution</span>
</div>
<p>Resolve Tools/Skills from principal then snapshot.</p>
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
<a href="prompt-versioning">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Versioning">
<span>Prompt Versioning</span>
</div>
<p>Version prompts separately from Workflow code.</p>
</a>
</div>
<div class="pattern-tile">
<a href="prompt-experiment-pins">
<div class="pattern-tile-header">
<img src="/images/continue-as-new-icon.svg" alt="Prompt Experiment Pins">
<span>Prompt Experiment Pins</span>
</div>
<p>Pin experiment variants for the life of a Session.</p>
</a>
</div>
</div>

## Choosing a Pattern

**You need reproducible agent config vs placement:** Use [Agent Definition Versioning](/agent-definition-versioning).

**You need catalog bytes pinned so long parks cannot drift:** Use [Catalog Snapshot Pinning](/catalog-snapshot-pinning).

**You need Session start to fail closed when bindings are down:** Use [Binding Readiness Gate](/binding-readiness-gate).

**You need replay-safe Worker code rollouts for open Sessions:** Use [Agent Worker Versioning](/agent-worker-versioning).

**You need to change Workflow branching under open histories:** Use [Patched Agent Workflow Evolution](/patched-agent-workflow-evolution).

**You need to version prompts without redeploying Workflows:** Use [Prompt Versioning](/prompt-versioning).

**You need to pin A/B prompt or model variants per Session:** Use [Prompt Experiment Pins](/prompt-experiment-pins).

**You need Tools/Skills resolved from principal then frozen:** Use [Dynamic Capability Resolution](/dynamic-capability-resolution).

## Related Sections

See [Sessions](/sessions) for lifecycle patterns and [Model Calls](/model-calls) / [Tools](/tools) for what those pins govern.

See Concepts for Session, Turn, Step, and related terms used by these patterns.
