from temporalio import activity

from shared import TransferDetails


@activity.defn
async def withdraw(details: TransferDetails) -> None:
    activity.logger.info(f"Withdrew ${details.amount} from {details.fromAccount}")


@activity.defn
async def deposit(details: TransferDetails) -> None:
    activity.logger.info(f"Deposited ${details.amount} to {details.toAccount}")


@activity.defn
async def notify_downstream(details: TransferDetails) -> None:
    activity.logger.info(
        f"Notify: simulating downstream failure for transfer {details.transferId}"
    )
    # Comment out the raise to watch the saga succeed end-to-end:
    raise RuntimeError("notification service down")


@activity.defn
async def withdraw_compensation(details: TransferDetails) -> None:
    activity.logger.info(f"Refunded ${details.amount} to {details.fromAccount}")


@activity.defn
async def deposit_compensation(details: TransferDetails) -> None:
    activity.logger.info(
        f"Reversed deposit of ${details.amount} from {details.toAccount}"
    )
