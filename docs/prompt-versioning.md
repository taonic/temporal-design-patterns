<h1>Prompt Versioning <img src="/images/continue-as-new-icon.svg" alt="Prompt Versioning" class="pattern-page-icon"></h1>

## Overview

The Prompt Versioning pattern treats system prompts and tool instructions as versioned artifacts referenced by Durable Model Calls so behavior is reproducible and safe to change while Sessions are open.
Primitives used: Durable Model Call inputs, Workflow versioning or explicit prompt_id, evals.

## Problem

Editing a prompt string in place changes in-flight Sessions unpredictably and makes evals non-reproducible.

## Solution

Store prompts under stable IDs/versions (files or config).
Pass `prompt_id` + `prompt_version` into model Activities.
Use Temporal Worker Versioning or an explicit pin in Session state when behavior must not change mid-session.

```mermaid
flowchart LR
    Files[Versioned prompts] --> Pin[Session pin]
    Pin --> Act[Model Activity]
    Act --> Eval[Eval fixtures]
```

The following describes each step in the diagram:

1. Authors commit prompt files with versions.
2. A Session pins a prompt version at start (or inherits worker deployment version).
3. Model Activities load that exact prompt text.
4. Evals reference the same IDs for reproducibility.

```python
PROMPTS = {
    ("researcher", "v3"): "You are a careful researcher...",
}

@activity.defn
async def call_llm(model: str, prompt_id: str, prompt_version: str, user: str) -> str:
    system = PROMPTS[(prompt_id, prompt_version)]
    return await provider.complete(model, system, user)
```

## Implementation

### Mid-session changes

Prefer pinning at session start.
If you must change prompts for open Sessions, use explicit versioning APIs or Continue-As-New onto new code with a recorded decision event.

### Evals

Fixtures should assert prompt_version in events or inputs.

## When to use

Use for any production agent whose prompt affects safety or revenue.
Hard-coded strings are acceptable only for throwaway demos.

## Benefits and trade-offs

You can reproduce and roll back behavior.
You maintain a prompt catalog beside code.

## Comparison with alternatives

| Approach | Reproducible | Safe for in-flight |
| :--- | :--- | :--- |
| Versioned prompt IDs | Yes | Yes if pinned |
| Mutable shared string | No | No |
| Prompt in DB without version | Weak | Risky |

## Best practices

- **Include prompt_version in model_call events.**
- **Review prompt changes like code.**
- **Run evals before promoting a new version.**

## Common pitfalls

- **Hot-editing prod prompts without pins.**
- **Different workers resolving different file contents for the same version label.**
- **Full prompt text in Workflow or Activity args.** Pass prompt_id and version; load text in the Worker or from versioned storage.
- **Worker Versioning alone while prompts load from mutable storage.** Pin prompt versions in Session state or you still drift mid-session.

## Related patterns

- [Durable Model Call](/durable-model-call)
- [Eval-Backed Behavior Checks](/eval-backed-behavior-checks)
- [Continue-As-New Session](/continue-as-new-session)

## Sample code

See related runnable samples under `sandbox-runner/patterns/` when this pattern builds on Session Workflow, Activity Tool, or Code Mode.

## References

- [Temporal Docs: Versioning](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning)
