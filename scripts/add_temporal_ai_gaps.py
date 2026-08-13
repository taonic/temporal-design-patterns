#!/usr/bin/env python3
"""Add catalog pages for gaps vs Temporal AI/agentic pattern guidance."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

import importlib.util

spec = importlib.util.spec_from_file_location(
    "expand_stub_docs", ROOT / "scripts" / "expand_stub_docs.py"
)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)

NEW = {
    "agent-tool-loop": {
        "title": "Agent Tool Loop",
        "icon": "polling-icon.svg",
        "overview": (
            "The Agent Tool Loop pattern runs a Turn as a durable loop: call the model, "
            "execute selected tools, feed results back, and repeat until the model returns a final reply.\n"
            "Each model call and tool call is its own Activity Step so retries and history stay clear.\n"
            "Primitives used: Turn, Durable Model Call, Activity Tool, Step events."
        ),
        "problem": (
            "A single model call rarely finishes real work.\n"
            "If the whole loop lives outside Temporal, a crash mid-tool loses progress and may double-run side effects."
        ),
        "solution": (
            "Inside the Turn (Session sub-state or Child Workflow), loop:\n"
            "1) Durable Model Call with tool schemas,\n"
            "2) for each tool call, Activity Tool or Workflow Tool,\n"
            "3) append tool results to the message list,\n"
            "4) exit when there are no tool calls or a cap is hit."
        ),
        "mermaid": """flowchart TD
    Start[Turn start] --> Model[Durable Model Call]
    Model -->|tool_calls| Tools[Activity tools]
    Tools --> Model
    Model -->|final text| End[Turn end]""",
        "walk": [
            "The Turn starts with the user input and session memory.",
            "A model Activity returns content and optional tool_calls.",
            "Each tool runs as its own Step with the tool's retry and approval profile.",
            "Results return to the next model call until a final reply or a loop limit.",
        ],
        "code": '''while True:
    response = await workflow.execute_activity(
        call_llm, request, start_to_close_timeout=timedelta(seconds=30)
    )
    if not response.tool_calls:
        return response.content
    for call in response.tool_calls:
        result = await workflow.execute_activity(
            execute_tool, call, start_to_close_timeout=timedelta(seconds=60)
        )
        request = request.with_tool_result(call.id, result)''',
        "impl": (
            "### Loop limits\n\n"
            "Cap iterations and total tokens so a runaway model cannot loop forever.\n\n"
            "### Deterministic tools\n\n"
            "State-only tools (for example updating a TODO list in Session state) belong in "
            "Workflow code; IO tools stay Activities."
        ),
        "when": (
            "Use for tool-using chat and job agents.\n"
            "Prefer Code Mode when one script should orchestrate many tools without round trips."
        ),
        "benefits": (
            "You get a clear audit trail of every model and tool Step.\n"
            "Long loops grow history—combine with Continue-As-New Session on long jobs."
        ),
        "table": (
            "| Approach | Durability | Round trips |\n"
            "| :--- | :--- | :--- |\n"
            "| Agent Tool Loop | Per Step | Many |\n"
            "| Code Mode Orchestrator | Per host call | Fewer |\n"
            "| Single-shot model call | One Step | One |"
        ),
        "practices": [
            "**Separate model and tool Activities.** Do not hide tool IO inside the model Activity.",
            "**Apply per-tool profiles** inside the loop.",
            "**Emit turn and step events** for each iteration.",
        ],
        "pitfalls": [
            "**Unbounded while True without a max_steps guard.**",
            "**Putting the provider SDK in the Workflow.**",
            "**Re-running the whole loop after Continue-As-New without snapshotting messages.**",
        ],
        "related": [
            "[Durable Model Call](/durable-model-call)",
            "[Activity Tool](/activity-tool)",
            "[Workflow Tool](/workflow-tool)",
            "[Code Mode Orchestrator](/code-mode-orchestrator)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
            "[Temporal Docs: Workflows](https://docs.temporal.io/workflows)",
        ],
    },
    "structured-model-output": {
        "title": "Structured Model Output",
        "icon": "request-response-icon.svg",
        "overview": (
            "The Structured Model Output pattern asks the model for schema-validated responses "
            "(for example Pydantic models) inside a Durable Model Call Activity.\n"
            "The Turn receives typed data instead of free text that later steps must re-parse.\n"
            "Primitives used: Durable Model Call, Tool/Operation schemas, typed Activity results."
        ),
        "problem": (
            "Free-text model replies force brittle parsing in the Workflow.\n"
            "Invalid shapes cause confusing failures deep in the tool loop."
        ),
        "solution": (
            "Declare a response schema and have the model Activity return a validated object.\n"
            "On validation failure, classify the error (often non-retryable or a model retry with repair instructions)."
        ),
        "mermaid": """flowchart LR
    Turn --> Act[Model Activity]
    Act --> Parse[Schema validate]
    Parse -->|ok| Typed[Typed result]
    Parse -->|fail| Err[Classified error]""",
        "walk": [
            "The Turn requests a structured response format.",
            "The model Activity calls the provider with that schema.",
            "Validation runs before the Activity completes successfully.",
            "The Workflow consumes a typed object without regex parsing.",
        ],
        "code": '''class AnalysisResult(BaseModel):
    sentiment: str
    confidence: float
    summary: str

@activity.defn
async def analyze_text(text: str) -> AnalysisResult:
    # Provider structured-output / parse API runs in the Activity.
    return await provider.parse(text, schema=AnalysisResult)''',
        "impl": (
            "### Data converter\n\n"
            "Use a Pydantic-friendly data converter on the Temporal Client and Worker so complex "
            "models serialize cleanly.\n\n"
            "### Repair loops\n\n"
            "Optionally retry once with the validation errors appended; cap repairs."
        ),
        "when": (
            "Use when later Steps need fields, not prose.\n"
            "Keep free text for user-facing chat replies."
        ),
        "benefits": (
            "You fail fast on bad shapes and keep Workflows simple.\n"
            "Schemas must evolve carefully alongside prompts."
        ),
        "table": (
            "| Output style | Workflow safety |\n"
            "| :--- | :--- |\n"
            "| Structured schema | High |\n"
            "| JSON in prose | Medium |\n"
            "| Free text only | Low for automation |"
        ),
        "practices": [
            "**Validate in the Activity** before completion.",
            "**Version schemas** when fields change.",
            "**Keep schemas small** for reliability.",
        ],
        "pitfalls": [
            "**Parsing JSON with ad-hoc string splits in the Workflow.**",
            "**Huge nested schemas that models rarely satisfy.**",
        ],
        "related": [
            "[Durable Model Call](/durable-model-call)",
            "[Agent Tool Loop](/agent-tool-loop)",
            "[Type-Checked Scripts](/type-checked-scripts)",
        ],
        "refs": [
            "[Temporal Docs: Data conversion](https://docs.temporal.io/dataconversion)",
        ],
    },
    "provider-retry-delegation": {
        "title": "Provider Retry Delegation",
        "icon": "fixed-count-retries-icon.svg",
        "overview": (
            "The Provider Retry Delegation pattern disables retries inside model/provider client "
            "libraries and lets Temporal Activity retries own backoff, visibility, and crash safety.\n"
            "Primitives used: Durable Model Call, Activity RetryPolicy, classified ApplicationError."
        ),
        "problem": (
            "Layered retries (SDK + HTTP + Temporal) multiply delays, hide attempt counts, and can "
            "stampede a rate-limited API after a worker restart."
        ),
        "solution": (
            "Configure the provider client with zero client-side retries.\n"
            "Raise retryable or non-retryable errors from the Activity and rely on the Activity RetryPolicy."
        ),
        "mermaid": """flowchart TD
    Act[Model Activity] -->|error| Class[Classify error]
    Class -->|retryable| Temp[Temporal retry]
    Class -->|non_retryable| Fail[Fail Step]
    Client[Provider SDK] -->|max_retries=0| Act""",
        "walk": [
            "The worker builds the provider client with retries disabled.",
            "Transient failures surface as retryable Activity errors.",
            "Temporal schedules the next attempt with durable backoff.",
            "Permanent failures fail the Step without spinning.",
        ],
        "code": '''# Worker process configuration (always outside Workflow code)
provider = ProviderClient(api_key=..., max_retries=0, timeout=30.0)

@activity.defn
async def call_llm(request: LLMRequest) -> LLMResponse:
    try:
        return await provider.complete(request)
    except RateLimitError as e:
        raise ApplicationError(str(e), type="RateLimitError")  # retryable
    except AuthenticationError as e:
        raise ApplicationError(str(e), type="AuthenticationError", non_retryable=True)''',
        "impl": (
            "### One control plane\n\n"
            "Document that Temporal is the only retry engine for model calls in this agent.\n\n"
            "### Interaction with rate limits\n\n"
            "Combine with Rate-Limit Aware Model Calls when the API returns Retry-After."
        ),
        "when": (
            "Use for every production Durable Model Call.\n"
            "Keep provider retries only if you are not using Temporal Activities for that call."
        ),
        "benefits": (
            "You get durable, visible retries that survive worker crashes.\n"
            "You must map provider errors carefully."
        ),
        "table": (
            "| Retry owner | Survives crash | Visible in history |\n"
            "| :--- | :--- | :--- |\n"
            "| Temporal Activity | Yes | Yes |\n"
            "| Provider SDK only | No | No |\n"
            "| Both stacked | Unpredictable | Confused |"
        ),
        "practices": [
            "**Set max_retries=0 (or equivalent) on every provider client.**",
            "**Prefer one generic call_llm Activity** with model_id routing.",
            "**Log attempt metadata** via Activity heartbeats or events.",
        ],
        "pitfalls": [
            "**Leaving default SDK retries on.**",
            "**Catching all exceptions and returning None.** Hides failures from Temporal.",
        ],
        "related": [
            "[Durable Model Call](/durable-model-call)",
            "[Model Error Classification](/model-error-classification)",
            "[Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls)",
        ],
        "refs": [
            "[Temporal Docs: Retry policies](https://docs.temporal.io/encyclopedia/retry-policies)",
            "[Temporal Docs: Application failure](https://docs.temporal.io/references/failures)",
        ],
    },
    "model-error-classification": {
        "title": "Model Error Classification",
        "icon": "non-retryable-errors-icon.svg",
        "overview": (
            "The Model Error Classification pattern maps provider failures to retryable versus "
            "non-retryable Temporal errors so Activities do not loop on permanent faults.\n"
            "Primitives used: Durable Model Call, ApplicationError non_retryable flag, Step failure events."
        ),
        "problem": (
            "Treating every model exception as retryable burns quota on bad API keys and invalid prompts.\n"
            "Treating every exception as fatal drops transient 503s."
        ),
        "solution": (
            "In the model Activity, classify errors:\n"
            "retryable — rate limits, timeouts, 5xx, network;\n"
            "non-retryable — 401, invalid request, content policy, model not found.\n"
            "Raise ApplicationError with non_retryable=True for the permanent class."
        ),
        "mermaid": """flowchart TD
    Err[Provider error] --> Q{Class}
    Q -->|429 / 5xx / timeout| R[Retryable]
    Q -->|401 / 400 / policy| NR[Non-retryable]
    R --> Temporal[Activity retry]
    NR --> Fail[Fail Step]""",
        "walk": [
            "The provider client raises an error.",
            "The Activity maps it to a Temporal failure type.",
            "Retryable errors follow the Activity RetryPolicy.",
            "Non-retryable errors fail the Step for the Turn to handle.",
        ],
        "code": '''except AuthenticationError as e:
    raise ApplicationError(str(e), type="AuthenticationError", non_retryable=True)
except APIStatusError as e:
    if e.status_code >= 500:
        raise ApplicationError(str(e), type="ServerError")
    raise ApplicationError(str(e), type="ClientError", non_retryable=True)''',
        "impl": (
            "### Turn-level handling\n\n"
            "Non-retryable model failures may trigger Resumable Correction, a user-visible error, "
            "or a fallback model—decide explicitly in the Turn.\n\n"
            "### Content policy\n\n"
            "Treat policy violations as non-retryable unless you have a safe rewrite path."
        ),
        "when": (
            "Use with every Durable Model Call.\n"
            "Skip only for stubbed demo Activities that never call a provider."
        ),
        "benefits": (
            "You save cost and time on permanent faults.\n"
            "You must maintain the mapping as providers evolve."
        ),
        "table": (
            "| Error | Retry |\n"
            "| :--- | :--- |\n"
            "| Rate limit 429 | Yes |\n"
            "| Timeout / 503 | Yes |\n"
            "| Invalid API key | No |\n"
            "| Invalid prompt / 400 | No |\n"
            "| Content policy | No (unless rewrite) |"
        ),
        "practices": [
            "**Put classification next to the provider client.**",
            "**Emit error class on step_failed events.**",
            "**Test both branches** with mocked exceptions.",
        ],
        "pitfalls": [
            "**Retrying 401 forever.**",
            "**Marking all APIStatusError as retryable.**",
        ],
        "related": [
            "[Provider Retry Delegation](/provider-retry-delegation)",
            "[Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls)",
            "[Resumable Correction](/resumable-correction)",
        ],
        "refs": [
            "[Temporal Docs: Failures](https://docs.temporal.io/references/failures)",
        ],
    },
    "rate-limit-aware-model-calls": {
        "title": "Rate-Limit Aware Model Calls",
        "icon": "downstream-rate-limiting-icon.svg",
        "overview": (
            "The Rate-Limit Aware Model Calls pattern turns provider 429 responses into Temporal "
            "retries that honor Retry-After / rate-limit headers via next_retry_delay.\n"
            "Primitives used: Durable Model Call, ApplicationError next_retry_delay, Activity retries."
        ),
        "problem": (
            "Fixed backoff ignores the provider's requested delay and can worsen throttling.\n"
            "Busy-looping in the Workflow is illegal and useless."
        ),
        "solution": (
            "On rate limit errors, parse Retry-After (or equivalent) and raise a retryable "
            "ApplicationError with next_retry_delay set so Temporal waits that long before the next attempt."
        ),
        "mermaid": """flowchart LR
    Call[Model Activity] -->|429| Parse[Parse Retry-After]
    Parse --> Raise[ApplicationError + delay]
    Raise --> Wait[Temporal backoff]
    Wait --> Call""",
        "walk": [
            "The provider returns 429 with rate-limit headers.",
            "The Activity parses the suggested delay.",
            "It raises a retryable error carrying next_retry_delay.",
            "Temporal schedules the retry after that delay without holding a worker thread.",
        ],
        "code": '''except RateLimitError as e:
    delay = parse_retry_after(e)  # timedelta
    raise ApplicationError(
        f"Rate limited: {e}",
        type="RateLimitError",
        next_retry_delay=delay,
    )''',
        "impl": (
            "### Timeouts\n\n"
            "Set schedule_to_close_timeout large enough to cover several delayed retries for "
            "search or bursty APIs.\n\n"
            "### Fairness across tenants\n\n"
            "For multi-tenant agents, consider Task Queue fairness so one hot tenant cannot starve others."
        ),
        "when": (
            "Use whenever the provider documents rate limits.\n"
            "Fixed exponential backoff alone is a weaker fallback when headers are absent."
        ),
        "benefits": (
            "You align retries with provider guidance and free workers during the wait.\n"
            "Header formats differ by vendor—keep parsers tested."
        ),
        "table": (
            "| Strategy | Uses provider hint | Durable wait |\n"
            "| :--- | :--- | :--- |\n"
            "| next_retry_delay | Yes | Yes |\n"
            "| Fixed exponential only | No | Yes |\n"
            "| Sleep in Activity thread | Maybe | Holds worker |"
        ),
        "practices": [
            "**Prefer header-driven delay when present.**",
            "**Fall back to RetryPolicy backoff** if headers are missing.",
            "**Metric rate-limit hits per model and tenant.**",
        ],
        "pitfalls": [
            "**time.sleep in the Activity for minutes** instead of next_retry_delay.",
            "**Parsing Retry-After in the Workflow.**",
        ],
        "related": [
            "[Provider Retry Delegation](/provider-retry-delegation)",
            "[Model Error Classification](/model-error-classification)",
            "[Model Timeout Profiles](/model-timeout-profiles)",
        ],
        "refs": [
            "[Temporal Docs: Retry policies](https://docs.temporal.io/encyclopedia/retry-policies)",
        ],
    },
    "model-timeout-profiles": {
        "title": "Model Timeout Profiles",
        "icon": "updatable-timer-icon.svg",
        "overview": (
            "The Model Timeout Profiles pattern assigns start_to_close (and related) timeouts by "
            "operation class—fast chat, reasoning models, web search, image generation—so Activities "
            "neither cut off expensive work nor hang forever.\n"
            "Primitives used: Durable Model Call / Activity Tool timeouts, StepPolicy."
        ),
        "problem": (
            "One 30s timeout kills reasoning models; one 15m timeout hides stuck calls and blocks Turns."
        ),
        "solution": (
            "Maintain a small timeout table keyed by operation type or model class and apply it when "
            "scheduling Activities."
        ),
        "mermaid": """flowchart TD
    Op[Operation type] --> Table[Timeout profile]
    Table --> Act[execute_activity timeouts]""",
        "walk": [
            "The Turn knows the operation class (chat, reasoning, search, image).",
            "It loads timeouts from a profile table.",
            "The Activity is scheduled with those timeouts.",
            "Stuck calls fail at the profile bound and surface as Step failures.",
        ],
        "code": '''TIMEOUTS = {
    "chat": timedelta(seconds=30),
    "reasoning": timedelta(minutes=5),
    "web_search": timedelta(minutes=5),
    "image": timedelta(minutes=2),
}

await workflow.execute_activity(
    call_llm,
    request,
    start_to_close_timeout=TIMEOUTS[request.op_class],
)''',
        "impl": (
            "### Recommended starting points\n\n"
            "| Class | start_to_close |\n"
            "| :--- | :--- |\n"
            "| Simple chat LLM | 30s |\n"
            "| Reasoning / extended thinking | 5m |\n"
            "| Web search tool | 5m |\n"
            "| Simple tool | 30–60s |\n"
            "| Image generation | 2m |\n"
            "| Document processing | 1–2m |\n\n"
            "Tune from production metrics."
        ),
        "when": (
            "Use whenever an agent mixes fast and slow model or tool operations.\n"
            "A single timeout is enough for uniform short chat demos."
        ),
        "benefits": (
            "You match timeouts to real latency distributions.\n"
            "Profiles need periodic review as models change."
        ),
        "table": (
            "| Timeout too short | Timeout too long |\n"
            "| :--- | :--- |\n"
            "| False failures | Stuck Turns |\n"
            "| Wasted retries | Poor UX |"
        ),
        "practices": [
            "**Pair with schedule_to_close** when many retries are expected.",
            "**Heartbeat long generations** when streaming inside an Activity.",
            "**Document profiles next to model routing.**",
        ],
        "pitfalls": [
            "**Copying chat timeouts onto reasoning models.**",
            "**No schedule_to_close on gather() fan-out searches.** One bad retry loop can stall the join.",
        ],
        "related": [
            "[Durable Model Call](/durable-model-call)",
            "[Best-Effort Parallel Tools](/best-effort-parallel-tools)",
            "[Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls)",
        ],
        "refs": [
            "[Temporal Docs: Activity timeouts](https://docs.temporal.io/encyclopedia/detecting-activity-failures)",
        ],
    },
    "best-effort-parallel-tools": {
        "title": "Best-Effort Parallel Tools",
        "icon": "parallel-execution-icon.svg",
        "overview": (
            "The Best-Effort Parallel Tools pattern runs many independent tool or search Activities "
            "concurrently and continues with successful results when some fail "
            "(`asyncio.gather(..., return_exceptions=True)`).\n"
            "Primitives used: parallel Activity Tools, partial failure handling, optional subagent fan-out."
        ),
        "problem": (
            "Fail-fast parallel joins drop an entire research Turn when one search times out.\n"
            "Sequential searches are correct but slow."
        ),
        "solution": (
            "Schedule independent Activities in parallel.\n"
            "Await with return_exceptions, filter successes, and pass partial results to the next "
            "model or synthesis Step.\n"
            "Set schedule_to_close_timeout so one poisoned retry loop cannot block the gather forever."
        ),
        "mermaid": """flowchart TB
    Turn --> A[Search A]
    Turn --> B[Search B]
    Turn --> C[Search C]
    A --> Join[Gather + filter]
    B --> Join
    C --> Join
    Join --> Synth[Synthesize]""",
        "walk": [
            "The Turn builds a list of independent tool Activities.",
            "It awaits them concurrently.",
            "Failures become exception values; successes remain payloads.",
            "Downstream synthesis uses whatever succeeded and records gaps in events.",
        ],
        "code": '''tasks = [
    workflow.execute_activity(
        search_web,
        q,
        start_to_close_timeout=timedelta(seconds=300),
        schedule_to_close_timeout=timedelta(seconds=900),
    )
    for q in queries
]
results = await asyncio.gather(*tasks, return_exceptions=True)
ok = [r for r in results if not isinstance(r, Exception)]''',
        "impl": (
            "### When to fail the Turn anyway\n\n"
            "If zero successes return, fail the Turn.\n"
            "If a minimum threshold is required, enforce it explicitly.\n\n"
            "### Versus subagent fan-out\n\n"
            "Use this pattern for parallel tools; use Fan-Out Subagents when each branch needs its "
            "own agent session."
        ),
        "when": (
            "Use for research, enrichment, and other independent IO.\n"
            "Avoid when all results are required for correctness (payments, ledger writes)."
        ),
        "benefits": (
            "You finish useful work despite partial outages.\n"
            "Callers must understand incomplete result sets."
        ),
        "table": (
            "| Join mode | Behavior |\n"
            "| :--- | :--- |\n"
            "| Best-effort | Continue with successes |\n"
            "| Fail-fast | Abort on first error |\n"
            "| All-required | Fail if any missing |"
        ),
        "practices": [
            "**Always set schedule_to_close_timeout on long parallel searches.**",
            "**Record per-branch failures as events.**",
            "**Cap concurrency** to protect downstream APIs.",
        ],
        "pitfalls": [
            "**Swallowing exceptions without logging which query failed.**",
            "**Using best-effort for non-idempotent writes.**",
        ],
        "related": [
            "[Fan-Out Subagents](/fanout-subagents)",
            "[Script Fan-Out](/script-fan-out)",
            "[Model Timeout Profiles](/model-timeout-profiles)",
        ],
        "refs": [
            "[Temporal Docs: Activities](https://docs.temporal.io/activities)",
        ],
    },
    "progress-streaming": {
        "title": "Progress Streaming",
        "icon": "event-accumulator-icon.svg",
        "overview": (
            "The Progress Streaming pattern lets a Session publish incremental agent events "
            "(tokens, tool starts, approvals) to UIs through a durable, offset-addressed stream "
            "built on Signals, Updates, and Queries—not ad-hoc websockets inside the worker.\n"
            "Primitives used: Standardized Event Stream, Session Workflow, client cursors."
        ),
        "problem": (
            "Polling Workflow queries for every token is inefficient.\n"
            "Pushing from Activities to a global socket bypasses durability and Continue-As-New."
        ),
        "solution": (
            "Host a durable stream on the Session Workflow.\n"
            "Publish events as the Turn progresses; clients subscribe with an offset/cursor and "
            "resume after disconnect.\n"
            "HTTP Channel Agent exposes the stream as SSE or NDJSON."
        ),
        "mermaid": """flowchart LR
    Turn --> Pub[Publish event]
    Pub --> Stream[Session stream]
    Stream --> Sub[UI subscriber]
    Sub -->|cursor| Stream""",
        "walk": [
            "The Session initializes a durable stream at Workflow init.",
            "Model/tool Steps publish progress events to topics.",
            "A UI subscribes with a cursor and receives batches.",
            "Reconnects resume from the last offset after Continue-As-New via carried state.",
        ],
        "code": '''# Conceptual shape — stream hosted on the Session Workflow
@workflow.init
def __init__(self) -> None:
    self.stream = DurableEventStream()  # Signals/Updates/Queries under the hood

# During a turn
self.stream.publish("agent", {"type": "tool_call_started", "tool_id": "search"})''',
        "impl": (
            "### Same-Workflow hosting\n\n"
            "For agents, host the stream on the Session that does the work so lifecycle aligns.\n\n"
            "### Limits\n\n"
            "Target modest subscriber counts (UI tabs), not thousands of consumers per Workflow.\n"
            "Skip for ultra-low-latency audio streaming."
        ),
        "when": (
            "Use for agent UIs that show live tool and token progress.\n"
            "Query-only snapshots are enough for admin dashboards that refresh slowly."
        ),
        "benefits": (
            "You get reconnectable live progress with durable offsets.\n"
            "You must manage stream storage across Continue-As-New."
        ),
        "table": (
            "| Approach | Durable cursor | Fits agents |\n"
            "| :--- | :--- | :--- |\n"
            "| Progress Streaming | Yes | Yes |\n"
            "| Query polling | Snapshot only | Coarse |\n"
            "| Side-channel websocket | No | Fragile |"
        ),
        "practices": [
            "**Publish from Workflow or via validated Signals** so history stays coherent.",
            "**Batch small token events** to limit history growth.",
            "**Authorize subscribers** per session.",
        ],
        "pitfalls": [
            "**Publishing secrets in stream payloads.**",
            "**Assuming real-time media suitability.**",
        ],
        "related": [
            "[Standardized Event Stream](/standardized-event-stream)",
            "[HTTP Channel Agent](/http-channel-agent)",
            "[Session Workflow](/session-workflow)",
        ],
        "refs": [
            "[Temporal Docs: Workflow message passing](https://docs.temporal.io/encyclopedia/workflow-message-passing)",
        ],
    },
    "prompt-versioning": {
        "title": "Prompt Versioning",
        "icon": "continue-as-new-icon.svg",
        "overview": (
            "The Prompt Versioning pattern treats system prompts and tool instructions as versioned "
            "artifacts referenced by Durable Model Calls so behavior is reproducible and safe to change "
            "while Sessions are open.\n"
            "Primitives used: Durable Model Call inputs, Workflow versioning or explicit prompt_id, evals."
        ),
        "problem": (
            "Editing a prompt string in place changes in-flight Sessions unpredictably and makes "
            "evals non-reproducible."
        ),
        "solution": (
            "Store prompts under stable IDs/versions (files or config).\n"
            "Pass `prompt_id` + `prompt_version` into model Activities.\n"
            "Use Temporal Worker Versioning or an explicit pin in Session state when behavior must "
            "not change mid-session."
        ),
        "mermaid": """flowchart LR
    Files[Versioned prompts] --> Pin[Session pin]
    Pin --> Act[Model Activity]
    Act --> Eval[Eval fixtures]""",
        "walk": [
            "Authors commit prompt files with versions.",
            "A Session pins a prompt version at start (or inherits worker deployment version).",
            "Model Activities load that exact prompt text.",
            "Evals reference the same IDs for reproducibility.",
        ],
        "code": '''PROMPTS = {
    ("researcher", "v3"): "You are a careful researcher...",
}

@activity.defn
async def call_llm(model: str, prompt_id: str, prompt_version: str, user: str) -> str:
    system = PROMPTS[(prompt_id, prompt_version)]
    return await provider.complete(model, system, user)''',
        "impl": (
            "### Mid-session changes\n\n"
            "Prefer pinning at session start.\n"
            "If you must change prompts for open Sessions, use explicit versioning APIs or "
            "Continue-As-New onto new code with a recorded decision event.\n\n"
            "### Evals\n\n"
            "Fixtures should assert prompt_version in events or inputs."
        ),
        "when": (
            "Use for any production agent whose prompt affects safety or revenue.\n"
            "Hard-coded strings are acceptable only for throwaway demos."
        ),
        "benefits": (
            "You can reproduce and roll back behavior.\n"
            "You maintain a prompt catalog beside code."
        ),
        "table": (
            "| Approach | Reproducible | Safe for in-flight |\n"
            "| :--- | :--- | :--- |\n"
            "| Versioned prompt IDs | Yes | Yes if pinned |\n"
            "| Mutable shared string | No | No |\n"
            "| Prompt in DB without version | Weak | Risky |"
        ),
        "practices": [
            "**Include prompt_version in model_call events.**",
            "**Review prompt changes like code.**",
            "**Run evals before promoting a new version.**",
        ],
        "pitfalls": [
            "**Hot-editing prod prompts without pins.**",
            "**Different workers resolving different file contents for the same version label.**",
        ],
        "related": [
            "[Durable Model Call](/durable-model-call)",
            "[Eval-Backed Behavior Checks](/eval-backed-behavior-checks)",
            "[Continue-As-New Session](/continue-as-new-session)",
        ],
        "refs": [
            "[Temporal Docs: Versioning](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning)",
        ],
    },
}


def patch_config() -> None:
    path = ROOT / "docs" / ".vitepress" / "config.mts"
    text = path.read_text()
    old_tool = """          { text: 'Durable Model Call', link: '/durable-model-call' },
          { text: 'Tool Retry Profiles', link: '/tool-retry-profiles' },
        ]
      },
      {
        text: 'Human-in-the-loop Patterns',"""
    new_tool = """          { text: 'Durable Model Call', link: '/durable-model-call' },
          { text: 'Agent Tool Loop', link: '/agent-tool-loop' },
          { text: 'Structured Model Output', link: '/structured-model-output' },
          { text: 'Provider Retry Delegation', link: '/provider-retry-delegation' },
          { text: 'Model Error Classification', link: '/model-error-classification' },
          { text: 'Rate-Limit Aware Model Calls', link: '/rate-limit-aware-model-calls' },
          { text: 'Model Timeout Profiles', link: '/model-timeout-profiles' },
          { text: 'Tool Retry Profiles', link: '/tool-retry-profiles' },
          { text: 'Prompt Versioning', link: '/prompt-versioning' },
        ]
      },
      {
        text: 'Human-in-the-loop Patterns',"""
    if old_tool not in text:
        raise SystemExit("config tool section not found")
    text = text.replace(old_tool, new_tool)

    old_sub = """          { text: 'Fan-Out Subagents', link: '/fanout-subagents' },
          { text: 'Remote Subagent', link: '/remote-subagent' },
        ]
      },
      {
        text: 'Code Mode & Sandbox Patterns',"""
    new_sub = """          { text: 'Fan-Out Subagents', link: '/fanout-subagents' },
          { text: 'Best-Effort Parallel Tools', link: '/best-effort-parallel-tools' },
          { text: 'Remote Subagent', link: '/remote-subagent' },
        ]
      },
      {
        text: 'Code Mode & Sandbox Patterns',"""
    text = text.replace(old_sub, new_sub)

    old_obs = """          { text: 'Standardized Event Stream', link: '/standardized-event-stream' },
          { text: 'Agent Tracing', link: '/agent-tracing' },"""
    new_obs = """          { text: 'Standardized Event Stream', link: '/standardized-event-stream' },
          { text: 'Progress Streaming', link: '/progress-streaming' },
          { text: 'Agent Tracing', link: '/agent-tracing' },"""
    text = text.replace(old_obs, new_obs)
    path.write_text(text)
    print("updated config.mts")


def patch_category(path: Path, tiles_html: str, choosing_extra: str) -> None:
    text = path.read_text()
    # Insert tiles before closing </div>\n\n## Choosing
    marker = "</div>\n\n## Choosing a Pattern"
    if marker not in text:
        raise SystemExit(f"marker missing in {path}")
    text = text.replace(marker, tiles_html + "\n</div>\n\n## Choosing a Pattern", 1)
    # Append choosing lines before Related Sections
    rel = "\n## Related Sections"
    text = text.replace(rel, "\n" + choosing_extra + rel, 1)
    path.write_text(text)


def tile(slug: str, title: str, desc: str, icon: str = "child-workflows-icon.svg") -> str:
    return f"""\
<div class="pattern-tile">
<a href="{slug}">
<div class="pattern-tile-header">
<img src="/images/{icon}" alt="{title}">
<span>{title}</span>
</div>
<p>{desc}</p>
</a>
</div>"""


def patch_index() -> None:
    path = DOCS / "index.md"
    text = path.read_text()
    # Tool section: insert before Tool overview tile
    tool_overview = """<div class="pattern-tile">
<a href="tool-model-call-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Tool & Model Call Patterns">
<span>Tool & Model Call Patterns Overview</span>
</div>
<p>These patterns make model and tool calls durable Temporal Activities or deterministic Workflow code.</p>
</a>
</div>"""
    tool_tiles = "\n".join(
        [
            tile("agent-tool-loop", "Agent Tool Loop", "Durable model↔tool loop until a final reply.", "polling-icon.svg"),
            tile("structured-model-output", "Structured Model Output", "Schema-validated model responses.", "request-response-icon.svg"),
            tile("provider-retry-delegation", "Provider Retry Delegation", "Disable provider SDK retries; Temporal owns backoff.", "fixed-count-retries-icon.svg"),
            tile("model-error-classification", "Model Error Classification", "Retryable vs non-retryable provider errors.", "non-retryable-errors-icon.svg"),
            tile("rate-limit-aware-model-calls", "Rate-Limit Aware Model Calls", "Honor Retry-After via next_retry_delay.", "downstream-rate-limiting-icon.svg"),
            tile("model-timeout-profiles", "Model Timeout Profiles", "Timeouts by chat, reasoning, search, and tools.", "updatable-timer-icon.svg"),
            tile("prompt-versioning", "Prompt Versioning", "Pin reproducible prompt IDs for in-flight sessions.", "continue-as-new-icon.svg"),
        ]
    )
    if tool_overview not in text:
        raise SystemExit("tool overview tile missing")
    text = text.replace(tool_overview, tool_tiles + "\n" + tool_overview)

    sub_overview = """<div class="pattern-tile">
<a href="subagent-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Subagent & Multi-agent Patterns">
<span>Subagent & Multi-agent Patterns Overview</span>
</div>
<p>These patterns compose agents as typed toolsets and durable child sessions.</p>
</a>
</div>"""
    text = text.replace(
        sub_overview,
        tile(
            "best-effort-parallel-tools",
            "Best-Effort Parallel Tools",
            "Parallel tools that continue with partial successes.",
            "parallel-execution-icon.svg",
        )
        + "\n"
        + sub_overview,
    )

    obs_overview = """<div class="pattern-tile">
<a href="observability-patterns">
<div class="pattern-tile-header">
<img src="/images/child-workflows-icon.svg" alt="Observability & Operations Patterns">
<span>Observability & Operations Patterns Overview</span>
</div>
<p>These patterns make agent behavior reconstructable from events, traces, and metrics.</p>
</a>
</div>"""
    text = text.replace(
        obs_overview,
        tile(
            "progress-streaming",
            "Progress Streaming",
            "Durable cursored live progress for agent UIs.",
            "event-accumulator-icon.svg",
        )
        + "\n"
        + obs_overview,
    )
    path.write_text(text)
    print("updated index.md")


def main() -> None:
    for slug, page in NEW.items():
        (DOCS / f"{slug}.md").write_text(mod.render(slug, page))
        print("wrote", slug)

    patch_config()
    patch_index()

    # Category pages
    tool_tiles = "\n".join(
        [
            tile("agent-tool-loop", "Agent Tool Loop", "Durable model↔tool loop until a final reply.", "polling-icon.svg"),
            tile("structured-model-output", "Structured Model Output", "Schema-validated model responses.", "request-response-icon.svg"),
            tile("provider-retry-delegation", "Provider Retry Delegation", "Disable provider SDK retries; Temporal owns backoff.", "fixed-count-retries-icon.svg"),
            tile("model-error-classification", "Model Error Classification", "Retryable vs non-retryable provider errors.", "non-retryable-errors-icon.svg"),
            tile("rate-limit-aware-model-calls", "Rate-Limit Aware Model Calls", "Honor Retry-After via next_retry_delay.", "downstream-rate-limiting-icon.svg"),
            tile("model-timeout-profiles", "Model Timeout Profiles", "Timeouts by operation class.", "updatable-timer-icon.svg"),
            tile("prompt-versioning", "Prompt Versioning", "Pin reproducible prompt versions.", "continue-as-new-icon.svg"),
        ]
    )
    tool_choose = "\n".join(
        [
            "**You need a multi-step tool-using turn:** use [Agent Tool Loop](/agent-tool-loop).",
            "**You need typed model fields:** use [Structured Model Output](/structured-model-output).",
            "**You need Temporal to own retries:** use [Provider Retry Delegation](/provider-retry-delegation).",
            "**You need correct retry vs fail behavior:** use [Model Error Classification](/model-error-classification).",
            "**You need Retry-After support:** use [Rate-Limit Aware Model Calls](/rate-limit-aware-model-calls).",
            "**You mix fast and slow models/tools:** use [Model Timeout Profiles](/model-timeout-profiles).",
            "**You need reproducible prompts:** use [Prompt Versioning](/prompt-versioning).",
        ]
    )
    patch_category(DOCS / "tool-model-call-patterns.md", tool_tiles, tool_choose)

    patch_category(
        DOCS / "subagent-patterns.md",
        tile(
            "best-effort-parallel-tools",
            "Best-Effort Parallel Tools",
            "Parallel tools that continue with partial successes.",
            "parallel-execution-icon.svg",
        ),
        "**You need parallel searches that tolerate partial failure:** use [Best-Effort Parallel Tools](/best-effort-parallel-tools).",
    )
    patch_category(
        DOCS / "observability-patterns.md",
        tile(
            "progress-streaming",
            "Progress Streaming",
            "Durable cursored live progress for agent UIs.",
            "event-accumulator-icon.svg",
        ),
        "**You need live UI progress with reconnect:** use [Progress Streaming](/progress-streaming).",
    )
    print("done")


if __name__ == "__main__":
    main()
