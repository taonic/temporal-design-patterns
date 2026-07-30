import * as wf from "@temporalio/workflow";

import type { Activities } from "./activities";
import { FallbackConfig, MAX_SWEEPS, MAX_TURNS, TIMEOUT } from "./shared";

// runTool is a plain Activity for the tools the agent invokes between model calls.
const { runTool } = wf.proxyActivities<Activities>({
  startToCloseTimeout: "10 seconds",
});

// Default fallback policy: sweep the providers in preference order, giving each a
// retry budget of 3 before failover. Each outcome spends against that budget — a
// 429 (rate limited) is cheap to retry in place; a 500 (server error) burns the
// whole budget at once; a TIMEOUT costs 2, so a provider fails over on its second
// timed-out call. Callers can override this per Activity call.
const DEFAULT_CONFIG: FallbackConfig = {
  providers: ["anthropic", "openai", "gemini"],
  budget: 3,
  errorCost: { 429: 1, 500: 3, [TIMEOUT]: 2 },
  defaultErrorCost: 2,
};

// providerFallbackWorkflow runs an agentic tool-calling loop. Each turn calls the
// model (generate); if the model asks for a tool, the Workflow runs it and feeds
// the output into the next turn, until the model returns a final answer. The
// provider that answered is reused as the preferred provider for the next turn,
// so a healthy provider is not re-swept from the top of the preference list every
// time — only a fresh failure triggers another fallback sweep.
export async function providerFallbackWorkflow(
  question: string,
  config: FallbackConfig = DEFAULT_CONFIG,
): Promise<string> {
  let preferredProvider = config.providers[0];
  let prompt = question;

  for (let turn = 1; turn <= MAX_TURNS; turn++) {
    // Create the model-call stub per turn so its Activity summary (shown in the
    // Temporal UI/CLI) names the provider this turn starts with. generate sweeps
    // providers internally; maximumAttempts caps the sweep at MAX_SWEEPS passes.
    const { generate } = wf.proxyActivities<Activities>({
      // A healthy call returns in a couple of seconds; a hung provider call
      // breaches this deadline and Temporal retries the Activity with a timeout,
      // which drives the timeout failover. heartbeatTimeout sits above it so the
      // start-to-close timeout — not a missed heartbeat — is what trips a hang.
      startToCloseTimeout: "6 seconds",
      heartbeatTimeout: "20 seconds",
      retry: { maximumAttempts: MAX_SWEEPS * config.providers.length },
      summary: `generate (${preferredProvider})`,
    });

    const result = await generate(prompt, preferredProvider, config);
    preferredProvider = result.provider; // stick with the provider that just worked
    wf.log.info(`turn ${turn}: answered by ${result.provider}`);

    if (!result.toolCall) {
      return result.text; // final answer — the agent is done
    }

    // The model requested a tool. Run it, then feed the output into the next turn.
    const output = await runTool(result.toolCall, question);
    prompt = `[${result.toolCall} output] ${output}`;
  }

  throw wf.ApplicationFailure.nonRetryable(
    `agent did not finish within ${MAX_TURNS} turns`,
    "AgentLoopExhausted",
  );
}
