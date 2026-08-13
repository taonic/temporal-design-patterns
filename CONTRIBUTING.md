# Contributing to Temporal Agentic Patterns

This guide covers how to add or improve patterns in this catalog.

## Getting Started

### Prerequisites

Node.js v18 or later.

```bash
npm install          # install dependencies
npm run docs:dev     # start local dev server with hot reload
```

Open `http://localhost:5173/temporal-agentic-patterns/` to preview the site. The server reloads automatically as you edit files.

## Adding a New Pattern

1. Create `docs/<pattern-name>.md` following the [pattern structure](#pattern-structure) below.
2. Add an entry to the appropriate sidebar section in `docs/.vitepress/config.mts`.

### Sidebar Categories

See `docs/.vitepress/config.mts` for Concepts, Agent & Session, Tool & Model Call, Human-in-the-loop, Subagent, Code Mode, Safety, Memory, Observability, and Channel sections.

## Pattern Structure

Use this section order on every pattern page:

1. Title with `pattern-page-icon`
2. Overview
3. Problem
4. Solution (Mermaid + numbered walkthrough + Python)
5. Implementation (optional `<DaytonaRunner pattern="..." />`)
6. When to use
7. Benefits and trade-offs
8. Comparison with alternatives
9. Best practices
10. Common pitfalls
11. Related patterns
12. Sample code
13. References

### Voice

- Write in second person ("you configure…").
- Avoid first person ("I", "we", "let's").
- Avoid banned fluff: simple/simply, easy/easily, just, straightforward, obviously, trivial, "dive into", "leverage", utilize, powerful, robust, seamless.
- Prefer agent terms (Session, Turn, Step, Tool, Approval); use Temporal terms when durability requires them.
- Do not name third-party agent runtimes or protocol product brands in docs.

### Diagrams

Include at least one Mermaid diagram in Solution, followed by a numbered walkthrough.

## Live samples (optional)

1. Add `sandbox-runner/patterns/<pattern>/pattern.json` with a Python language block.
2. Add sources under `sandbox-runner/patterns/<pattern>/python/`.
3. Embed `<DaytonaRunner pattern="<pattern>" />` in Implementation.

Prefer deterministic stubs so samples run without model API keys.

## Pull Requests

- Keep changes focused on one pattern or a coherent set of related pages.
- Do not push agentic-catalog work to the Workflow design-patterns publication branch unless maintainers request it.
