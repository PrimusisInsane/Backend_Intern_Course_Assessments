from ariadne import QueryType
from app.services.user_service import list_users_service, get_user_by_id_service
from app.services.project_service import list_projects_service, get_project_service, get_project_tasks_service
from app.services.task_service import list_tasks_service, get_task_service

query = QueryType()


@query.field("me")
def resolve_me(_, info):
    user = info.context["user"]
    if not user:
        raise Exception("Not authenticated")
    return user


@query.field("users")
def resolve_users(_, info):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    if user.role != "admin":
        raise Exception("Admin access required")
    return list_users_service(db)
    


@query.field("user")
def resolve_user(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    if user.id != id:
        raise Exception("Not your profile")
    return get_user_by_id_service(db, id)


@query.field("projects")
def resolve_projects(_, info, limit=None, offset=None):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return list_projects_service(db, user.id, limit, offset)

@query.field("projectTasks")
def resolve_project_tasks(_, info, projectId):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return get_project_tasks_service(db, projectId, user.id)


@query.field("tasks")
def resolve_tasks(_, info, limit=None, offset=None, done=None):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return list_tasks_service(db, user.id, limit, offset, done)


@query.field("task")
def resolve_task(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return get_task_service(db, id, user.id)

from ariadne import ObjectType

task_type = ObjectType("Task")

@task_type.field("userId")
def resolve_task_user_id(task, info):
    return task.user_id

@task_type.field("projectId")
def resolve_task_project_id(task, info):
    return task.project_id