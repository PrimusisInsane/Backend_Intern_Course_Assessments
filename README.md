# Internship of Backend Repository

## Completed Course action 
* Week 1 - Fundamentals of Python
* Week 2 - FastAPI and Starlette
* Week 3 - Databases(Postgres/MongoDB) & Alembic
* Week 4 - Django Reference and FastAPI main backend



# Backend Internship — Learning Report (Weeks 1–4)

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

## Overall Progression

Across the four weeks, the work moved from Python basics with a local SQLite database, to building structured REST APIs with FastAPI, to persistent PostgreSQL storage with a proper layered architecture, and finally to a cloud-hosted, authenticated, and authorized backend on AWS RDS closely mirroring how a real-world production backend is built up in stages. I think that's what I actually liked the most. It resembles actual backend work.


## Office environment

- The office environment has been pretty cozy and comfortable overall. Having a clear, structured assessment outline each week made it a lot easier to focus on actual work instead of being unsure what to do next each week built on the last in a way that made sense and kept things from feeling scattered. Communication with other interns has been good too I've specifically been talking with two DevOps interns about what they've been learning on their end, which has been a nice way to pick up context outside of just the backend track. Overall it's been a good setup for actually getting into the work and learning at a steady pace.