// The Workflow and the sweeping Activity both run on this Task Queue.
export const TASK_QUEUE = "provider-fallback-task-queue";
export const WORKFLOW_ID_PREFIX = "completion";

// Maximum number of full passes over the provider list before giving up.
export const MAX_SWEEPS = 3;

// Maximum agent turns (model calls) before giving up on the tool-calling loop.
export const MAX_TURNS = 6;

// Sentinel used both as a scripted provider outcome (a hung call) and as the
// errorCost key for a start-to-close timeout, so a timeout spends the budget the
// same way an HTTP error does. Not a real HTTP status, hence the negative value.
export const TIMEOUT = -1;

// Fallback policy passed into the generate Activity: which providers to sweep in
// preference order, how much retry budget each one gets before failover, and what
// each outcome costs against that budget — the errorCost map is keyed by HTTP
// status and by TIMEOUT, so a timed-out call spends budget like any other error.
export interface FallbackConfig {
  providers: string[];
  budget: number;
  errorCost: Record<number, number>;
  defaultErrorCost: number;
}

// Error state maintained ACROSS Activity retries via heartbeat details, so a
// retried attempt resumes the sweep where the previous one left off instead of
// restarting from the first provider.
export interface ErrorState {
  // retry budget already spent per provider, accumulated across retries
  spent: Record<string, number>;
  // the attempt number that last recorded an HTTP outcome (success or a spent
  // budget). Any retry beyond this without advancing it was a start-to-close
  // timeout — a hung provider call Temporal killed before it could record a
  // result — so the gap between it and the current attempt counts the timeouts.
  lastResolvedAttempt: number;
}

// What one model call returns: the provider that produced the response, the
// message text, and an optional tool the model wants to run next. No toolCall
// means the model returned a final answer.
export interface GenerateResult {
  provider: string;
  text: string;
  toolCall?: string;
}
