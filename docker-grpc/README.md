# Docker Setup and Run Commands

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux) installed and running
- `.env` file present in the project root with required variables (see below)

## Running with Docker (recommended)

Start the full stack — API, ARQ worker, PostgreSQL, Redis, and MongoDB — with one command:

```bash
docker compose up -d --build
```

`--build` rebuilds the image from the Dockerfile. Only needed the first time, or after changing dependencies or the Dockerfile itself. On later runs:

```bash
docker compose up -d
```

Check that everything is running:

```bash
docker compose ps
```

You should see four containers: `api`, `worker`, `postgres`, `redis`, `mongo` — all showing `Up`.

View logs for any service:

```bash
docker compose logs api --tail 20
docker compose logs worker --tail 20
```

Stop everything:

```bash
docker compose down
```

Stop and also wipe the database volumes (full reset):

```bash
docker compose down -v
```

## Running Migrations Against the Containerized Database

The Postgres container exposes port `5432` on the host, so Alembic can be run from your local machine — it just needs `.env` pointed at `localhost` rather than the in-container service name:

```bash
poetry run alembic upgrade head
```

## Running Locally Without Docker (alternative)

If you prefer running services individually outside containers:

```bash
# Terminal 1 — API
poetry run uvicorn app.main:app --reload

# Terminal 2 — ARQ worker
poetry run arq app.worker.WorkerSettings

# Redis and Mongo still need to be running somewhere —
# either via docker compose up -d redis mongo,
# or installed locally.
```

## Environment Variables

| Variable | Local (.env) | Inside Docker (compose) |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/backend_db` | `postgresql://postgres:postgres@postgres:5432/backend_db` |
| `REDIS_URL` | `redis://localhost:6379/0` | `redis://redis:6379/0` |
| `MONGODB_URL` | `mongodb://localhost:27017` | `mongodb://mongo:27017` |
| `SECRET_KEY` | same value either way | same value either way |

The only difference between local and containerized environments is the **hostname** — `localhost` outside containers, the **service name** (`postgres`, `redis`, `mongo`) inside Docker's internal network. Docker Compose injects the container-specific values automatically via the `environment:` block in `docker-compose.yml`; the `.env` file is only used for local, non-Docker development.

## Why Service Names Instead of `localhost` Inside Docker

Each container in a `docker-compose.yml` setup gets its own isolated network namespace. Inside a container, `localhost` only ever refers to *that same container* — not to other containers running alongside it, even though they're on the same machine.

Docker Compose automatically creates an internal DNS so that containers can reach each other using their **service name** as a hostname. That's why `api` connects to `postgres:5432` rather than `localhost:5432` — `postgres` resolves to the actual IP address of the Postgres container on Docker's internal network.

## Verifying Everything Works

```bash
# 1. Confirm all containers are up
docker compose ps

# 2. Confirm the worker connected to Redis
docker compose logs worker --tail 5

# 3. Hit the API
# open http://localhost:8000/graphql in a browser, run a register/login mutation

# 4. Confirm Postgres has the data
docker exec -it <project-name>-postgres-1 psql -U postgres -d backend_db -c "SELECT * FROM users;"

# 5. Confirm Mongo received the denormalized activity feed
docker exec -it <project-name>-mongo-1 mongosh --eval "use backend_db; db.activity_feed.find().pretty()"
```




# Microservice Boundary Thinking

This project remains a single application (a "monolith") on purpose. This section documents how I'd think about splitting it into microservices *if* that became necessary — without actually doing it, since premature splitting adds complexity without a real payoff at this scale.

## What a Microservice Boundary Actually Means

A good microservice boundary isn't just "put this file in a different folder." It's a place where:

1. The data genuinely doesn't need to be transactionally consistent with the rest of the system in real time
2. The team/person responsible for it could reasonably change its internals without touching anything else
3. It has a clear, narrow *contract* (a few specific operations) rather than dozens of tangled responsibilities

## Looking at My Domain

```
User ──< Membership >── Project
User ──< Task
Project ──< Task
User/Task/Project ──< ActivityLog
```

### Candidates for splitting, and why (or why not)

**ActivityLog — good candidate, NOT split yet**
- Already the most isolated piece: nothing else *reads* from it to make decisions, it's pure record-keeping
- Already handled asynchronously via ARQ — meaning the architecture already tolerates it being "eventually written" rather than instantly consistent
- If this were a real product with heavy audit/compliance needs, this would likely become its own service with its own database, written to via a queue (Kafka/SQS/Redis pub-sub) rather than direct function calls
- **Why not split now**: there's no second team, no compliance requirement, and no separate scaling need yet. Splitting it would mean network calls and partial-failure handling for a feature that currently "just works" as an in-process function call.

**UserLookupService — built as a gRPC learning exercise, NOT actually split**
- Demonstrated as a proof-of-concept: a tiny gRPC service that looks up user info by ID
- In a real split, this might become a genuine **Identity Service** — the one place that knows about users, authentication, and roles, which other services call into rather than each maintaining their own copy of user data
- **Why not split now**: every part of this app already needs direct, fast access to user data for nearly every operation (ownership checks happen on almost every request). Making that a network call instead of a local function call would add latency and a new failure mode (what happens if the Identity Service is down?) for no real benefit at this scale.

**Tasks and Projects — NOT a good candidate to split apart from each other**
- They're tightly coupled: a task always belongs to a project, ownership checks need to know about both, and most queries naturally span both (`projectTasks`, `getProjectById` returning task counts, etc.)
- Splitting these into separate services would mean constant network calls just to answer "which tasks belong to this project" — a query that's currently a single, fast database join
- **This is the trap of premature splitting**: it looks like a clean boundary on a diagram, but in practice it's one tightly-coupled feature artificially cut in half

## The General Rule I'm Taking Away

> Split along boundaries where the *data* and *team* naturally diverge — not along boundaries that just look clean in a diagram.

Right now, this app has:
- One team (me)
- One real data store (Postgres) for source-of-truth data
- A queue (Redis/ARQ) already handling the one feature (logging) that's genuinely asynchronous in nature
- A cache (Redis) for performance, not for service boundaries
- A second store (MongoDB) used for one denormalized read-feed, not for splitting ownership of core data

None of that currently justifies tearing the app into separate deployable services. The gRPC exercise here exists to learn the *mechanism* (proto contracts, generated stubs, server/client request-response) — not because this app needs it today.

## When I'd Actually Reach for Microservices

- A second team needs to own and deploy a piece independently, on its own schedule
- One piece has wildly different scaling needs than the rest (e.g. needing 50 instances of a notification sender while the rest of the app needs 2)
- Strict failure isolation matters — e.g. a reporting feature should never be able to take down the core task/project API
- A piece of the domain has a genuinely different data model that doesn't fit the relational structure of the rest (which is part of why ActivityLog → Mongo made sense as a *read feed*, even without becoming a separate service)

Until one of those becomes true here, the monolith — with async background jobs for naturally-async work, and a small gRPC demo to understand the mechanism — is the right level of complexity for this project's actual needs.