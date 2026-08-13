# CLAUDE.md

This file provides guidance when working with code in this repository.

## Project Overview

This is a documentation site cataloging **design patterns for Temporal-native AI agents**, built with [VitePress](https://vitepress.dev/). Content is Markdown with Mermaid diagrams. Samples are **Python only**.

Public docs teach patterns and agent vernacular only. Do not name third-party agent runtimes or protocol product brands in reader-facing Markdown, Sample code, or References.

## Commands

```bash
npm install           # Install dependencies
npm run docs:dev      # Start local dev server with hot reload
npm run docs:build    # Build static site to docs/.vitepress/dist
npm run docs:preview  # Preview production build locally

# Live-runner workflow (requires DAYTONA_KEY env var):
npm --prefix sandbox-runner install
npm run sandbox       # Start the Daytona launcher API on :8787
npm run dev           # Run docs:dev + sandbox concurrently
```

There are no test or lint commands.

## Architecture

- `docs/` — Pattern and vernacular content as Markdown
- `docs/.vitepress/config.mts` — Sidebar, Mermaid, search, `/api` proxy
- `docs/.vitepress/theme/components/DaytonaRunner.vue` — Live runner (`pattern="..."`)
- `sandbox-runner/src/` — Express + Daytona launcher (host is Node; samples are Python)
- `sandbox-runner/patterns/<pattern>/pattern.json` — Python-only language block
- `sandbox-runner/patterns/<pattern>/python/` — Sample sources
- `sandbox-runner/runtime/python/` — Shared `pyproject.toml` baked into snapshots

## Pattern Style Guide

Match the Workflow design-patterns catalog voice and section order.

**Required sections (in order):**

1. `<h1>{Name} … <img class="pattern-page-icon">`
2. `## Overview`
3. `## Problem`
4. `## Solution` — Mermaid + numbered walkthrough + Python code
5. `## Implementation` — DaytonaRunner when runnable; descriptive `###` subsections
6. `## When to use`
7. `## Benefits and trade-offs`
8. `## Comparison with alternatives`
9. `## Best practices`
10. `## Common pitfalls`
11. `## Related patterns`
12. `## Sample code` — links into this repo and Temporal docs only
13. `## References` — Temporal docs / general reading only

**Voice:** Second person ("you configure…"). No first-person singular or plural ("I", "we", "let's").

**Banned words:** simple/simply, easy/easily, just, straightforward, obviously, trivial, "dive into", "leverage" (use "use"), utilize, powerful, robust, seamless, and other assumptive or marketing language.

**Diagrams:** Every pattern needs at least one Mermaid diagram, followed by a numbered narrative walkthrough.

**Implementation headings:** Use descriptive headings, not "Step N — Gerund" format.

**Terminology:** Prefer agent vernacular (Session, Turn, Step, Tool, Approval) in the main narrative; use Temporal terms (Workflow, Activity, Signal, Continue-As-New) when durability mechanics require them.

## Adding a new pattern

1. Create `docs/<pattern-name>.md` using the section order above
2. Add a sidebar entry in `docs/.vitepress/config.mts`
3. Optionally add `sandbox-runner/patterns/<pattern>/` with Python sources and `pattern.json`
