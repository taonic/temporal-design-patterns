import { ApplicationFailure, activityInfo, heartbeat, log } from "@temporalio/activity";
import type { Duration } from "@temporalio/common";

import { ErrorState, FallbackConfig, GenerateResult, TIMEOUT } from "./shared";

// Error from the provider's HTTP client, carrying the status and message a real
// SDK (openai, anthropic, fetch) would surface.
class ProviderError extends Error {
  constructor(
    readonly status: number,
    message: string,
  ) {
    super(message);
  }
}

// LLMRegistry is worker-local state injected into the activities: it records the
// provider `generate` settled on per Workflow so runTool can read it without
// threading it through Workflow arguments. Keyed by Workflow ID so concurrent
// executions do not collide, and safe only because every Activity of one execution
// runs on the same worker (use a worker-specific Task Queue to guarantee that). It
// is process-local and NOT durable — which is why the retry BUDGET travels through
// heartbeat details instead; this registry only shares a convenience hint.
export class LLMRegistry {
  private readonly byWorkflow = new Map<string, string>();

  set(workflowId: string, provider: string): void {
    this.byWorkflow.set(workflowId, provider);
  }

  get(workflowId: string): string | undefined {
    return this.byWorkflow.get(workflowId);
  }

  // Production code should evict an entry when the Workflow completes so the map
  // does not grow without bound. The demo runs one short Workflow, so it does not.
  clear(workflowId: string): void {
    this.byWorkflow.delete(workflowId);
  }
}

// Scripted per-provider outcomes, indexed by how many times the provider has been
// called this run. 0 = success; an HTTP status throws; TIMEOUT hangs past the
// start-to-close timeout. Run with an empty prompt to see the 400 abort path.
// The script drives a three-turn loop:
//   turn 1: anthropic rate-limits (429) until its budget is spent → openai answers.
//   turn 2: openai 500s, spending its budget at once → gemini answers.
//   turn 3: gemini hangs; two timeouts spend its budget → anthropic (recovered) answers.
const MOCK_STATUSES: Record<string, number[]> = {
  anthropic: [429, 429, 429], // three rate-limit responses in turn 1, then recovers
  openai: [0, 500], // succeeds in turn 1, then a server error in turn 2
  gemini: [0, TIMEOUT, TIMEOUT], // answers in turn 2, then two hangs in turn 3
};

// Per-status backoff before Temporal retries the Activity (applied via nextRetryDelay).
const BACKOFF: Record<number, Duration> = {
  429: "2s",
  500: "1s",
  408: "1s",
  503: "2s",
};

// Simulated per-call latency (ms), kept well under the start-to-close timeout.
const SIMULATED_LATENCY_MS = 2500;

// A hung call sleeps this long — past generate's start-to-close timeout — so
// Temporal kills the attempt with a timeout instead of it ever returning.
const HUNG_CALL_MS = 20000;

const sleep = (ms: number): Promise<void> => new Promise((resolve) => setTimeout(resolve, ms));

// Per-provider call counter in worker memory, so callProvider walks each provider's
// MOCK_STATUSES itself. Process-local demo state, unsafe across restarts/executions.
const providerCallCount: Record<string, number> = {};

// Simulates the model's reasoning: inspect the prompt and either ask for a tool or
// return a final answer. This is what makes the Workflow loop.
function respond(prompt: string): { text: string; toolCall?: string } {
  if (prompt.includes("[calculator output]")) {
    return { text: "Durable execution keeps workflow state safe across failures — the answer is 42." };
  }
  if (prompt.includes("[search output]")) {
    return { text: "Got the figures; running the numbers.", toolCall: "calculator" };
  }
  return { text: "I need to look that up first.", toolCall: "search" };
}

// Stands in for the provider SDK: waits for the round-trip, then returns the
// response or throws a ProviderError. Walks the provider's scripted MOCK_STATUSES.
async function callProvider(provider: string, prompt: string): Promise<{ text: string; toolCall?: string }> {
  const index = providerCallCount[provider] ?? 0;
  providerCallCount[provider] = index + 1;
  const status = MOCK_STATUSES[provider]?.[index] ?? 0;

  // A scripted TIMEOUT hangs past the start-to-close timeout so Temporal kills the
  // attempt — it never returns, so the retry must infer the timeout (see generate).
  if (status === TIMEOUT) {
    await sleep(HUNG_CALL_MS);
  }

  await sleep(SIMULATED_LATENCY_MS);
  if (status !== 0) {
    throw new ProviderError(status, `${provider} responded HTTP ${status}`);
  }
  return respond(prompt);
}

// Prefer the caller's default, then sweep the rest in preference order (wrapping),
// skipping any that have spent their budget.
function pickProvider(spent: Record<string, number>, defaultProvider: string, config: FallbackConfig): string {
  const start = Math.max(0, config.providers.indexOf(defaultProvider));
  const order = config.providers.map(
    (_, i) => config.providers[(start + i) % config.providers.length],
  );
  for (const provider of order) {
    if ((spent[provider] ?? 0) < config.budget) {
      return provider;
    }
  }
  // Every provider is exhausted; stay on the last one and let Temporal's
  // maximumAttempts stop the retries.
  return order[order.length - 1];
}

// Replay `count` timeouts onto the budget. A timeout persists no outcome, so each
// attempt re-derives them from the attempt gap and charges the TIMEOUT cost against
// the provider pickProvider would pick — failing over once a provider is exhausted.
function chargeTimeouts(
  spent: Record<string, number>,
  count: number,
  defaultProvider: string,
  config: FallbackConfig,
): Record<string, number> {
  const cost = config.errorCost[TIMEOUT] ?? config.defaultErrorCost;
  for (let i = 0; i < count; i++) {
    const provider = pickProvider(spent, defaultProvider, config);
    spent[provider] = (spent[provider] ?? 0) + cost;
  }
  return spent;
}

// Dependency-injection factory: closes over the injected LLMRegistry and returns the
// activity implementations, so they use `registry` directly. The Workflow infers
// signatures from `Activities = ReturnType<typeof createActivities>`.
export const createActivities = (registry: LLMRegistry) => ({
  // Calls one provider per invocation: 400 aborts; other errors are retryable so
  // Temporal retries and may switch providers; a hung call breaches start-to-close
  // and retries too. Returns the provider that answered.
  async generate(prompt: string, defaultProvider: string, config: FallbackConfig): Promise<GenerateResult> {
    // A malformed request is an HTTP 400 that no provider will accept — abort.
    if (prompt.trim() === "") {
      throw ApplicationFailure.nonRetryable("empty prompt (HTTP 400)", "400");
    }

    // attempt is Temporal's 1-based retry counter; heartbeatDetails carries the
    // spent budget and last resolved attempt across retries.
    const { attempt, heartbeatDetails, workflowExecution } = activityInfo();

    const errorState: ErrorState = (heartbeatDetails as ErrorState | undefined) ?? { spent: {}, lastResolvedAttempt: 0 };
    errorState.spent ??= {};
    errorState.lastResolvedAttempt ??= 0;

    // Attempts since the last recorded HTTP outcome were timeouts (hung calls
    // Temporal killed before they could heartbeat). Infer them from the gap and
    // replay onto a working copy of the budget before picking.
    const timeouts = Math.max(0, attempt - 1 - errorState.lastResolvedAttempt);
    const spent = chargeTimeouts({ ...errorState.spent }, timeouts, defaultProvider, config);

    // Pick the provider: default until its budget is spent, then the next in order.
    const provider = pickProvider(spent, defaultProvider, config);

    // Publish the current provider so runTool (same worker) can read it — a
    // convenience hint; the durable budget lives in heartbeat details.
    registry.set(workflowExecution.workflowId, provider);

    log.info(
      `[${provider}] attempt ${attempt}, ${timeouts} timeout(s) since last HTTP outcome, budget spent ${JSON.stringify(spent)}`,
    );

    try {
      const response = await callProvider(provider, prompt);
      return { provider, ...response };
    } catch (err) {
      if (!(err instanceof ProviderError)) throw err;
      const { status, message } = err;

      // 400 Bad Request is permanent — no provider will accept the request.
      if (status === 400) {
        throw ApplicationFailure.nonRetryable(message, "400");
      }

      // Transient (429/500/503): spend this provider's budget and mark this the
      // last resolved attempt, so later retries only count the timeouts after it.
      const cost = config.errorCost[status] ?? config.defaultErrorCost;
      spent[provider] = (spent[provider] ?? 0) + cost;

      // Persist the running tally so the retried attempt resumes here.
      heartbeat({ spent, lastResolvedAttempt: attempt });

      // Retryable: Temporal retries the Activity after the per-status backoff.
      throw ApplicationFailure.create({
        message: `${message}; failing over`,
        type: String(status),
        nextRetryDelay: BACKOFF[status] ?? "1s",
      });
    }
  },

  // Runs a tool the model asked for between turns (simulated here). Reads the current
  // provider from the injected registry — state generate wrote on this same worker.
  async runTool(tool: string, question: string): Promise<string> {
    const { workflowExecution } = activityInfo();
    const provider = registry.get(workflowExecution.workflowId) ?? "unknown";
    log.info(`running tool '${tool}' (generate is currently on provider '${provider}')`);
    await sleep(500);
    switch (tool) {
      case "search":
        return `top hit for "${question}"`;
      case "calculator":
        return "42";
      default:
        return "";
    }
  },
});

// Activity interface the Workflow proxies against.
export type Activities = ReturnType<typeof createActivities>;
