<h1>On-Demand Skill Load <img src="/images/child-workflows-icon.svg" alt="On-Demand Skill Load" class="pattern-page-icon"></h1>

## Overview

The On-Demand Skill Load pattern keeps Skill **descriptions** in the always-on catalog and loads a Skill’s full procedure body into the active Turn only when the model calls a load Tool—then drops that body on compaction so it does not become permanent history weight.
Primitives used: Skill catalog (name + description + body digest), Activity-backed load, Catalog Snapshot Pinning, Context Compaction, Agent Tool Loop.

## Problem

If every procedure ships in system instructions, prompts bloat and every Turn pays for unused Skills.
If Workers `open("skill.md")` inside the tool loop without an Activity, replay breaks and mid-park deploys mutate behavior.

## Solution

1. Advertise Skills as descriptions (and digests) in the pinned catalog.
2. Expose a `load_skill` Tool that fetches the body via Activity (or baked Worker build) and appends it to the **current Turn** context.
3. Do not treat Skill load as adding Tools—only instructions for this Turn.
4. On compaction, drop loaded Skill bodies; keep digests / names if still relevant.

```mermaid
flowchart LR
    Catalog[Skill descriptions] --> Model[Model Step]
    Model -->|load_skill| Act[Load Activity]
    Act --> Body[Skill body in Turn context]
    Body --> Loop[Continue tool loop]
    Loop --> Compact[Compaction drops bodies]
```

The following describes each step in the diagram:

1. The Turn starts with descriptions only.
2. The model selects `load_skill` when a procedure is needed.
3. An Activity returns the body (from snapshot or registry).
4. Later compaction removes bodies while preserving Session identity and digests.

```python
from datetime import timedelta

from temporalio import workflow

@workflow.defn
class AgentTurnWorkflow:
    @workflow.run
    async def run(self, session_id: str, catalog_snapshot_id: str, user_message: str) -> str:
        context = {"skills_loaded": []}
        # model selects load_skill("deploy") …
        body = await workflow.execute_activity(
            load_skill_body,
            args=[catalog_snapshot_id, "deploy"],
            start_to_close_timeout=timedelta(seconds=30),
        )
        context["skills_loaded"].append({"name": "deploy", "body": body})
        return await workflow.execute_activity(
            call_model_with_context,
            args=[user_message, context],
            start_to_close_timeout=timedelta(seconds=60),
        )
```

## Implementation

<DaytonaRunner pattern="on-demand-skill-load" />

### Baked vs registry

| Mode | Body source | Replay |
| :--- | :--- | :--- |
| Baked | Worker build / snapshot blob | Stable with [Catalog Snapshot Pinning](/catalog-snapshot-pinning) |
| Registry | External Activity fetch by digest | Record Activity result; never raw disk in Workflow |

### Scope

Skills are scoped per agent definition.
Do not silently share parent Skill bodies into child Sessions unless the child catalog includes them.

### Safety

Loading a Skill does not bypass [Approval-Gated Tools](/approval-gated-tools) or [Safety-Profiled Tools](/safety-profiled-tools).
It only adds instructions.

## When to use

Use when agents have many procedures and only a few apply per Turn.
Skip when the entire catalog fits comfortably and never changes.

## Benefits and trade-offs

You shrink always-on prompts and keep progressive disclosure durable.
You need a load Tool, snapshot digests, and compaction rules so bodies do not accumulate forever.

## Comparison with alternatives

| Approach | Prompt size | Replay-safe |
| :--- | :--- | :--- |
| On-Demand Skill Load | Small + selective | Yes with Activity/snapshot |
| All Skills in system prompt | Large | Yes if pinned |
| Disk read in Workflow | Variable | No |

## Best practices

- **Descriptions always; bodies on demand.**
- **Pin digests** in the catalog snapshot.
- **Drop bodies on compaction** ([Compaction Tool-State Continuity](/compaction-tool-state-continuity)).
- **Offer `load_skill` only when Skills exist** in the agent catalog.

## Common pitfalls

- Stuffing Skill markdown into always-on instructions.
- Reading Skill files inside Workflow code.
- Expecting Skill load to register new Tools.
- Leaving loaded bodies in Session memory across Continue-As-New forever.

## Related patterns

- [Catalog Snapshot Pinning](/catalog-snapshot-pinning)
- [Context Compaction](/context-compaction)
- [Compaction Tool-State Continuity](/compaction-tool-state-continuity)
- [Filesystem Authoring](/filesystem-authoring)
- [Agent Tool Loop](/agent-tool-loop)
- [Dynamic Capability Resolution](/dynamic-capability-resolution)

## Sample code

- [`sandbox-runner/patterns/on-demand-skill-load/python/`](https://github.com/temporal-sa/temporal-agentic-patterns/tree/main/sandbox-runner/patterns/on-demand-skill-load/python)

## References

- [Temporal Docs: Activities](https://docs.temporal.io/activities)
- [Temporal Docs: Workflow deterministic constraints](https://docs.temporal.io/workflows#deterministic-constraints)
