from dataclasses import dataclass, field
from typing import Optional

# The Workflow and the sweeping Activity both run on this Task Queue.
TASK_QUEUE = "provider-fallback-task-queue"
WORKFLOW_ID_PREFIX = "completion"

# Maximum number of full passes over the provider list before giving up.
MAX_SWEEPS = 3

# Maximum agent turns (model calls) before giving up on the tool-calling loop.
MAX_TURNS = 6

# Sentinel used both as a scripted provider outcome (a hung call) and as the
# error_cost key for a start-to-close timeout, so a timeout spends the budget the
# same way an HTTP error does. Not a real HTTP status, hence the negative value.
TIMEOUT = -1


# Error state maintained ACROSS Activity retries via heartbeat details, so a
# retried attempt resumes the sweep where the previous one left off instead of
# restarting from the first provider.
@dataclass
class ErrorState:
    # retry budget already spent per provider, accumulated across retries
    spent: dict[str, int] = field(default_factory=dict)
    # the attempt number that last recorded an HTTP outcome (success or a spent
    # budget). Any retry beyond this without advancing it was a start-to-close
    # timeout — a hung provider call Temporal killed before it could record a
    # result — so the gap between it and the current attempt counts the timeouts.
    last_resolved_attempt: int = 0


# Fallback policy passed into the generate Activity: which providers to sweep in
# preference order, how much retry budget each one gets before failover, and what
# each outcome costs against that budget — the error_cost map is keyed by HTTP
# status and by TIMEOUT, so a timed-out call spends budget like any other error.
# The keys are strings (e.g. "429", "-1"): a config crosses the JSON boundary as an
# Activity argument, and Temporal's converter cannot rebuild a dict[int, int] because
# JSON object keys are always strings. Callers look up with str(status).
@dataclass
class FallbackConfig:
    providers: list[str]
    budget: int
    error_cost: dict[str, int]
    default_error_cost: int


# What one model call returns: the provider that produced the response, the
# message text, and an optional tool the model wants to run next. No tool_call
# means the model returned a final answer.
@dataclass
class GenerateResult:
    provider: str
    text: str
    tool_call: Optional[str] = None
