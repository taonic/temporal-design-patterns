# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a documentation site cataloging design patterns for Temporal Workflows, built with [VitePress](https://vitepress.dev/) and published to GitHub Pages. Content is written in Markdown with embedded Mermaid diagrams. The site is at https://taonic.github.io/temporal-design-patterns.

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

- `docs/` — All pattern content as Markdown files, one file per pattern
- `docs/.vitepress/config.mts` — Site configuration: sidebar navigation, Mermaid plugin, search, vite proxy
- `docs/.vitepress/theme/components/DaytonaRunner.vue` — Integrated live-runner component embedded in pattern pages via `<DaytonaRunner pattern="..." />`. Reads `pattern.json` over `/api/patterns` to populate language tabs and uses CodeMirror with per-language syntax (TS via `@codemirror/lang-javascript`, Python via `@codemirror/lang-python`)
- `docs/.vitepress/dist/` — Generated static site output (git-ignored)
- `sandbox-runner/src/` — Express + Daytona launcher API (host side)
- `sandbox-runner/patterns/<pattern>/pattern.json` — Per-pattern manifest declaring supported languages and their `deps` file, source file order, `worker`/`starter` run commands, `workerProcessPattern` (used by `pkill -f` between runs), and optional `diskGib` / `memoryGib` resource overrides.
- `sandbox-runner/patterns/<pattern>/<language>/` — Per-language sources uploaded into the Daytona sandbox; each language directory owns its own deps file (`package.json` for TS, `pyproject.toml` for Python, `go.mod` + `go.sum` for Go, `pom.xml` for Java).
- `skills/validated-pattern-writing/` — A Claude skill for validating pattern drafts against the style guide

### Adding a language to an existing pattern

1. Create `sandbox-runner/patterns/<pattern>/<language>/` with the pattern's source files and a deps file.
2. Add a language entry to `pattern.json` (`deps`, `files`, `worker`, `starter`, `workerProcessPattern`, plus `diskGib` / `memoryGib` if the defaults of 1 / 2 GiB aren't enough).
3. If the language isn't already in `IMAGE_FACTORIES` in `sandbox-runner/src/manager.ts`, add an `Image` factory there. **For compiled languages (Go, Java), see "Build-cache warmup" below — first-run compile must finish before the starter timeout (~120 s).**
4. If the editor doesn't already syntax-highlight that language, add a `@codemirror/lang-*` package and a branch in `languageExtension()` in `DaytonaRunner.vue`.

### Build-cache warmup (compiled languages)

**Go** — runtime `go run worker.go workflows.go activities.go shared.go` would otherwise compile the SDK on every fresh launch (~90 s, races the starter timeout). To pre-warm:

- Commit `go.sum` next to `go.mod` (run `go mod tidy` locally to generate; without it, `go mod download` at image-build time produces an incomplete `go.sum` and runtime `go run` fails with "missing go.sum entry").
- Commit `warmup.go` next to `go.mod` — a stub `package main` that imports the SDK packages used (`activity`, `client`, `worker`, `workflow`). **Do not prefix with `_`** — Go's package loader filters leading-underscore files even when listed explicitly on the build command line, surfacing as "no Go files in /opt/app". The image factory deletes the file after building, so it never coexists with the user's source at runtime.
- The Go `IMAGE_FACTORIES` entry copies `warmup.go` into the snapshot, runs `go build -o /tmp/warmup warmup.go`, then deletes the binary and source. The compiled SDK archives stay in `~/.cache/go-build` and serve subsequent `go run` invocations.

**Java** — runtime `mvn compile exec:java -Dexec.mainClass=...` pays JVM startup, Maven plugin classloading, and a fresh javac invocation on every Run. To pre-warm:

- Commit `_warmup/Warmup.java` next to `pom.xml` — a minimal `public class Warmup` that holds a `Class<?>[]` field referencing `ActivityInterface`, `WorkflowInterface`, `WorkflowClient`, `WorkflowServiceStubs`, and `WorkerFactory` so javac eagerly resolves the SDK.
- The Java `IMAGE_FACTORIES` entry copies `_warmup/Warmup.java` into `src/main/java/Warmup.java`, runs `mvn -B dependency:go-offline` (downloads project + plugin deps), then `mvn -B compile` (validates the toolchain end-to-end and exercises plugin classloading), then `rm -rf target src/main/java/Warmup.java` so user uploads start with a clean tree.
- `dependency:go-offline` is more thorough than `dependency:resolve` + `dependency:resolve-plugins`: it also pulls plugin transitive deps. Without it, the first runtime `mvn compile` may still hit the network for plugin internals.

### Snapshot rebuild timeout

`daytona.create` defaults to a 60 s timeout, which is too short for first-time snapshot bakes that include a warmup compile. The manager passes `{ timeout: 1800 }` so the bake gets up to 30 minutes. Cached snapshots reuse the existing image and finish well under that.

### Adding a new pattern

1. Create `docs/<pattern-name>.md`
2. Add an entry to the appropriate sidebar section in `docs/.vitepress/config.mts`

### Sidebar categories (defined in config.mts)

| Category | Patterns |
| :--- | :--- |
| Distributed Transaction | Saga Pattern, Early Return |
| Stateful / Lifecycle | Entity Workflow, Request-Response via Updates, Continue-As-New, Child Workflows |
| Event-Driven | Signal with Start, Updatable Timer |
| Business Process | Approval, Delayed Start |
| Long-Running | Polling, Long Running Activity, Parallel Execution, Pick First (Race), Worker-Specific Task Queues |
| SDK Examples | Java, Go |

## Pattern Style Guide

All patterns follow a strict style defined in `skills/validated-pattern-writing/references/`. Key rules:

**Required sections (in order):** Title → Metadata → Introduction (Executive Summary, Problem Statement, Solution, Outcomes) → Background and Best Practices → Target Audience → Prerequisites → People and Process Considerations → Architecture Diagrams → Implementation Plan → Outcomes → Best Practices → Common Pitfalls → Related Resources

**Voice:** Second person throughout ("you will configure…"). No first-person singular or plural ("I", "we", "let's").

**Banned words:** simple/simply, easy/easily, just, straightforward, obviously, trivial, "dive into", "leverage" (use "use"), utilize, powerful, robust, seamless, and other assumptive or marketing language. Full list in `skills/validated-pattern-writing/references/style.md`.

**Diagrams:** Every pattern needs at least one Mermaid diagram (preferred) or SVG, followed by a numbered narrative walkthrough.

**Implementation phases:** Use descriptive headings, not "Step N — Gerund" format.

## Validated Pattern Writing Skill

Use `/validated-pattern-writing` (or the `validated-pattern-writing` skill) to validate a pattern draft against the full style guide. The skill checks structure, voice, banned words, Temporal terminology, and formatting, then groups findings as Errors / Warnings / Suggestions.

Word count utility: `skills/validated-pattern-writing/scripts/wordcount <file>`
