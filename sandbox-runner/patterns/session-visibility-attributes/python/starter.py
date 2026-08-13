import asyncio
import subprocess
import uuid

from temporalio.client import Client
from temporalio.common import TypedSearchAttributes, SearchAttributePair

from shared import TASK_QUEUE, TENANT_ID, TURN_STATUS
from workflows import AgentSessionWorkflow


def ensure_search_attributes() -> None:
    for name in ("AgentTurnStatus", "AgentTenantId"):
        subprocess.run(
            [
                "temporal",
                "operator",
                "search-attribute",
                "create",
                "--name",
                name,
                "--type",
                "Keyword",
                "--address",
                "localhost:7233",
            ],
            check=False,
            capture_output=True,
        )


async def main() -> None:
    ensure_search_attributes()
    client = await Client.connect("localhost:7233")
    session_id = f"session-{uuid.uuid4().hex[:8]}"
    tenant_id = "tenant-demo"
    handle = await client.start_workflow(
        AgentSessionWorkflow.run,
        args=[session_id, tenant_id],
        id=session_id,
        task_queue=TASK_QUEUE,
        search_attributes=TypedSearchAttributes(
            [
                SearchAttributePair(TURN_STATUS, "running"),
                SearchAttributePair(TENANT_ID, tenant_id),
            ]
        ),
    )
    for _ in range(50):
        status = await handle.query(AgentSessionWorkflow.turn_status)
        if status == "awaiting_approval":
            break
        await asyncio.sleep(0.1)
    status = await handle.query(AgentSessionWorkflow.turn_status)
    await handle.signal(AgentSessionWorkflow.approve)
    final = await handle.result()
    print(f"parked={status}|final={final}")


if __name__ == "__main__":
    asyncio.run(main())
