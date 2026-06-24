# How REST and GraphQL Share the Same Service Layer

This project's GraphQL API was built by replacing the REST route layer with GraphQL resolvers, while keeping every other layer untouched. This section explains why that worked and how the layers divide responsibility.

## The Architecture

```
REST version:
  routes/  →  services/  →  repositories/  →  models/  →  database

GraphQL version:
  resolvers/  →  services/  →  repositories/  →  models/  →  database
```

Only the top layer changed. `services/`, `repositories/`, and `models/` are identical in both versions — same files, same logic, same function signatures (give or take a few argument tweaks for things like `is_admin`).

## Why This Works

A **service function** doesn't know or care whether it was called from a FastAPI route handler or a GraphQL resolver. It just receives a database session and some plain arguments, and returns data:

```python
def get_task_service(db, task_id: int, user_id: int, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    return task
```

This same function is called from:

**A REST route** (FastAPI):
```python
@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    is_admin = current_user.role == "admin"
    return get_task_service(db, task_id, current_user.id, is_admin)
```

**A GraphQL resolver** (Ariadne):
```python
@query.field("task")
def resolve_task(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    is_admin = user.role == "admin"
    return get_task_service(db, id, user.id, is_admin)
```

Both routes do the exact same three things:
1. Identify who's asking (`current_user` / `info.context["user"]`)
2. Get a database session (`Depends(get_db)` / `info.context["db"]`)
3. Call the same service function with the same arguments

## What Changes Between REST and GraphQL

| Layer | REST | GraphQL |
|---|---|---|
| Entry point | Many routes (`/tasks/`, `/tasks/{id}`) | One endpoint (`/graphql`) |
| Auth injection | `Depends(get_current_user)` | Built once per request in `context.py`, read via `info.context["user"]` |
| Request shape | Defined by URL + HTTP method | Defined by the query/mutation the client writes |
| Response shape | Fixed by the endpoint | Chosen by the client per request |
| Ownership/role checks | Inside the service function | Inside the *same* service function |
| Business logic | `services/` | `services/` — unchanged |
| Database queries | `repositories/` | `repositories/` — unchanged |

## Why Keep Services Separate from Routes/Resolvers at All

If the ownership check, role check, or hashing logic lived inside the route or resolver itself, switching from REST to GraphQL would have meant rewriting all of it. Because that logic lives in `services/`, switching protocols only meant rewriting the thin entry-point layer — a much smaller and safer change.

This is the same principle as separating a car's engine from its dashboard: swapping the dashboard (REST → GraphQL) doesn't require rebuilding the engine (services/repositories/models).

## Practical Takeaway

When adding a new feature to this project, the question is never "REST or GraphQL?" — it's "where does this logic belong?"

- New business rule or validation → `services/`
- New database query → `repositories/`
- New way to expose it → `routes/` (REST) or `resolvers/` (GraphQL), whichever protocol is active

Both protocols are just different doors into the same house.