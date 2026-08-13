import asyncio

from temporalio import activity

_JOBS: dict[str, int] = {}


@activity.defn
async def start_job(goal: str) -> str:
    job_id = f"job-{abs(hash(goal)) % 10000}"
    _JOBS[job_id] = 0
    return job_id


@activity.defn
async def poll_job_until_done(job_id: str) -> dict:
    while True:
        if activity.is_cancelled():
            raise asyncio.CancelledError()
        ticks = _JOBS.get(job_id, 0) + 1
        _JOBS[job_id] = ticks
        activity.heartbeat(ticks)
        if ticks >= 3:
            return {"job_id": job_id, "state": "done", "result": f"done-{job_id}"}
        await asyncio.sleep(0.05)
