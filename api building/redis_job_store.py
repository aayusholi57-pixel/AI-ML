import json
import os

try:
    import redis  # the real client — used whenever fake_server is not given
except ImportError:
    redis = None

JOB_TTL_SECONDS = 3600  # jobs auto-expire after an hour — Redis does this natively


def get_redis_client(fake_server=None):
    """fake_server: pass a fakeredis.FakeServer() to get an in-memory client
    for testing/class use. Two clients built with the SAME fake_server share
    state, standing in for two workers talking to the same real Redis. Omit
    it (the default) to connect to a real server via REDIS_URL."""
    if fake_server is not None:
        import fakeredis
        return fakeredis.FakeRedis(server=fake_server)
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(redis_url)


def set_job(client, job_id: str, data: dict):
    client.set(f"job:{job_id}", json.dumps(data), ex=JOB_TTL_SECONDS)


def get_job(client, job_id: str):
    raw = client.get(f"job:{job_id}")
    if raw is None:
        return None
    return json.loads(raw)


def update_job(client, job_id: str, **fields):
    job = get_job(client, job_id) or {}
    job.update(fields)
    set_job(client, job_id, job)
    return job


if __name__ == "__main__":
    import fakeredis

    print("=== Proving the store is external to any one client handle ===")
    print("(this is what makes it safe across --workers N — see formulas.md §2)\n")

    # One shared fake server; two SEPARATE client objects, standing in for
    # two separate worker processes each holding their own connection.
    shared_server = fakeredis.FakeServer()
    worker_a = get_redis_client(fake_server=shared_server)
    worker_b = get_redis_client(fake_server=shared_server)

    job_id = "demo-job-001"

    print(f"worker A: set_job({job_id!r}, status=queued)")
    set_job(worker_a, job_id, {"status": "queued", "result": None})

    seen_by_b = get_job(worker_b, job_id)
    print(f"worker B: get_job({job_id!r}) -> {seen_by_b}")
    assert seen_by_b == {"status": "queued", "result": None}, "worker B should see worker A's write"
    print("  OK: worker B (a different client handle) sees worker A's write.\n")

    print(f"worker B: update_job({job_id!r}, status=done, result=...)")
    updated = update_job(worker_b, job_id, status="done", result={"predicted_digit": 0, "confidence": 0.9954})
    print(f"  -> {updated}")

    seen_by_a = get_job(worker_a, job_id)
    print(f"worker A: get_job({job_id!r}) -> {seen_by_a}")
    assert seen_by_a["status"] == "done", "worker A should see worker B's update"
    assert seen_by_a["result"]["predicted_digit"] == 0
    print("  OK: worker A sees worker B's update.\n")

    missing = get_job(worker_a, "does-not-exist")
    assert missing is None
    print("get_job on an unknown id -> None (correct, no KeyError).\n")

    ttl = worker_a.ttl(f"job:{job_id}")
    print(f"TTL on the job key: {ttl}s (expected close to {JOB_TTL_SECONDS}s)")
    assert 0 < ttl <= JOB_TTL_SECONDS

    print("\nAll checks passed. Note: this proves the mechanism (client-server")
    print("separation) using two client HANDLES in the same process. Two REAL")
    print("separate OS processes need an actual out-of-process Redis server —")
    print("fakeredis's FakeServer is itself in-process. See docker-compose.yml")
    print("+ deployment_commands.md for how to verify that for real at home.")
