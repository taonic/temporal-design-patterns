import asyncio, uuid
from temporalio.client import Client
from shared import TASK_QUEUE
from workflows import AgentTurnWorkflow

async def main() -> None:
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        AgentTurnWorkflow.run,
        id=f"mop-{uuid.uuid4().hex[:8]}", task_queue=TASK_QUEUE,
    )
    model_keys = sorted(result["model"]["value"].keys())
    has_secret = "secret_token" in result["channel"] and "secret_token" not in result["model"]["value"]
    print(f"model_keys={model_keys}|secret_channel_only={has_secret}")

if __name__ == "__main__":
    asyncio.run(main())
