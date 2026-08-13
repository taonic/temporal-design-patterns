from temporalio import activity

_STORE: dict[str, str] = {}


@activity.defn
async def store_blob(text: str) -> str:
    ref = f"blob-{len(text)}-{abs(hash(text)) % 100000}"
    _STORE[ref] = text
    return ref


@activity.defn
async def load_blob(ref: str) -> str:
    return _STORE[ref]
