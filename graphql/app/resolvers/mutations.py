from ariadne import MutationType
from app.services.auth_service import register_service, login_service
from app.services.project_service import create_project_service, update_project_service, delete_project_service
from app.services.task_service import create_task_service, update_task_service, delete_task_service
from app.db.security import create_access_token

mutation = MutationType()


@mutation.field("register")
def resolve_register(_, info, input):
    db = info.context["db"]
    user = register_service(db, input["name"], input["email"], input["age"], input["password"])
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"accessToken": token, "tokenType": "bearer"}


@mutation.field("login")
def resolve_login(_, info, input):
    db = info.context["db"]
    result = login_service(db, input["email"], input["password"])
    return {"accessToken": result["access_token"], "tokenType": result["token_type"]}


@mutation.field("createProject")
def resolve_create_project(_, info, input):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return create_project_service(db, input["name"], user.id)


@mutation.field("updateProject")
def resolve_update_project(_, info, id, input):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return update_project_service(db, id, input.get("name"), user.id)


@mutation.field("deleteProject")
def resolve_delete_project(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return delete_project_service(db, id, user.id)


@mutation.field("createTask")
def resolve_create_task(_, info, input):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return create_task_service(db, input["title"], input["projectId"], user.id)


@mutation.field("updateTask")
def resolve_update_task(_, info, id, input):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return update_task_service(db, id, input.get("title"), input.get("projectId"), user.id)


@mutation.field("deleteTask")
def resolve_delete_task(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return delete_task_service(db, id, user.id)