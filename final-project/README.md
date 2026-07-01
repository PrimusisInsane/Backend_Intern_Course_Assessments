# Final Project — Backend

A GraphQL backend with JWT authentication, role-based access control, Redis caching, ARQ background jobs, a MongoDB activity feed, a thin REST layer, and a gRPC demo service — built incrementally across an internship, consolidated here into one clean, tested, documented codebase.

This project is designed to be picked up and run by someone who was not part of building it — a frontend developer, a DevOps engineer, or a new team member.

---

## What "Deployable" Means Here

This project is **not** a live, internet-hosted service. There is no public URL, no domain, no cloud hosting account tied to it. "Deployable" means: anyone with Docker installed can clone this repository, run one command, and get a fully working backend on their own machine — ready to build a frontend against, or adapt for whatever infrastructure they use (AWS, Render, a bare VPS, anything).

---

## Architecture Overview

```
                         ┌─────────────┐
       Browser /         │             │
       Frontend  ───────▶│   FastAPI   │
       (GraphQL)         │  + Ariadne  │
                         └──────┬──────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                  ▼
        ┌──────────┐      ┌──────────┐      ┌──────────┐
        │ PostgreSQL│     │   Redis   │      │  MongoDB  │
        │ (source of│     │ (cache +  │      │(denormal- │
        │  truth)   │     │ job queue)│      │ ized feed)│
        └──────────┘      └─────┬────┘      └─────▲─────┘
                                 │                  │
                                 ▼                  │
                          ┌─────────────┐           │
                          │ ARQ Worker  │───────────┘
                          │ (background │
                          │  jobs)      │
                          └─────────────┘
```

**Request flow (read):** GraphQL query → resolver checks cache (Redis) → cache miss → service layer queries Postgres → result cached → returned.

**Request flow (write):** GraphQL mutation → service layer writes to Postgres → enqueues an activity-log job to Redis → cache invalidated → mutation returns immediately. The ARQ worker picks up the queued job separately and writes the log to both Postgres and MongoDB.

**Layered code structure:**
```
schema.graphql / REST routes   → WHAT exists (the API surface)
resolvers / route handlers     → WHO handles each request (thin)
services                       → HOW it works (business logic, ownership, roles)
repositories                   → the actual database queries
models                         → table definitions
```
The same service functions are called from GraphQL resolvers, REST routes, and the gRPC server — proving the business logic genuinely doesn't care which protocol is calling it.

---

## Tech Stack

- **FastAPI** + **Ariadne** — GraphQL API (primary interface)
- **FastAPI routes** — thin REST layer (`/health`, `/auth/register`, `/auth/login`)
- **SQLAlchemy 2.0** (typed `Mapped[]` style) + **Alembic** — ORM and migrations
- **PostgreSQL** — primary database
- **Redis** — caching (with TTL and invalidation) and the ARQ job queue
- **ARQ** — async background worker (activity logging)
- **MongoDB** (Motor) — denormalized activity feed
- **gRPC** — `UserLookupService` demo (proto-defined contract, generated stubs)
- **pytest** / **pytest-asyncio** / **pytest-cov** / **httpx** — testing
- **Ruff** / **Black** / **Mypy** — linting, formatting, static type checking
- **Docker** + **Docker Compose** — containerized local environment
- **Poetry** — dependency management

---

## Quick Start (Docker — Recommended)

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux), running
- A `.env` file in the project root (copy `.env.example` and fill in `SECRET_KEY`)

### Run everything

```bash
docker compose up -d --build
```

This starts five containers: `api`, `worker`, `postgres`, `redis`, `mongo`.

Check everything is healthy:

```bash
docker compose ps
```

All five should show `Up`.

### Run database migrations

The Postgres container exposes port `5432` to your host, so Alembic can run from your local machine:

```bash
poetry run alembic upgrade head
```

(Requires your local `.env`'s `DATABASE_URL` to point at `localhost:5432`, not the in-container service name — see Environment Variables below.)

### Verify it's working

```
http://localhost:8000/graphql    → GraphQL Playground
http://localhost:8000/docs       → REST API docs (Swagger)
http://localhost:8000/health/db  → REST health check
```

Run a register mutation in the Playground to confirm the full stack works:

```graphql
mutation {
  register(input: {name: "Test", email: "test@example.com", age: 25, password: "test1234"}) {
    accessToken
    tokenType
  }
}
```

---

## Quick Start (Without Docker)

```bash
# Terminal 1 — API
poetry run uvicorn app.main:app --reload

# Terminal 2 — ARQ worker
poetry run arq app.worker.WorkerSettings
```

Redis and MongoDB still need to be running somewhere — either:
```bash
docker compose up -d redis mongo postgres
```
or installed natively on your machine.

---

## Environment Variables

See `.env.example` for the full annotated list. Key points:

| Variable | Local (.env) | Inside Docker |
|---|---|---|
| `DATABASE_URL` | `...@localhost:5432/...` | `...@postgres:5432/...` |
| `TEST_DATABASE_URL` | `...@localhost:5433/...` | n/a (tests run locally) |
| `REDIS_URL` | `redis://localhost:6379/0` | `redis://redis:6379/0` |
| `MONGODB_URL` | `mongodb://localhost:27017` | `mongodb://mongo:27017` |

The only difference between local and containerized environments is the **hostname** — `localhost` outside containers, the **service name** (`postgres`, `redis`, `mongo`) inside Docker's internal network. Docker Compose injects container-specific values via the `environment:` block in `docker-compose.yml`; your local `.env` is only used when running outside containers.

**Why service names instead of `localhost` inside Docker:** each container has its own isolated network namespace. Inside a container, `localhost` only ever refers to *that same container*. Docker Compose's internal DNS resolves service names (`postgres`, `redis`, `mongo`) to the correct container IPs automatically.

---

## API Surface

### GraphQL (primary) — `/graphql`

```graphql
type Query {
  me, users, user(id), projects, project(id), getProjectById(id),
  searchProjects(keyword), projectTasks(projectId), projectLogs(projectId),
  tasks, task(id), getTaskById(id), searchTasks(keyword), taskLogs(taskId),
  redisHealth, dbHealth
}

type Mutation {
  register, login,
  createProject, updateProject, deleteProject,
  createTask, updateTask, deleteTask, changeTaskStatus
}
```

Full schema: `app/schema/schema.graphql`

### REST (secondary, minimal) — for environments preferring REST

| Method | Path | Purpose |
|---|---|---|
| GET | `/health/db` | Database connectivity check |
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Login, get a JWT |

These routes call the exact same service functions as the GraphQL mutations — see Architecture Overview.

### gRPC (demo) — port `50051`

`UserLookupService.GetUser(user_id) → {id, name, email, role, found}`

Run the server: `poetry run python app/grpc_server.py`
Run the client: `poetry run python app/grpc_client.py`

This is a learning demonstration of synchronous service-to-service communication, not a load-bearing part of the application (see [Microservice Boundary Thinking](#microservice-boundary-thinking) below).

---

## Authentication

```
Register → password hashed (bcrypt) → user stored
Login → password verified against hash → JWT issued (signed with SECRET_KEY)
Every request → Authorization: Bearer <token> → context builder decodes it → resolver gets current_user
```

Tokens expire after 24 hours. Roles: `member` (default, restricted to own data) and `admin` (manually promoted in the database, bypasses ownership checks).

To promote a user to admin:
```sql
UPDATE users SET role = 'admin' WHERE id = <id>;
```

---

## Testing

```bash
poetry run pytest -v              # run everything
poetry run pytest --cov=app       # with coverage report
poetry run pytest tests/test_auth.py -v   # one file
```

**38 tests across 5 files:**

| File | Covers |
|---|---|
| `tests/test_auth.py` | Password hashing, registration, login, duplicate-email rejection |
| `tests/test_ownership.py` | Ownership rules, admin override, 404 handling |
| `tests/test_health.py` | REST and GraphQL health checks |
| `tests/test_graphql.py` | Full GraphQL lifecycle — query, mutation, unauthorized, forbidden access |
| `tests/test_redis_cache.py` | Cache miss/hit behavior, invalidation on write |

**Test isolation strategy:** a dedicated test database (`test-postgres`, port `5433`, separate from your real data) combined with per-test transaction rollback. Every test that hits the live app (via `httpx.AsyncClient`) is redirected to this test database through an environment override in `tests/conftest.py`, applied before any other module imports.

---

## Code Quality

```bash
poetry run ruff check .     # lint
poetry run ruff check . --fix   # auto-fix what's safe to fix
poetry run black .          # format
poetry run mypy app --explicit-package-bases   # type-check
```

All three currently pass clean against this codebase. Models use SQLAlchemy 2.0's typed `Mapped[]` declarative style specifically so mypy can verify them properly.

---

## Microservice Boundary Thinking

This project remains a single application on purpose. The gRPC `UserLookupService` exists to demonstrate the *mechanism* (proto contracts, generated stubs, synchronous request/response between services) — not because this app currently needs to be split into microservices.

**What would justify an actual split:** a second team needing to own and deploy a piece independently; one component having dramatically different scaling needs than the rest; a genuine need for failure isolation. None of those are true here yet. Activity logging is already handled asynchronously via ARQ — the correct tool for fire-and-forget work — rather than being rebuilt as a synchronous gRPC call, because logging was never the part of this system that needed an immediate response.

---

## Troubleshooting

**Port already in use**
```bash
# find what's using it
lsof -i :8000
# or just run on a different port
poetry run uvicorn app.main:app --port 8001
```

**Database connection refused**
- Confirm the Postgres container is running: `docker compose ps`
- Confirm `DATABASE_URL` in `.env` matches the right host (`localhost` outside Docker, `postgres` inside)
- If running Alembic from your host machine, it needs `localhost:5432`, not the Docker service name

**Docker not running**
- Start Docker Desktop (Windows/Mac) or `sudo systemctl start docker` (Linux)
- `docker compose up` will fail immediately with a connection error to the Docker daemon if it's not running

**Migration error ("relation does not exist")**
- No migrations have been run yet against this database — run `poetry run alembic upgrade head`
- If you changed models, generate a new migration first: `poetry run alembic revision --autogenerate -m "description"`

**Redis connection error**
- Confirm the Redis container is running: `docker compose ps`
- Check `REDIS_URL` matches the right host for your context (local vs Docker)
- The app is designed to degrade gracefully if Redis is unreachable — `redisHealth` will report `"fail: <error>"` instead of crashing the whole API; if you see a 500 error instead, check that `app/schema/context.py`'s Redis pool creation is wrapped in a try/except

**GraphQL schema mismatch ("Cannot query field 'X' on type 'Y'")**
- The field doesn't exist in `app/schema/schema.graphql` — check spelling and that it's defined under the right type
- If you just added a field/resolver, restart the server — without `--reload`, code changes (including `.graphql` file changes) aren't picked up automatically

**Token missing / "Not authenticated"**
- The `Authorization: Bearer <token>` header wasn't sent, or the token expired (24 hour lifetime) — log in again to get a fresh one
- In the GraphQL Playground, check the Authorization tab isn't conflicting with a manually-added header in the Headers tab

**Trailing slash 307 redirect on `/graphql`**
- FastAPI's `app.mount("/graphql", ...)` requires the trailing slash — use `/graphql/`, not `/graphql`, especially when calling it programmatically (e.g. with `httpx`), since automated clients don't follow redirects by default the way browsers do

**Known harmless warnings**
- SQLAlchemy `SAWarning` about overlapping relationships on the `User↔Project↔Membership` many-to-many setup — cosmetic, does not affect correctness, left as-is after an earlier attempt to silence it via `overlaps=` introduced a real bug that was reverted
- `bcrypt`/`graphql-core` need to be pinned to specific versions (`bcrypt==4.0.1`, `graphql-core==3.2.6`) — newer releases of both have caused real breakage across this project's history; `pyproject.toml` already has them pinned correctly

---

## Project History (Week-by-Week)

This project consolidates work built incrementally:

- **Django reference** — comparison study against FastAPI
- **FastAPI + REST** — JWT auth, password hashing, role/ownership rules, AWS RDS
- **GraphQL (Ariadne)** — REST migrated to GraphQL with the same service layer underneath
- **Redis + ARQ** — caching with TTL/invalidation, background job processing
- **Docker + MongoDB + gRPC** — full containerization, denormalized activity feed, gRPC demo service, microservice boundary thinking
- **This final project** — consolidation, automated testing, code quality tooling, documentation

---

## Running Order Summary (Cheat Sheet)

```bash
# First time setup
cp .env.example .env              # fill in SECRET_KEY
docker compose up -d --build
poetry run alembic upgrade head

# Day to day
docker compose up -d              # start everything
docker compose logs api --tail 20 # check logs
poetry run pytest -v              # run tests
docker compose down               # stop everything

# Code quality, before committing
poetry run ruff check . --fix
poetry run black .
poetry run mypy app --explicit-package-bases
poetry run pytest -v
```