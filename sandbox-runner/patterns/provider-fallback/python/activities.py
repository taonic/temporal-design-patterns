import asyncio
from datetime import timedelta
from typing import Optional

from temporalio import activity
from temporalio.exceptions import ApplicationError

from shared import ErrorState, FallbackConfig, GenerateResult, TIMEOUT


# An error raised by the provider's HTTP client, carrying the status and
# message the library would surface. A real SDK (openai, anthropic, httpx)
# raises something equivalent; the Activity reads `status` and `message` off it
# rather than reconstructing them.
class ProviderError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


# LLMRegistry is worker-local state injected into the activities: it records the
# provider `generate` settled on per Workflow so run_tool can read it without
# threading it through Workflow arguments. Keyed by Workflow ID so concurrent
# executions do not collide, and safe only because every Activity of one execution
# runs on the same worker (use a worker-specific Task Queue to guarantee that). It
# is process-local and NOT durable — which is why the retry BUDGET travels through
# heartbeat details instead; this registry only shares a convenience hint.
class LLMRegistry:
    def __init__(self) -> None:
        self._by_workflow: dict[str, str] = {}

    def set(self, workflow_id: str, provider: str) -> None:
        self._by_workflow[workflow_id] = provider

    def get(self, workflow_id: str) -> Optional[str]:
        return self._by_workflow.get(workflow_id)

    # Production code should evict an entry when the Workflow completes so the map
    # does not grow without bound. The demo runs one short Workflow, so it does not.
    def clear(self, workflow_id: str) -> None:
        self._by_workflow.pop(workflow_id, None)


# Each provider returns a scripted sequence of outcomes, indexed by how many
# times that provider has been called across the whole run. 0 = success; an HTTP
# status (429, 500, …) raises that error; TIMEOUT makes the call hang past the
# Activity's start-to-close timeout so Temporal times the attempt out. Run with
# an empty prompt to see the 400 (invalid request) abort path. The scripted
# outcomes drive a three-turn agent loop:
#   turn 1: anthropic is rate limited (429) until its budget is spent, then fails
#           over to openai, which answers for the first time.
#   turn 2: openai returns a server error (500) that spends its budget in one
#           shot, then fails over to gemini, which answers.
#   turn 3: gemini's calls hang and time out; after two timeouts spend its
#           budget it fails over to anthropic, which has recovered and answers.
MOCK_STATUSES: dict[str, list[int]] = {
    "anthropic": [429, 429, 429],  # three rate-limit responses in turn 1, then recovers
    "openai": [0, 500],  # succeeds in turn 1, then a server error in turn 2
    "gemini": [0, TIMEOUT, TIMEOUT],  # answers in turn 2, then two hangs in turn 3
}

# Per-status backoff before Temporal retries the Activity (applied via next_retry_delay).
BACKOFF: dict[int, timedelta] = {
    429: timedelta(seconds=2),
    500: timedelta(seconds=1),
    408: timedelta(seconds=1),
    503: timedelta(seconds=2),
}

# Simulated per-call latency (ms) so each provider round-trip takes time, the
# way a real model call would. Keep it well under the start-to-close timeout.
SIMULATED_LATENCY_MS = 2500

# A hung call sleeps this long — past the generate Activity's start-to-close
# timeout — so Temporal kills the attempt with a timeout instead of ever
# returning. Real model calls stall the same way when a provider is degraded.
HUNG_CALL_MS = 20000

# Per-provider call counter kept in worker-process memory (like the heartbeat
# sample's static call index), so call_provider walks down each provider's
# scripted MOCK_STATUSES by itself. NOTE: process-local demo state — it does not
# survive a worker restart and is not safe across concurrent Workflow executions.
provider_call_count: dict[str, int] = {}


# respond simulates the model's reasoning: it inspects the prompt and either
# asks to run a tool or returns a final answer. This is what makes the Workflow
# loop — the model drives an agentic tool-calling cycle.
def respond(prompt: str) -> tuple[str, Optional[str]]:
    if "[calculator output]" in prompt:
        return (
            "Durable execution keeps workflow state safe across failures — the answer is 42.",
            None,
        )
    if "[search output]" in prompt:
        return ("Got the figures; running the numbers.", "calculator")
    return ("I need to look that up first.", "search")


# call_provider stands in for the provider SDK: given the prompt, it waits for
# the simulated round-trip, then returns the model's response on success or
# raises a ProviderError carrying the HTTP status and message. It walks down the
# provider's scripted MOCK_STATUSES, counting calls itself.
async def call_provider(provider: str, prompt: str) -> tuple[str, Optional[str]]:
    index = provider_call_count.get(provider, 0)
    provider_call_count[provider] = index + 1
    statuses = MOCK_STATUSES.get(provider, [])
    status = statuses[index] if index < len(statuses) else 0

    # A scripted TIMEOUT is a latency failure: the call hangs so long that the
    # Activity's start-to-close timeout fires and Temporal kills the attempt. The
    # Activity never returns from here — there is no error to catch, which is why
    # the retry has to detect the timeout from its own context (see generate).
    if status == TIMEOUT:
        await asyncio.sleep(HUNG_CALL_MS / 1000)

    await asyncio.sleep(SIMULATED_LATENCY_MS / 1000)
    if status != 0:
        raise ProviderError(status, f"{provider} responded HTTP {status}")
    return respond(prompt)


# pick_provider prefers the caller's default, then sweeps the remaining providers
# in preference order — starting from the default's position and wrapping around
# the list — skipping any that have spent their budget. This can be extended with
# more sophisticated rules.
def pick_provider(
    spent: dict[str, int], default_provider: str, config: FallbackConfig
) -> str:
    providers = config.providers
    start = providers.index(default_provider) if default_provider in providers else 0
    order = [providers[(start + i) % len(providers)] for i in range(len(providers))]
    for provider in order:
        if spent.get(provider, 0) < config.budget:
            return provider
    # Every provider is exhausted; stay on the last one and let Temporal's
    # maximum_attempts stop the retries.
    return order[-1]


# charge_timeouts rebuilds the spent budget after `count` start-to-close timeouts.
# A timeout leaves no outcome to persist (the attempt was killed mid-call), so
# instead of storing a running count each attempt replays the timeouts the gap
# implies. Each one charges the TIMEOUT cost against the provider pick_provider
# would have chosen; once a provider's spend reaches the budget the sweep fails
# over to the next one — even though no HTTP error was ever seen.
def charge_timeouts(
    spent: dict[str, int], count: int, default_provider: str, config: FallbackConfig
) -> dict[str, int]:
    cost = config.error_cost.get(str(TIMEOUT), config.default_error_cost)
    for _ in range(count):
        provider = pick_provider(spent, default_provider, config)
        spent[provider] = spent.get(provider, 0) + cost
    return spent


# CompletionActivities binds the activity implementations to an injected LLMRegistry
# (dependency injection): worker.py constructs one registry and passes it in, so
# generate and run_tool share it through self instead of module-global state.
class CompletionActivities:
    def __init__(self, registry: LLMRegistry) -> None:
        self.registry = registry

    # generate calls one provider per invocation: 400 aborts, other errors are
    # retryable so Temporal retries and the next attempt may switch providers. A
    # hung call is left to breach the start-to-close timeout, which Temporal turns
    # into a retry too. Returns the provider that answered so the caller can reuse it.
    @activity.defn
    async def generate(
        self, prompt: str, default_provider: str, config: FallbackConfig
    ) -> GenerateResult:
        # A malformed request is an HTTP 400 that no provider will accept — abort.
        if prompt.strip() == "":
            raise ApplicationError("empty prompt (HTTP 400)", type="400", non_retryable=True)

        # attempt is Temporal's built-in retry counter (1-based); heartbeat details
        # carry the spent budget and the last resolved attempt across retries.
        info = activity.info()
        attempt = info.attempt

        # Error state maintained across retries via heartbeat details. Heartbeat
        # details deserialize to a plain dict (no type hint), so rebuild the
        # dataclass from it.
        if info.heartbeat_details:
            error_state = ErrorState(**info.heartbeat_details[0])
        else:
            error_state = ErrorState()

        # Any attempt since the last one that recorded an HTTP outcome was a timeout —
        # a hung call Temporal killed before it could heartbeat or return a result. The
        # activity context carries no "last failure", so infer those timeouts from the
        # attempt gap and replay them onto a working copy of the budget before picking.
        timeouts = max(0, attempt - 1 - error_state.last_resolved_attempt)
        spent = charge_timeouts(dict(error_state.spent), timeouts, default_provider, config)

        # Decide which provider to call: the default until it has spent its budget
        # (to HTTP errors or timeouts), then the next provider in preference order.
        provider = pick_provider(spent, default_provider, config)

        # Publish the current provider so run_tool (same worker) can read it — a
        # convenience hint; the durable budget lives in heartbeat details.
        self.registry.set(info.workflow_id, provider)

        activity.logger.info(
            f"[{provider}] attempt {attempt}, {timeouts} timeout(s) since last HTTP outcome, budget spent {spent}"
        )

        try:
            text, tool_call = await call_provider(provider, prompt)
            return GenerateResult(provider=provider, text=text, tool_call=tool_call)
        except ProviderError as err:
            status = err.status
            message = err.message

            # 400 Bad Request is permanent — no provider will accept the request.
            if status == 400:
                raise ApplicationError(message, type="400", non_retryable=True)

            # Transient (429 / 500 / 503): spend this provider's budget by the error's
            # cost and record this as the last resolved attempt, so later retries count
            # only the timeouts that follow it. pick_provider keeps this provider until
            # its budget runs out, then switches.
            cost = config.error_cost.get(str(status), config.default_error_cost)
            spent[provider] = spent.get(provider, 0) + cost

            # Persist the running tally (including any replayed timeout failovers) so
            # the retried attempt resumes from here.
            activity.heartbeat(ErrorState(spent=spent, last_resolved_attempt=attempt))

            # Retryable (non_retryable defaults to False): Temporal retries the
            # Activity after the per-status backoff.
            raise ApplicationError(
                f"{message}; failing over",
                type=str(status),
                next_retry_delay=BACKOFF.get(status, timedelta(seconds=1)),
            )

    # run_tool executes a tool the model asked for between turns (simulated here). It
    # reads the current provider from the injected registry — state generate wrote on
    # this same worker.
    @activity.defn
    async def run_tool(self, tool: str, question: str) -> str:
        provider = self.registry.get(activity.info().workflow_id) or "unknown"
        activity.logger.info(f"running tool '{tool}' (generate is currently on provider '{provider}')")
        await asyncio.sleep(0.5)
        if tool == "search":
            return f'top hit for "{question}"'
        if tool == "calculator":
            return "42"
        return ""
