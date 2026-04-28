# Temporal Design Patterns

> **Warning:** This catalog is under active development. Content and structure may change.
>
> **Personal project by [@taonic](https://github.com/taonic).**
>

A catalog of design patterns for Temporal Workflows.

- [View the live site](https://taonic.github.io/temporal-design-patterns)
- [View the full pattern catalog](docs/README.md)

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
pattern's code in the chosen language, and streams logs back. The dormant
state is a single button; the editor, language selector, and console only
appear once you toggle it on. Continue-As-New is wired up first in both
**TypeScript** and **Python** — see [docs/continue-as-new.md](docs/continue-as-new.md).

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
| `sandbox-runner/src/manager.ts` | Drives the Daytona sandbox lifecycle. Holds the per-language `Image` factories (Node 20 + `npm install` for TypeScript, `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` + `uv sync` for Python). |
| `sandbox-runner/patterns/<pattern>/pattern.json` | Manifest declaring supported languages, deps file, source file order, and `worker` / `starter` run commands. |
| `sandbox-runner/patterns/<pattern>/<language>/` | Per-language sources uploaded into the sandbox. |
| `docs/.vitepress/theme/components/DaytonaRunner.vue` | Integrated runner component (toggle, language selector, CodeMirror editor with per-language syntax, console + output panel). |

### Adding another language to an existing pattern

1. Drop the source files under `sandbox-runner/patterns/<pattern>/<language>/` along with a deps file.
2. Add a language entry to `pattern.json`. The `deps` field is the deps-file *basename* (e.g. `package.json`, `pyproject.toml`); the manager copies that file into the sandbox at the same name.
3. If the language is new to the runner, add an `Image` factory in `IMAGE_FACTORIES` (manager.ts) and a CodeMirror language extension in `languageExtension()` (DaytonaRunner.vue).

## Deployment

The site deploys to GitHub Pages automatically when you push changes to the main branch.

## Contributors

- [@taonic](https://github.com/taonic)
- [@darshitvvora](https://github.com/darshitvvora)
