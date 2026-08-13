# Temporal Agentic Patterns

> **Warning:** This catalog is under active development. Content and structure may change.

A catalog of design patterns for Temporal-native AI agents.

- [Contributing guide](CONTRIBUTING.md)

## Development

Install the project dependencies before running any commands:

```bash
npm install
```

Start a local development server to preview changes as you edit:

```bash
npm run docs:dev
```

The development server watches for file changes and reloads automatically.

Generate the static site output for production hosting:

```bash
npm run docs:build
```

After building, you can verify the production output locally:

```bash
npm run docs:preview
```

## Live runner (Daytona)

Pattern pages can include a `<DaytonaRunner pattern="..." />` component that
provisions a Daytona sandbox running a Temporal dev server, executes the
pattern's Python sample, and streams logs back. The dormant state is a single
button; the editor and console only appear once you toggle it on.

To run the live runner locally you need a `DAYTONA_KEY` env var. The
`npm run sandbox` script wraps the launcher in `bash -lc`, so adding
`export DAYTONA_KEY=...` to your `~/.profile` (or `~/.bash_profile`) is
enough — no need to re-export per-shell:

```bash
npm --prefix sandbox-runner install
echo 'export DAYTONA_KEY=<your-key>' >> ~/.profile  # or ~/.bash_profile
npm run dev          # docs:dev + sandbox launcher concurrently
```

The vitepress dev server proxies `/api/*` to the launcher on port 8787.
Without `DAYTONA_KEY` (or when running just `npm run docs:dev`), pattern
pages still render normally; the runner panel shows an inline note instead.

### Layout

| Path | Role |
| ---- | ---- |
| `sandbox-runner/src/server.ts` | Express + SSE API: `/api/patterns`, `/api/files`, `/api/launch`, `/api/run`, `/api/stop`. |
| `sandbox-runner/src/manager.ts` | Drives the Daytona sandbox lifecycle (Python image factory). |
| `sandbox-runner/patterns/<pattern>/pattern.json` | Manifest declaring Python sources and `worker` / `starter` run commands. |
| `sandbox-runner/patterns/<pattern>/python/` | Sources uploaded into the sandbox. |
| `docs/.vitepress/theme/components/DaytonaRunner.vue` | Integrated runner component. |

## Deployment

Publish this catalog from a dedicated `temporal-agentic-patterns` repository.
Do not push agentic-catalog content to the Workflow design-patterns `main` branch.
