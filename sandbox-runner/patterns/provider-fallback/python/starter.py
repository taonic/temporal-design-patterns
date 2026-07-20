import asyncio
import time

from temporalio.client import Client

from shared import TASK_QUEUE, WORKFLOW_ID_PREFIX
from workflows import ProviderFallbackWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    workflow_id = f"{WORKFLOW_ID_PREFIX}-{int(time.time() * 1000)}"
    # Change to "" (empty) to exercise the abort (invalid request) path.
    question = "What is the meaning of durable execution?"

    handle = await client.start_workflow(
        ProviderFallbackWorkflow.run,
        question,
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )
    print(f"Started workflow: {workflow_id}")

    result = await handle.result()
    print(result)
    print(
        f"Open the Temporal UI and search for '{workflow_id}' to see the agent loop and provider sweep."
    )


if __name__ == "__main__":
    asyncio.run(main())
