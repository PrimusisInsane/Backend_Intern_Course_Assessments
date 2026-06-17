# FastAPI Project Structure — With Auth

```
app/
├── main.py                          ← MODIFIED (add auth router)
│
├── core/
│   ├── database.py                  ← untouched
│   └── security.py                  ← NEW (password hashing + JWT utils)
│
├── models/
│   ├── user_model.py                ← MODIFIED (add password, role fields)
│   ├── project_model.py             ← untouched
│   ├── task_model.py                ← untouched
│   └── membership_model.py          ← untouched
│
├── schemas/
│   ├── auth_schema.py               ← NEW (login request/response)
│   ├── user_schema.py               ← MODIFIED (add password field)
│   ├── task_schema.py               ← untouched
│   └── project_schema.py            ← untouched
│
├── repositories/
│   ├── user_repo.py                 ← MODIFIED (add get_user_by_email)
│   ├── task_repo.py                 ← untouched
│   └── project_repo.py              ← untouched
│
├── services/
│   ├── auth_service.py              ← NEW (register + login logic)
│   ├── user_service.py              ← untouched
│   ├── task_service.py              ← untouched
│   └── project_service.py           ← untouched
│
├── api/
│   └── routes/
│       ├── auth.py                  ← NEW (register + login endpoints)
│       ├── user.py                  ← MODIFIED (protect routes)
│       ├── task.py                  ← MODIFIED (protect routes)
│       ├── project.py               ← MODIFIED (protect routes)
│       └── health.py                ← untouched
│
└── dependencies/
    └── auth_dependency.py           ← NEW (get_current_user)
```

## Summary

### New files (5)
- core/security.py
- schemas/auth_schema.py
- services/auth_service.py
- api/routes/auth.py
- dependencies/auth_dependency.py

### Modified files (5)
- main.py
- models/user_model.py
- schemas/user_schema.py
- repositories/user_repo.py
- api/routes/user.py, task.py, project.py

### Untouched files
- Everything else