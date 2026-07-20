import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import CompletionActivities, LLMRegistry
from shared import TASK_QUEUE
from workflows import ProviderFallbackWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    # One registry shared by every Activity this worker runs, injected into the
    # activities instance instead of reached for as a module global. See the note in
    # activities.py on why this is safe only for same-worker, per-Workflow-keyed state.
    registry = LLMRegistry()
    activities = CompletionActivities(registry)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ProviderFallbackWorkflow],
        activities=[activities.generate, activities.run_tool],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
