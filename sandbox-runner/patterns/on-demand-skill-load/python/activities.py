from temporalio import activity
from temporalio.exceptions import ApplicationError

from shared import SKILLS


@activity.defn
async def load_skill_body(catalog_snapshot_id: str, name: str) -> str:
    skill = SKILLS.get(name)
    if skill is None:
        raise ApplicationError("unknown_skill", type="UnknownSkill", non_retryable=True)
    return f"{catalog_snapshot_id}|{skill['body']}"


@activity.defn
async def call_model_with_context(user_message: str, loaded_body: str) -> str:
    return f"used_skill={bool(loaded_body)}|msg={user_message}|body_len={len(loaded_body)}"
