/**
 * Express launcher API for the integrated Vitepress runner.
 *
 * Vitepress proxies /api/* to this server during `npm run docs:dev`. Each
 * request is scoped to a (pattern, language) pair backed by `pattern.json`.
 */

import path from "node:path";

import express, { type Request, type Response } from "express";

import { SandboxManager, listPatterns } from "./manager.js";

const PORT = Number(process.env.PORT ?? 8787);
const HOST = process.env.HOST ?? "127.0.0.1";
const DOCS_DIST_DIR = process.env.DOCS_DIST_DIR;

const manager = new SandboxManager();
const app = express();
app.use(express.json({ limit: "1mb" }));

function requireParam(req: Request, name: string): string | null {
  const fromQuery = req.query[name];
  const fromBody = (req.body ?? {})[name];
  const value = (fromQuery ?? fromBody) as string | undefined;
  return typeof value === "string" && value.length > 0 ? value : null;
}

app.get("/api/health", (_req, res) => {
  res.json({ ok: true });
});

app.get("/api/patterns", async (_req, res) => {
  try {
    const patterns = await listPatterns();
    res.json(
      patterns.map(({ id, manifest }) => ({
        id,
        name: manifest.name,
        languages: Object.entries(manifest.languages).map(([key, lang]) => ({
          id: key,
          label: lang.label,
        })),
      })),
    );
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

app.get("/api/files", async (req: Request, res: Response) => {
  const pattern = requireParam(req, "pattern");
  const language = requireParam(req, "language");
  if (!pattern || !language) {
    res.status(400).json({ error: "pattern and language are required" });
    return;
  }
  try {
    res.json(await manager.getEditableFiles(pattern, language));
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

app.get("/api/launch", async (req: Request, res: Response) => {
  const pattern = requireParam(req, "pattern");
  const language = requireParam(req, "language");
  if (!pattern || !language) {
    res.status(400).json({ error: "pattern and language are required" });
    return;
  }

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache, no-transform");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("X-Accel-Buffering", "no");
  res.flushHeaders();

  const send = (kind: string, payload: unknown) => {
    res.write(`data: ${JSON.stringify({ kind, payload })}\n\n`);
  };

  const events = {
    log: (msg: string) => send("log", msg),
    spinner: (text: string | null) => send("spinner", text),
  };
  let aborted = false;
  req.on("close", () => {
    aborted = true;
  });

  try {
    const result = await manager.launch(pattern, language, events, (ui) => {
      if (!aborted) send("ui", ui);
    });
    if (!aborted) send("result", result);
  } catch (err) {
    if (!aborted) send("error", (err as Error).message);
  } finally {
    if (!aborted) {
      send("done", null);
      res.end();
    }
  }
});

app.post("/api/run", async (req: Request, res: Response) => {
  const { sandboxId, pattern, language, files } = req.body as {
    sandboxId?: string;
    pattern?: string;
    language?: string;
    files?: Record<string, string>;
  };
  if (!sandboxId || !pattern || !language || !files || typeof files !== "object") {
    res
      .status(400)
      .json({ error: "sandboxId, pattern, language, and files are required" });
    return;
  }

  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache, no-transform");
  res.setHeader("Connection", "keep-alive");
  res.setHeader("X-Accel-Buffering", "no");
  res.flushHeaders();

  const send = (kind: string, payload: unknown) => {
    res.write(`data: ${JSON.stringify({ kind, payload })}\n\n`);
  };
  const events = {
    log: (msg: string) => send("log", msg),
    spinner: (text: string | null) => send("spinner", text),
  };

  try {
    const output = await manager.runEdited(
      sandboxId,
      pattern,
      language,
      files,
      events,
    );
    send("result", { workflowResult: output });
  } catch (err) {
    send("error", (err as Error).message);
  } finally {
    send("done", null);
    res.end();
  }
});

app.post("/api/stop", async (req: Request, res: Response) => {
  const { sandboxId } = req.body as { sandboxId?: string };
  if (!sandboxId) {
    res.status(400).json({ error: "sandboxId required" });
    return;
  }
  try {
    await manager.stop(sandboxId);
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

// Serve the built VitePress site from the same origin so DaytonaRunner.vue's
// relative /api/* calls work without CORS. Set in fly.toml; unset locally,
// where vitepress dev proxies /api to this server instead.
if (DOCS_DIST_DIR) {
  app.use(express.static(DOCS_DIST_DIR, { extensions: ["html"] }));
  app.get(/^\/(?!api\/).*/, (_req, res) => {
    res.sendFile(path.join(DOCS_DIST_DIR, "index.html"));
  });
}

app.listen(PORT, HOST, () => {
  console.log(`Sandbox runner API listening on http://${HOST}:${PORT}`);
});
