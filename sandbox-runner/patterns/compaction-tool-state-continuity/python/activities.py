from temporalio import activity


@activity.defn
async def compact_transcript(transcript: list[str]) -> str:
    return f"summary({len(transcript)}):" + ";".join(transcript[-2:])
