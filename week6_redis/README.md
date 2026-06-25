# Redis, Caching, and Background Jobs

## Overview

This project uses Redis for two distinct purposes:

1. **Caching** — speeding up expensive read queries (`tasks`, `projects`) by storing results temporarily with a TTL
2. **Background job queue** — offloading slow or non-critical work (activity logging) to a separate worker process via ARQ, so API responses aren't delayed by it

## Running Redis

Redis runs locally via Docker:

```bash
docker compose -f infra/docker-compose.redis.yml up -d
```

Verify it's running:

```bash
redis-cli ping
# Expected: PONG
```

Stop it:

```bash
docker compose -f infra/docker-compose.redis.yml down
```

## Environment Variables

Add to `.env`:

```env
REDIS_URL=redis://localhost:6379/0
```

## Running the ARQ Worker

The worker is a **separate process** from the API server. Both must be running for background jobs to actually execute.

**Terminal 1 — API server:**
```bash
poetry run uvicorn app.main:app --reload
```

**Terminal 2 — ARQ worker:**
```bash
poetry run arq app.worker.WorkerSettings
```

If the worker isn't running, jobs will sit queued in Redis indefinitely until a worker process starts and picks them up. The API will still respond successfully (the job is enqueued, not run inline) — but the actual logging won't happen until a worker is online.

## Checking Worker Health

Watch the worker terminal for lines like:

```
12:34:56:   0.20s → write_activity_log(action='created', task_id=12, user_id=3)
[ARQ] Logged: created for user 3
12:34:57:   0.85s ← write_activity_log ●
```

`→` means a job started, `←` means it finished, and `●` means it succeeded. A `✗` or stack trace in place of `●` means the job failed — check the printed error for details.

## Caching Pattern Used

Every cached read query follows the same pattern:

```python
cache_key = f"tasks:{user_id}:list:{limit}:{offset}:{done}"
cached = await cache_get(cache_key)
if cached is not None:
    return cached

result = list_tasks_service(...)
await cache_set(cache_key, result, ttl=60)
return result
```

1. Check Redis first using a key built from the user ID and filters
2. If found, return immediately — no database hit
3. If missing, query Postgres, then store the result in Redis with a 60 second TTL before returning

### Key naming convention

```
tasks:{user_id}:list:{limit}:{offset}:{done}
projects:{user_id}:list:{limit}:{offset}
```

Each user's cached lists are isolated by `user_id`, so one user's cache can never leak into another's response.

## Cache Invalidation

Whenever a task or project is created, updated, or deleted, the relevant cache keys for that user are wiped immediately:

```python
await cache_delete_pattern(f"tasks:{user_id}:list:*")
```

This guarantees the next read after a write always reflects fresh data, rather than waiting up to 60 seconds for the TTL to naturally expire.

## When to Use FastAPI Background Tasks vs. ARQ

| | FastAPI `BackgroundTasks` | ARQ |
|---|---|---|
| Runs in | Same process as the API | Separate worker process |
| Survives API restart | No — lost if server restarts mid-task | Yes — job stays in Redis until a worker picks it up |
| Best for | Quick, low-risk, fire-and-forget work (e.g. sending a simple confirmation email) | Anything that should be retried on failure, monitored, or run independently of the API process |
| Failure visibility | Silent — exceptions just get logged, caller never knows | Worker logs success/failure explicitly per job |
| Scaling | Tied to the API server's resources | Can run multiple worker processes independently of the API |

This project uses ARQ for activity logging because:
- The log write should happen even if the API process restarts before it's done
- Failures should be visible in worker logs, not silently swallowed
- Logging work is decoupled from request/response timing — the mutation returns to the client immediately

## Redis Health Check

```graphql
query {
  redisHealth
}
```

Returns `"ok"` if Redis is reachable, or `"fail: <error message>"` if not. This endpoint does not require authentication, since health checks are typically polled by monitoring tools without a user token.