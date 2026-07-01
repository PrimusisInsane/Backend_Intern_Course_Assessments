# Internship of Backend Repository

## Completed Course action 
* Week 1 - Fundamentals of Python
* Week 2 - FastAPI and Starlette
* Week 3 - Databases(Postgres/MongoDB) & Alembic
* Week 4 - Django Reference and FastAPI main backend
* Week 5 - GraphQL as the main-backend 
* Week 6 - Redis Caching
* Week 7 - Docker gRPC and Microservices



# Backend Internship — Learning Report (Weeks 1–7)

## Week 1: Python Fundamentals & SQLite Student Database

This week was primarily focused on Python fundamentals, using a student database project as the practical exercise.

**What I learned:**
- Core Python fundamentals applied through a real mini-project
- Working with SQLite as a lightweight local database
- Implementing basic CRUD operations (Create, Read, Update, Delete)
- Structuring a simple project with a `main.py` entry point
- Writing tests using `pytest`

**Project summary:** A SQLite-based student database storing at least 5 students' records, supporting adding, deleting, and tracking student information.

---

## Week 2: FastAPI, Starlette Middleware & REST Endpoints

This week introduced FastAPI as the main backend framework, moving beyond plain Python scripts into a proper API structure.

**What I learned:**
- Building REST APIs with FastAPI
- Structuring a project into packages: middlewares, exceptions, and routers
- Implementing full CRUD operations across multiple resources — users, tasks, and projects
- Using Pydantic for data validation and producing clean, structured error messages
- Assigning and using unique ID numbers to look up, update, or delete records
- Writing custom Starlette middleware to log request metadata (response time, method, path)
- Using FastAPI's built-in Swagger UI (`/docs`) for interactive API documentation
- Understanding HTTP methods in practice — `GET`, `POST`, `PUT`, `DELETE` — and how each maps to an operation

---

## Week 3: PostgreSQL Persistence, Alembic & Layered Architecture

This week's focus shifted to persistent storage and proper backend architecture, replacing the temporary, in-memory/local setup from Week 2.

**What I learned:**
- Setting up PostgreSQL as the primary database, run locally via Docker
- Using SQLAlchemy as the ORM layer to define models and relationships
- Designing relational tables (users, projects, tasks) with one-to-many relationships, including a join table for memberships using composite foreign keys
- Managing schema changes with Alembic migrations (generate, upgrade, downgrade, view history)
- Adding system health monitoring with MongoDB and Motor
- Breaking the project into clean architectural layers:
  - **Models** – table structure and relationships
  - **Schemas** – Pydantic validation for input/output
  - **Repository** – direct database communication
  - **Service** – business logic and validation before writes
  - **Routes** – FastAPI endpoints delegating to the service layer
- Managing dependencies with Poetry and running the app with Uvicorn
- Handling environment-based secrets safely (`.env`, `.env.example`, `.gitignore`)
- Understanding the practical value of persistence — data surviving server restarts — compared to the previous week's setup

---

## Week 4: AWS RDS, JWT Authentication & Authorization

This was the real backend project for the program, building directly on Week 3's PostgreSQL/Docker setup but replacing local hosting with a production-style cloud database and adding proper security.

**What I learned:**
- Connecting a FastAPI backend to a real AWS RDS instance instead of a local database
- Implementing JWT-based authentication for user login
- Hashing passwords on registration so plaintext credentials are never stored
- Implementing role-based authorization, restricting sensitive CRUD operations (on users, tasks, and projects) to admin accounts only
- Understanding the distinction between **authentication** (who you are) and **authorization/ownership** (what you're allowed to do)
- Using Swagger UI's "Authorize" button to test authenticated endpoints with a JWT access token
- Observing how unauthorized requests are handled and rejected by the API

**What I liked most:** Connecting to RDS in Week 4 with FastAPI was my favorite part, since that's the setup we're using mostly going forward anyway.

---


## Week 5: GraphQL as the Main Backend (Ariadne)

This week replaced the REST layer built in Week 4 with a GraphQL API, while keeping the existing authentication, hashing, and ownership logic completely intact underneath.

**What I learned:**
- Setting up Ariadne as a schema-first GraphQL library, where the `.graphql` file is the single source of truth for the API's shape, and Python only provides the resolvers that fulfill it
- Defining `type`, `input`, `Query`, and `Mutation` blocks in GraphQL's own SDL syntax, separate from any Python code
- Writing resolvers using `QueryType()` and `MutationType()` for top-level fields, and `ObjectType("TypeName")` for resolving individual fields on a specific type
- Building a request-scoped context object (`info.context`) that carries the current user, database session, and other shared resources into every resolver — the same concept as FastAPI's `Depends()`, built once per request instead of injected per-route
- Confirming that the existing `services/` and `repositories/` layers needed almost no changes — the same service functions were called from GraphQL resolvers exactly as they had been from REST routes
- Adding pagination (`limit`/`offset`) and filtering as optional arguments directly on GraphQL queries
- Implementing consistent admin-override logic so admin roles bypass ownership checks across all queries and mutations

**What I liked most:** Seeing the REST-to-GraphQL migration actually prove out the layered architecture from Week 3 — the service layer didn't care which protocol was calling it, which made the earlier investment in separating concerns feel concretely justified rather than just "good practice" on paper.

---

## Week 6: Redis Caching and ARQ Background Jobs

This week added a Redis cache in front of expensive read queries and an ARQ background worker to handle activity logging asynchronously, without blocking API responses.

**What I learned:**
- Implementing a cache-aside pattern: check Redis first on every read query, return immediately on a hit, query Postgres on a miss and store the result with a TTL before returning
- Structuring cache keys by user ID and query parameters (`tasks:{user_id}:list:{filters}`) so each user's data is isolated and can be invalidated independently
- Explicitly invalidating cache keys on every write mutation, rather than waiting for TTL expiry, so reads after a write always return fresh data
- Setting up ARQ as a background job queue backed by Redis — defining job functions, running the worker as a separate process, and understanding that `enqueue_job()` only writes a job description to Redis, while the worker executes it independently
- Understanding when background jobs are appropriate: activity logging is genuinely fire-and-forget (the API doesn't need the log written before responding), making it a correct fit for a queue rather than a synchronous call
- Adding a `redisHealth` GraphQL query that returns a clean error string rather than crashing the API when Redis is unreachable, demonstrating graceful degradation

**What I liked most:** Watching the worker terminal print confirmation of a logged job moments after a mutation returned — the full asynchronous pipeline (enqueue, respond, worker picks up, writes to DB) working end-to-end made background processing click as a concept rather than just theory.

---

## Week 7: Docker, MongoDB, and gRPC

This week containerized the full stack, gave MongoDB a real role in the system, and introduced gRPC to demonstrate strict-contract service-to-service communication alongside the existing GraphQL API.

**What I learned:**
- Writing a multi-stage `Dockerfile` so Poetry and build-time tooling don't end up in the final production image — only the installed packages are copied into the lean runtime stage
- Defining a full `docker-compose.yml` with six services (API, worker, PostgreSQL, Redis, MongoDB, and a dedicated test database) so the entire stack starts with one command
- Separating a production-shaped `docker-compose.yml` from a `docker-compose.override.yml` for development conveniences like live reload and source volume-mounting
- Understanding why containers use service names instead of `localhost` — each container's network namespace treats `localhost` as itself, so inter-container communication requires Docker Compose's internal DNS (`postgres`, `redis`, `mongo`)
- Giving MongoDB a real job: writing a denormalized copy of every activity log event alongside the authoritative Postgres record, using each database for what it's genuinely better at (Postgres for relational consistency, MongoDB for fast schema-less reads)
- Writing a `.proto` file as a strict contract for a `UserLookupService`, compiling it with `protoc` to generate Python message classes and service stubs, then implementing a real server and client that communicate over gRPC
- Thinking through microservice boundaries — recognizing that a boundary which looks clean on a diagram isn't always justified, and that the correct question is whether data and team responsibility genuinely diverge, not just whether domain nouns are separable
- Verifying deployability from a complete teardown: running `docker compose down -v` to wipe all containers and volumes, rebuilding from zero, re-running migrations, and confirming all 38 automated tests still pass

**What I liked most:** The deployability test — proving that a stranger following only the written README could get a fully working, fully tested backend from absolute zero, without needing to ask the original author anything. It was the first time "it works on my machine" became something demonstrably true on any machine.

---