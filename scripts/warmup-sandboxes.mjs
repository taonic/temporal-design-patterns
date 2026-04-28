#!/usr/bin/env node
// Post-deploy warmup: hits /api/launch for one pattern per language so each
// language's Daytona snapshot is baked and cached before real users arrive.
// Streams SSE, captures the sandboxId from the `ui` event, then stops the
// sandbox once the launch reports `result` or `error`.

const BASE = (process.env.WARMUP_BASE_URL ?? "").replace(/\/$/, "");
if (!BASE) {
  console.error("WARMUP_BASE_URL is required");
  process.exit(2);
}
const TIMEOUT_MS = Number(process.env.WARMUP_TIMEOUT_MS ?? 25 * 60 * 1000);

async function fetchPatterns() {
  const res = await fetch(`${BASE}/api/patterns`);
  if (!res.ok) throw new Error(`GET /api/patterns -> ${res.status}`);
  return res.json();
}

async function stopSandbox(sandboxId) {
  try {
    const res = await fetch(`${BASE}/api/stop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sandboxId }),
    });
    if (!res.ok) {
      console.warn(`stop ${sandboxId} -> ${res.status}`);
    }
  } catch (err) {
    console.warn(`stop ${sandboxId} failed: ${err.message}`);
  }
}

async function warmup({ pattern, language }) {
  const tag = `${pattern}/${language}`;
  console.log(`[${tag}] launching`);
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  let sandboxId = null;
  let result = null;
  let errored = null;

  try {
    const url = `${BASE}/api/launch?pattern=${encodeURIComponent(pattern)}&language=${encodeURIComponent(language)}`;
    const res = await fetch(url, {
      headers: { Accept: "text/event-stream" },
      signal: ctrl.signal,
    });
    if (!res.ok || !res.body) {
      throw new Error(`launch -> ${res.status}`);
    }

    const decoder = new TextDecoder();
    let buf = "";
    for await (const chunk of res.body) {
      buf += decoder.decode(chunk, { stream: true });
      let sep;
      while ((sep = buf.indexOf("\n\n")) !== -1) {
        const frame = buf.slice(0, sep);
        buf = buf.slice(sep + 2);
        const dataLine = frame.split("\n").find((l) => l.startsWith("data:"));
        if (!dataLine) continue;
        const json = dataLine.slice(5).trim();
        if (!json) continue;
        let evt;
        try {
          evt = JSON.parse(json);
        } catch {
          continue;
        }
        if (evt.kind === "ui" && evt.payload?.sandboxId) {
          sandboxId = evt.payload.sandboxId;
          console.log(`[${tag}] sandbox=${sandboxId}`);
        } else if (evt.kind === "result") {
          result = evt.payload;
          console.log(`[${tag}] workflow ok`);
        } else if (evt.kind === "error") {
          errored = String(evt.payload ?? "unknown error");
        }
      }
    }
  } finally {
    clearTimeout(timer);
    if (sandboxId) await stopSandbox(sandboxId);
  }

  if (errored) throw new Error(`[${tag}] ${errored}`);
  if (!result) throw new Error(`[${tag}] stream ended without result`);
}

const patterns = await fetchPatterns();
// One pattern per language is enough — IMAGE_FACTORIES are pattern-agnostic, so
// the cached snapshot serves every pattern that shares the language.
const seen = new Set();
const tasks = [];
for (const p of patterns) {
  for (const l of p.languages) {
    if (seen.has(l.id)) continue;
    seen.add(l.id);
    tasks.push({ pattern: p.id, language: l.id });
  }
}
console.log(`Warming ${tasks.length} language(s):`, tasks);

const results = await Promise.allSettled(tasks.map(warmup));
const failed = results.filter((r) => r.status === "rejected");
for (const r of failed) console.error(r.reason?.message ?? r.reason);
if (failed.length) {
  console.error(`${failed.length}/${tasks.length} warmups failed`);
  process.exit(1);
}
console.log(`All ${tasks.length} warmups completed`);
