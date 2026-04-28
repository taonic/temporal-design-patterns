from temporalio import activity

from shared import OpenAccountRequest


@activity.defn
async def create_account(req: OpenAccountRequest) -> None:
    activity.logger.info(f"Created account {req.accountId} for {req.clientName}")


@activity.defn
async def add_address(req: OpenAccountRequest) -> None:
    activity.logger.info(f"Added address '{req.address}' to {req.accountId}")


@activity.defn
async def add_client(req: OpenAccountRequest) -> None:
    activity.logger.info(f"Added client {req.clientEmail} to {req.accountId}")


@activity.defn
async def add_bank_account(req: OpenAccountRequest) -> None:
    activity.logger.info(
        f"Linking bank account {req.bankAccount}: simulating downstream failure"
    )
    # Comment out the raise to watch the saga succeed end-to-end:
    raise RuntimeError("bank link service down")


@activity.defn
async def clear_postal_addresses(req: OpenAccountRequest) -> None:
    activity.logger.info(f"Cleared postal addresses for {req.accountId}")


@activity.defn
async def remove_client(req: OpenAccountRequest) -> None:
    activity.logger.info(f"Removed client from {req.accountId}")


@activity.defn
async def disconnect_bank_accounts(req: OpenAccountRequest) -> None:
    activity.logger.info(f"Disconnected any bank accounts from {req.accountId}")
