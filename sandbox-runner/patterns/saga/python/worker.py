import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import (
    add_address,
    add_bank_account,
    add_client,
    clear_postal_addresses,
    create_account,
    disconnect_bank_accounts,
    remove_client,
)
from shared import TASK_QUEUE
from workflows import OpenAccountWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[OpenAccountWorkflow],
        activities=[
            create_account,
            add_address,
            add_client,
            add_bank_account,
            clear_postal_addresses,
            remove_client,
            disconnect_bank_accounts,
        ],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'", flush=True)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
