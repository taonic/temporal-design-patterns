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
```

There are no test or lint commands.

## Architecture

- `docs/` — All pattern content as Markdown files, one file per pattern
- `docs/.vitepress/config.mts` — Site configuration: sidebar navigation, Mermaid plugin, search
- `docs/.vitepress/dist/` — Generated static site output (git-ignored)
- `skills/validated-pattern-writing/` — A Claude skill for validating pattern drafts against the style guide

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
