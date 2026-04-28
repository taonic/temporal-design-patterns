<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useData } from "vitepress";

import { EditorView, basicSetup } from "codemirror";
import { javascript } from "@codemirror/lang-javascript";
import { python } from "@codemirror/lang-python";
import { go } from "@codemirror/lang-go";
import { java } from "@codemirror/lang-java";
import { oneDark } from "@codemirror/theme-one-dark";
import { Compartment, type Extension } from "@codemirror/state";

type Status = "idle" | "checking" | "unavailable" | "launching" | "ready" | "running" | "error";

interface UiInfo {
  sandboxId: string;
  uiUrl: string;
}

interface LanguageOption {
  id: string;
  label: string;
}

const props = defineProps<{
  pattern?: string;
}>();

const patternId = computed(() => props.pattern ?? "continue-as-new");

const { isDark } = useData();

const open = ref(false);
const status = ref<Status>("idle");
const statusMessage = ref("");
const apiAvailable = ref<boolean | null>(null);

const languages = ref<LanguageOption[]>([]);
const activeLanguage = ref<string>("");

const files = ref<Record<string, string>>({});
const baseline = ref<Record<string, string>>({});
const fileOrder = ref<string[]>([]);
const activeFile = ref<string>("");

const sandboxId = ref<string | null>(null);
const uiInfo = ref<UiInfo | null>(null);

const logs = ref<string[]>([]);
const spinnerText = ref<string | null>(null);
const workflowOutput = ref<string>("");
const panelTab = ref<"console" | "output">("console");

const isClient = ref(false);
const editorEl = ref<HTMLElement | null>(null);
let editor: EditorView | null = null;
const themeCompartment = new Compartment();
const langCompartment = new Compartment();

const launching = computed(() => status.value === "launching");
const running = computed(() => status.value === "running");
const busy = computed(() => launching.value || running.value);
const canStop = computed(() => !!sandboxId.value && !launching.value);
const runDisabled = computed(
  () => busy.value || apiAvailable.value === false || !activeLanguage.value,
);
const runLabel = computed(() => {
  if (launching.value) return "Launching…";
  if (running.value) return "Running…";
  return "Run";
});

let currentEventSource: EventSource | null = null;

function languageExtension(lang: string): Extension {
  switch (lang) {
    case "python":
      return python();
    case "go":
      return go();
    case "java":
      return java();
    case "typescript":
    default:
      return javascript({ typescript: true });
  }
}

function tabLabel(filePath: string): string {
  const idx = filePath.lastIndexOf("/");
  return idx >= 0 ? filePath.slice(idx + 1) : filePath;
}

async function checkAvailability(): Promise<void> {
  if (apiAvailable.value !== null) return;
  status.value = "checking";
  try {
    const r = await fetch("/api/health", { method: "GET" });
    apiAvailable.value = r.ok;
    status.value = "idle";
    if (apiAvailable.value) {
      await loadPattern();
    }
  } catch {
    apiAvailable.value = false;
    status.value = "unavailable";
  }
}

async function loadPattern(): Promise<void> {
  try {
    const r = await fetch("/api/patterns");
    if (!r.ok) throw new Error(await r.text());
    const all = (await r.json()) as Array<{
      id: string;
      name: string;
      languages: LanguageOption[];
    }>;
    const found = all.find((p) => p.id === patternId.value);
    if (!found) {
      throw new Error(`Pattern '${patternId.value}' not found on the runner`);
    }
    languages.value = found.languages;
    if (!activeLanguage.value && languages.value.length > 0) {
      activeLanguage.value = languages.value[0].id;
    }
    await loadFiles();
  } catch (err) {
    appendLog(`Could not load pattern: ${(err as Error).message}`);
  }
}

async function loadFiles(): Promise<void> {
  if (!activeLanguage.value) return;
  try {
    const params = new URLSearchParams({
      pattern: patternId.value,
      language: activeLanguage.value,
    });
    const r = await fetch(`/api/files?${params}`);
    if (!r.ok) throw new Error(await r.text());
    const data = (await r.json()) as Record<string, string>;
    files.value = { ...data };
    baseline.value = { ...data };
    fileOrder.value = Object.keys(data);
    activeFile.value = fileOrder.value[0] ?? "";
    await nextTick();
    ensureEditor();
    syncEditorToActive();
    syncEditorLanguage();
  } catch (err) {
    appendLog(`Could not load files: ${(err as Error).message}`);
  }
}

async function selectLanguage(lang: string): Promise<void> {
  if (lang === activeLanguage.value || busy.value) return;
  // Switching languages always abandons the previous sandbox. Fire the stop
  // request in the background so the UI can swap immediately; clear local
  // state up front so a Run click during teardown doesn't target the
  // disappearing sandbox. Any orphan also gets auto-deleted by Daytona.
  if (sandboxId.value) {
    backgroundStop(sandboxId.value);
    sandboxId.value = null;
    uiInfo.value = null;
    status.value = "idle";
    statusMessage.value = "";
  }
  activeLanguage.value = lang;
  logs.value = [];
  workflowOutput.value = "";
  await loadFiles();
}

function backgroundStop(id: string): void {
  fetch("/api/stop", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sandboxId: id }),
  }).catch(() => {
    /* fire-and-forget: orphan sandboxes get auto-deleted by Daytona */
  });
}

function appendLog(line: string): void {
  logs.value.push(line);
}

// Daytona auto-deletes idle sandboxes; the cached sandboxId then points at
// nothing. When that happens, drop the cached id so the next click reverts to
// "Launch" instead of looping the same not-found error.
function clearStaleSandbox(message: string): boolean {
  if (!sandboxId.value) return false;
  if (!/not found/i.test(message)) return false;
  appendLog("Sandbox no longer exists — click Run to provision a new one.");
  sandboxId.value = null;
  uiInfo.value = null;
  return true;
}

function dirty(name: string): boolean {
  return files.value[name] !== baseline.value[name];
}

async function toggle(): Promise<void> {
  open.value = !open.value;
  if (open.value) {
    await checkAvailability();
    await nextTick();
    ensureEditor();
  }
}

function close(): void {
  open.value = false;
}

function runOrLaunch(): void {
  if (runDisabled.value) return;
  if (sandboxId.value) {
    void run();
  } else {
    launch();
  }
}

function launch(): void {
  if (busy.value || !activeLanguage.value) return;
  logs.value = [];
  spinnerText.value = null;
  workflowOutput.value = "";
  uiInfo.value = null;
  sandboxId.value = null;
  status.value = "launching";
  statusMessage.value = "Provisioning sandbox…";
  panelTab.value = "console";

  const params = new URLSearchParams({
    pattern: patternId.value,
    language: activeLanguage.value,
  });
  const es = new EventSource(`/api/launch?${params}`);
  currentEventSource = es;
  es.onmessage = (ev) => {
    const { kind, payload } = JSON.parse(ev.data);
    if (kind === "log") {
      appendLog(payload);
    } else if (kind === "spinner") {
      spinnerText.value = payload as string | null;
    } else if (kind === "ui") {
      uiInfo.value = payload;
      sandboxId.value = payload.sandboxId;
      statusMessage.value = "Temporal UI ready, running workflow…";
    } else if (kind === "result") {
      workflowOutput.value = payload.workflowResult || "(no output)";
      panelTab.value = "output";
      status.value = "ready";
      statusMessage.value = "Workflow completed";
      for (const name of Object.keys(files.value)) {
        baseline.value[name] = files.value[name];
      }
    } else if (kind === "error") {
      appendLog(`ERROR: ${payload}`);
      status.value = "error";
      statusMessage.value = "Launch failed";
    } else if (kind === "done") {
      es.close();
      currentEventSource = null;
      if (status.value === "launching") {
        status.value = sandboxId.value ? "ready" : "error";
      }
    }
  };
  es.onerror = () => {
    appendLog("Stream disconnected.");
    status.value = "error";
    statusMessage.value = "Stream disconnected";
    es.close();
    currentEventSource = null;
  };
}

async function run(): Promise<void> {
  if (!sandboxId.value || busy.value || !activeLanguage.value) return;
  status.value = "running";
  statusMessage.value = "Uploading edits and re-running worker…";
  spinnerText.value = null;
  workflowOutput.value = "";
  panelTab.value = "console";

  try {
    const resp = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sandboxId: sandboxId.value,
        pattern: patternId.value,
        language: activeLanguage.value,
        files: files.value,
      }),
    });
    if (!resp.ok || !resp.body) {
      throw new Error((await resp.text().catch(() => "")) || `HTTP ${resp.status}`);
    }
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf("\n\n")) !== -1) {
        const frame = buf.slice(0, idx).trim();
        buf = buf.slice(idx + 2);
        if (!frame.startsWith("data:")) continue;
        const { kind, payload } = JSON.parse(frame.slice(5).trim());
        if (kind === "log") {
          appendLog(payload);
        } else if (kind === "spinner") {
          spinnerText.value = payload as string | null;
        } else if (kind === "result") {
          workflowOutput.value = payload.workflowResult || "(no output)";
          panelTab.value = "output";
          status.value = "ready";
          statusMessage.value = "Run complete";
          for (const name of Object.keys(files.value)) {
            baseline.value[name] = files.value[name];
          }
        } else if (kind === "error") {
          appendLog(`ERROR: ${payload}`);
          status.value = "error";
          statusMessage.value = "Run failed";
          clearStaleSandbox(String(payload));
        }
      }
    }
  } catch (err) {
    const msg = (err as Error).message;
    appendLog(`Run failed: ${msg}`);
    status.value = "error";
    statusMessage.value = `Run failed: ${msg}`;
    clearStaleSandbox(msg);
  }
}

async function stop(): Promise<void> {
  if (!sandboxId.value) return;
  const id = sandboxId.value;
  statusMessage.value = "Stopping sandbox…";
  try {
    const r = await fetch("/api/stop", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sandboxId: id }),
    });
    if (!r.ok) throw new Error(await r.text());
    appendLog(`Sandbox ${id} deleted.`);
    sandboxId.value = null;
    uiInfo.value = null;
    status.value = "idle";
    statusMessage.value = "";
  } catch (err) {
    const msg = (err as Error).message;
    if (clearStaleSandbox(msg)) {
      // Already gone — treat Stop as a successful no-op.
      status.value = "idle";
      statusMessage.value = "";
      return;
    }
    appendLog(`Stop failed: ${msg}`);
    status.value = "error";
    statusMessage.value = "Stop failed";
  }
}

function themeExtensions(dark: boolean): Extension[] {
  return dark ? [oneDark] : [];
}

function ensureEditor(): void {
  if (editor || !editorEl.value || !activeFile.value) return;
  editor = new EditorView({
    doc: files.value[activeFile.value] ?? "",
    extensions: [
      basicSetup,
      langCompartment.of(languageExtension(activeLanguage.value)),
      themeCompartment.of(themeExtensions(isDark.value)),
      EditorView.theme({
        "&": { height: "100%", fontSize: "12.5px" },
        ".cm-scroller": { fontFamily: "var(--vp-font-family-mono)", lineHeight: "1.55" },
        ".cm-content": { padding: "10px 0" },
        ".cm-gutters": { background: "transparent" },
      }),
      EditorView.lineWrapping,
      EditorView.updateListener.of((u) => {
        if (u.docChanged && activeFile.value) {
          files.value[activeFile.value] = u.state.doc.toString();
        }
      }),
    ],
    parent: editorEl.value,
  });
}

function syncEditorToActive(): void {
  if (!editor || !activeFile.value) return;
  const next = files.value[activeFile.value] ?? "";
  if (editor.state.doc.toString() !== next) {
    editor.dispatch({
      changes: { from: 0, to: editor.state.doc.length, insert: next },
    });
  }
}

function syncEditorLanguage(): void {
  if (!editor) return;
  editor.dispatch({
    effects: langCompartment.reconfigure(languageExtension(activeLanguage.value)),
  });
}

watch(activeFile, () => syncEditorToActive());

watch(isDark, (dark) => {
  editor?.dispatch({ effects: themeCompartment.reconfigure(themeExtensions(dark)) });
});

watch(open, (val) => {
  if (!val && currentEventSource) {
    currentEventSource.close();
    currentEventSource = null;
  }
});

onMounted(() => {
  isClient.value = true;
});

onBeforeUnmount(() => {
  editor?.destroy();
  editor = null;
  currentEventSource?.close();
});
</script>

<template>
  <div class="daytona-runner">
    <div class="daytona-toggle-row">
      <button class="daytona-toggle" :class="{ active: open }" @click="toggle" type="button">
        <span class="daytona-toggle-icon">▶</span>
        <span>Run this pattern live</span>
      </button>
    </div>

    <Teleport to="body" :disabled="!isClient">
      <Transition name="daytona-slide">
        <div
          v-show="open"
          class="daytona-panel"
          role="dialog"
          aria-label="Live runner"
        >
          <div class="daytona-panel-header">
            <div class="daytona-panel-title">
              <span class="daytona-panel-icon">⏱</span>
              <span>Live runner</span>
              <span
                v-if="status !== 'idle'"
                class="daytona-status-pill"
                :class="`daytona-status-${status}`"
              >{{ statusMessage || status }}</span>
            </div>
            <div class="daytona-panel-actions">
              <button
                class="daytona-btn daytona-btn-primary"
                :disabled="runDisabled"
                @click="runOrLaunch"
                type="button"
              >{{ runLabel }}</button>
              <a
                v-if="uiInfo?.uiUrl"
                class="daytona-ui-button"
                :href="uiInfo.uiUrl"
                target="_blank"
                rel="noopener"
              >Open Temporal UI ↗</a>
              <button
                class="daytona-btn daytona-btn-ghost"
                :disabled="!canStop"
                @click="stop"
                type="button"
              >Stop</button>
              <button
                class="daytona-btn daytona-btn-icon"
                @click="close"
                type="button"
                aria-label="Close"
              >×</button>
            </div>
          </div>

          <div v-if="apiAvailable === false" class="daytona-banner">
            Sandbox launcher not reachable on <code>/api</code>. Run
            <code>npm run sandbox</code> in another terminal (and set
            <code>DAYTONA_KEY</code>) to enable live runs.
          </div>

          <template v-else-if="apiAvailable">
            <div v-if="languages.length > 1" class="daytona-language-bar">
              <button
                v-for="lang in languages"
                :key="lang.id"
                class="daytona-language-btn"
                :class="{ active: activeLanguage === lang.id }"
                :disabled="busy"
                @click="selectLanguage(lang.id)"
                type="button"
              >{{ lang.label }}</button>
            </div>

            <div class="daytona-tabs">
              <button
                v-for="name in fileOrder"
                :key="name"
                class="daytona-tab"
                :class="{ active: activeFile === name, dirty: dirty(name) }"
                @click="activeFile = name"
                :title="name"
                type="button"
              >{{ tabLabel(name) }}</button>
            </div>

            <div ref="editorEl" class="daytona-editor"></div>

            <div class="daytona-panel-tabs">
              <button
                class="daytona-panel-tab"
                :class="{ active: panelTab === 'console' }"
                @click="panelTab = 'console'"
                type="button"
              >Console</button>
              <button
                class="daytona-panel-tab"
                :class="{ active: panelTab === 'output' }"
                @click="panelTab = 'output'"
                type="button"
              >Output</button>
              <span v-if="sandboxId" class="daytona-sandbox-id">{{ sandboxId }}</span>
            </div>
            <pre v-show="panelTab === 'console'" class="daytona-pane"><template v-if="logs.length">{{ logs.join('\n') }}<template v-if="spinnerText">
<span class="daytona-spinner-line">{{ spinnerText }}</span></template></template><template v-else-if="spinnerText"><span class="daytona-spinner-line">{{ spinnerText }}</span></template><template v-else>Activity log streams here once you launch.</template></pre>
            <pre v-show="panelTab === 'output'" class="daytona-pane">{{ workflowOutput || 'Workflow output appears here after a successful run.' }}</pre>
          </template>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.daytona-runner {
  margin: 24px 0;
}

.daytona-toggle-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.daytona-toggle {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
  border: 1px solid transparent;
  color: #ffffff;
  padding: 10px 20px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  box-shadow: 0 2px 10px rgba(124, 58, 237, 0.28);
  transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease;
}
.daytona-toggle:hover, .daytona-toggle.active {
  filter: brightness(1.08);
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(219, 39, 119, 0.4);
}
.daytona-toggle:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(124, 58, 237, 0.3);
}
.daytona-toggle-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  font-size: 9px;
  color: #7c3aed;
  background: #ffffff;
  border-radius: 999px;
  padding-left: 1px;
}

.daytona-ui-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  color: #7c3aed;
  border: 1px solid #7c3aed;
  padding: 6px 13px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: background 120ms ease, color 120ms ease, border-color 120ms ease;
}
.daytona-ui-button:hover {
  background: rgba(124, 58, 237, 0.08);
  color: #7c3aed;
  border-color: #6d28d9;
  text-decoration: none;
}
.dark .daytona-ui-button {
  color: #c4b5fd;
  border-color: #a78bfa;
}
.dark .daytona-ui-button:hover {
  background: rgba(167, 139, 250, 0.12);
  color: #ddd6fe;
  border-color: #c4b5fd;
}
</style>

<style>
/* Unscoped: panel is teleported to <body> and must keep its styles. */
.daytona-panel {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: min(720px, 95vw);
  background: var(--vp-c-bg);
  border-left: 1px solid var(--vp-c-divider);
  box-shadow: -8px 0 32px rgba(0, 0, 0, 0.18);
  z-index: 100;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-size: 13px;
  color: var(--vp-c-text-1);
}

.daytona-slide-enter-active, .daytona-slide-leave-active {
  transition: transform 240ms cubic-bezier(0.2, 0, 0.2, 1);
}
.daytona-slide-enter-from, .daytona-slide-leave-to {
  transform: translateX(100%);
}

.daytona-panel-header {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  flex-wrap: wrap;
}
.daytona-panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 13px;
}
.daytona-panel-icon {
  font-size: 14px;
}
.daytona-status-pill {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 10px;
  background: var(--vp-c-default-soft);
  color: var(--vp-c-text-2);
}
.daytona-status-launching, .daytona-status-running, .daytona-status-checking {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}
.daytona-status-ready {
  background: var(--vp-c-success-soft);
  color: var(--vp-c-success-1);
}
.daytona-status-error, .daytona-status-unavailable {
  background: var(--vp-c-danger-soft);
  color: var(--vp-c-danger-1);
}

.daytona-panel-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.daytona-panel-actions .daytona-ui-button {
  border-radius: 6px;
  padding: 5px 12px;
  font-size: 12px;
}
.daytona-btn {
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-1);
  padding: 5px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  transition: background 120ms ease, border-color 120ms ease;
}
.daytona-btn:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.daytona-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.daytona-btn-primary {
  background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%);
  border-color: transparent;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.22);
}
.daytona-btn-primary:hover:not(:disabled) {
  filter: brightness(1.08);
  border-color: transparent;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(219, 39, 119, 0.32);
}
.daytona-btn-primary:disabled {
  filter: saturate(0.5);
}
.daytona-btn-ghost {
  background: transparent;
}
.daytona-btn-icon {
  background: transparent;
  border: none;
  color: var(--vp-c-text-2);
  font-size: 18px;
  line-height: 1;
  padding: 4px 10px;
  border-radius: 6px;
}
.daytona-btn-icon:hover:not(:disabled) {
  background: var(--vp-c-default-soft);
  color: var(--vp-c-text-1);
}

.daytona-banner {
  flex: 0 0 auto;
  padding: 12px 16px;
  font-size: 12px;
  background: var(--vp-c-warning-soft);
  color: var(--vp-c-text-1);
  border-bottom: 1px solid var(--vp-c-divider);
}
.daytona-banner code {
  font-family: var(--vp-font-family-mono);
  font-size: 11px;
  background: var(--vp-c-bg);
  padding: 1px 4px;
  border-radius: 3px;
}

.daytona-language-bar {
  flex: 0 0 auto;
  display: flex;
  gap: 6px;
  padding: 8px 12px;
  border-bottom: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
}
.daytona-language-btn {
  background: transparent;
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: background 120ms ease, border-color 120ms ease, color 120ms ease;
}
.daytona-language-btn:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.daytona-language-btn.active {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.daytona-language-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.daytona-tabs {
  flex: 0 0 auto;
  display: flex;
  flex-wrap: wrap;
  background: var(--vp-c-bg-soft);
  border-bottom: 1px solid var(--vp-c-divider);
}
.daytona-tab {
  background: transparent;
  border: none;
  border-right: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  padding: 8px 14px;
  font-size: 12px;
  font-family: var(--vp-font-family-mono);
  cursor: pointer;
  border-bottom: 2px solid transparent;
}
.daytona-tab:hover {
  color: var(--vp-c-text-1);
}
.daytona-tab.active {
  color: var(--vp-c-text-1);
  background: var(--vp-c-bg);
  border-bottom-color: var(--vp-c-brand-1);
}
.daytona-tab.dirty::after {
  content: " ●";
  color: var(--vp-c-warning-1);
}

.daytona-editor {
  flex: 1 1 auto;
  min-height: 200px;
  background: var(--vp-c-bg);
  overflow: hidden;
}
.daytona-editor .cm-editor {
  height: 100%;
  outline: none;
}
.daytona-editor .cm-editor.cm-focused {
  outline: none;
}

.daytona-panel-tabs {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 8px;
  border-top: 1px solid var(--vp-c-divider);
  border-bottom: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
}
.daytona-panel-tab {
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--vp-c-text-2);
  padding: 8px 12px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
}
.daytona-panel-tab:hover { color: var(--vp-c-text-1); }
.daytona-panel-tab.active {
  color: var(--vp-c-text-1);
  border-bottom-color: var(--vp-c-brand-1);
}
.daytona-sandbox-id {
  margin-left: auto;
  font-family: var(--vp-font-family-mono);
  font-size: 11px;
  color: var(--vp-c-text-3);
  padding-right: 6px;
}

.daytona-pane {
  flex: 0 0 auto;
  margin: 0;
  padding: 12px 14px;
  font-family: var(--vp-font-family-mono);
  font-size: 11.5px;
  line-height: 1.55;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  white-space: pre-wrap;
  word-break: break-word;
  height: 200px;
  overflow-y: auto;
}
.daytona-spinner-line {
  color: var(--vp-c-brand-1);
}
</style>
