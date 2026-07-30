from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError

with workflow.unsafe.imports_passed_through():
    from activities import CompletionActivities
    from shared import MAX_SWEEPS, MAX_TURNS, TIMEOUT, FallbackConfig


# Default fallback policy: sweep the providers in preference order, giving each a
# retry budget of 3 before failover. Each outcome spends against that budget — a
# 429 (rate limited) is cheap to retry in place; a 500 (server error) burns the
# whole budget at once; a TIMEOUT costs 2, so a provider fails over on its second
# timed-out call. Callers can override this per Workflow execution.
DEFAULT_CONFIG = FallbackConfig(
    providers=["anthropic", "openai", "gemini"],
    budget=3,
    error_cost={"429": 1, "500": 3, str(TIMEOUT): 2},
    default_error_cost=2,
)


# ProviderFallbackWorkflow runs an agentic tool-calling loop. Each turn calls the
# model (generate); if the model asks for a tool, the Workflow runs it and feeds
# the output into the next turn, until the model returns a final answer. The
# provider that answered is reused as the preferred provider for the next turn,
# so a healthy provider is not re-swept from the top of the preference list every
# time — only a fresh failure triggers another fallback sweep.
@workflow.defn
class ProviderFallbackWorkflow:
    @workflow.run
    async def run(self, question: str, config: FallbackConfig = DEFAULT_CONFIG) -> str:
        preferred_provider = config.providers[0]
        prompt = question

        for turn in range(1, MAX_TURNS + 1):
            # generate sweeps providers internally; maximum_attempts caps the
            # sweep at MAX_SWEEPS passes over the provider list. The Activity
            # summary (shown in the Temporal UI/CLI) names the provider this turn
            # starts with. A healthy call returns in a couple of seconds; a hung
            # provider call breaches start_to_close_timeout and Temporal retries
            # the Activity with a timeout, which drives the timeout failover.
            # heartbeat_timeout sits above it so the start-to-close timeout — not a
            # missed heartbeat — is what trips a hang.
            result = await workflow.execute_activity_method(
                CompletionActivities.generate,
                args=[prompt, preferred_provider, config],
                start_to_close_timeout=timedelta(seconds=6),
                heartbeat_timeout=timedelta(seconds=20),
                retry_policy=RetryPolicy(
                    maximum_attempts=MAX_SWEEPS * len(config.providers)
                ),
                summary=f"generate ({preferred_provider})",
            )
            preferred_provider = result.provider  # stick with the provider that just worked
            workflow.logger.info(f"turn {turn}: answered by {result.provider}")

            if not result.tool_call:
                return result.text  # final answer — the agent is done

            # The model requested a tool. Run it, then feed the output into the
            # next turn.
            output = await workflow.execute_activity_method(
                CompletionActivities.run_tool,
                args=[result.tool_call, question],
                start_to_close_timeout=timedelta(seconds=10),
            )
            prompt = f"[{result.tool_call} output] {output}"

        raise ApplicationError(
            f"agent did not finish within {MAX_TURNS} turns",
            type="AgentLoopExhausted",
            non_retryable=True,
        )
