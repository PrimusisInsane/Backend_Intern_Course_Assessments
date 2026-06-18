# Django vs FastAPI — Week 4 Comparison

Built both this week. Here's what each one actually gave me.

---

## The one-liner

> **Django: batteries included. FastAPI: bring your own batteries.**

---

## Feature by feature

### Auth setup
- **Django + DRF** — install `djangorestframework-simplejwt`, add two URLs, done. JWT login and refresh just work out of the box.
- **FastAPI** — install `pyjwt`, write `create_access_token()`, write `decode_access_token()`, write the `HTTPBearer` dependency, wire it into every route manually. You understand exactly what's happening because you wrote it.

### Password hashing
- **Django** — completely automatic. Call `User.objects.create_user()` and Django hashes the password using pbkdf2_sha256 with 1.2 million iterations and a random salt. You never think about it.
- **FastAPI** — install `passlib[bcrypt]`, create a `CryptContext`, write `hash_password()` and `verify_password()` yourself, call them explicitly in your auth service.

### ORM
- **Django** — built in. Define a model, run migrations, query with `Task.objects.filter(owner=user)`. No setup.
- **FastAPI** — SQLAlchemy is a separate package. Query syntax is `db.query(Task).filter(Task.user_id == user_id).first()`. More verbose but more explicit.

### Migrations
- **Django** — `python manage.py makemigrations` + `python manage.py migrate`. That's it.
- **FastAPI** — Alembic is a separate tool. `alembic revision --autogenerate -m "message"` + `alembic upgrade head`. Requires configuring `env.py` to point at your models and database URL.

### Admin panel
- **Django** — automatic at `/admin/`. Register your model with one line and get a full CRUD UI with search, filters, and user management for free.
- **FastAPI** — nothing. You build your own admin routes or use a third-party package.

### API docs
- **Django + DRF** — browsable API at the route URL, HTML only, basic.
- **FastAPI** — Swagger UI auto-generated at `/docs`, ReDoc at `/redoc`. Interactive — you can test endpoints directly from the browser. The Authorize button appears automatically once you add security dependencies to routes.

### Ownership rules
- **Django + DRF** — override `get_queryset()` in a ViewSet to filter by the current user. Clean and built into the framework pattern.
- **FastAPI** — manual check in the service layer: `if task.user_id != current_user.id: raise HTTPException(403)`. More explicit, fully in your control.

### Role-based auth
- **Django + DRF** — `IsAdminUser` permission class is built in. Apply it to any view.
- **FastAPI** — write a `get_admin_user` dependency that checks `current_user.role != "admin"` and raises 403. Reusable across any route.

### Project structure
- **Django** — opinionated. One way to do things: `models.py`, `views.py`, `urls.py`, `admin.py` per app. Familiarity across all Django projects.
- **FastAPI** — completely flexible. Built this structure: `models/`, `schemas/`, `repositories/`, `services/`, `routes/`, `dependencies/`, `core/`. Separation of concerns is explicit and your responsibility.

---

## What this week proved

Starting with Django first was the right call. When building the FastAPI auth system:
- Already understood JWT flow from DRF — just translated it
- Already understood password hashing — just did it manually with passlib
- Already understood ownership rules — just wrote the check explicitly instead of using a ViewSet method
- Already understood migrations — just used Alembic instead of Django's built-in tool

Django teaches you *what* needs to happen. FastAPI makes you write *how* it happens.

---

## When to use which

| Situation | Use |
|---|---|
| Need admin panel fast | Django |
| Building a pure API | FastAPI |
| Quick MVP with auth | Django |
| Microservices | FastAPI |
| Full-stack with templates | Django |
| High-performance async API | FastAPI |
| Team already knows Django | Django + DRF |
| Need auto Swagger docs | FastAPI |

---

## Stack used this week

**Django project**
- Django 6.0
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL on AWS RDS

**FastAPI project**
- FastAPI
- SQLAlchemy ORM
- Alembic migrations
- pyjwt
- passlib[bcrypt]
- PostgreSQL on AWS RDS
- Poetry for dependency management