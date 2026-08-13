from temporalio import activity


@activity.defn
async def call_model(definition_revision: str, binding_revision: str, user_message: str) -> str:
    return f"{definition_revision}|{binding_revision}|{user_message}"
