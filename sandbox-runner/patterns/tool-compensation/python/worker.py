import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import (
    charge_customer,
    close_ticket,
    create_ticket,
    notify_user,
    refund_charge,
)
from shared import TASK_QUEUE
from workflows import AgentSessionWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AgentSessionWorkflow],
        activities=[
            create_ticket,
            charge_customer,
            notify_user,
            close_ticket,
            refund_charge,
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
