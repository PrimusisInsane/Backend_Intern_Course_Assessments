from ariadne import QueryType, ObjectType
from app.services.user_service import list_users_service, get_user_by_id_service
from app.services.project_service import (
    list_projects_service, get_project_service, get_project_tasks_service,
    search_projects_service
)
from app.services.task_service import (
    list_tasks_service, get_task_service, search_tasks_service
)
from app.repositories.activity_log_repo import get_logs_for_task, get_logs_for_project
from app.db.redis import cache_get, cache_set, redis_client


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
    is_admin = user.role == "admin"
    if not is_admin and user.id != id:
        raise Exception("Not your profile")
    return get_user_by_id_service(db, id)


@query.field("projects")
async def resolve_projects(_, info, limit=None, offset=None):
    user = info.context["user"]
    db = info.context["db"]
    cache = info.context["cache"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"

    cache_key = f"projects:{user.id}:list:{limit}:{offset}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    result = list_projects_service(db, user.id, is_admin, limit, offset)
    serialized = [{"id": p.id, "name": p.name} for p in result]
    await cache_set(cache_key, serialized, ttl=60)
    return serialized



@query.field("project")
def resolve_project(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return get_project_service(db, id, user.id, is_admin)


@query.field("getProjectById")
def resolve_get_project_by_id(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return get_project_service(db, id, user.id, is_admin)


@query.field("searchProjects")
def resolve_search_projects(_, info, keyword):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return search_projects_service(db, user.id, keyword, is_admin)


@query.field("projectTasks")
def resolve_project_tasks(_, info, projectId):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return get_project_tasks_service(db, projectId, user.id, is_admin)


@query.field("projectLogs")
def resolve_project_logs(_, info, projectId):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return get_logs_for_project(db, projectId)


@query.field("tasks")
async def resolve_tasks(_, info, limit=None, offset=None, done=None):
    user = info.context["user"]
    db = info.context["db"]
    cache = info.context["cache"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"

    cache_key = f"tasks:{user.id}:list:{limit}:{offset}:{done}"
    cached = await cache_get(cache_key)
    if cached is not None:
        return cached

    result = list_tasks_service(db, user.id, is_admin, limit, offset, done)
    serialized = [
        {"id": t.id, "title": t.title, "done": t.done, "userId": t.user_id, "projectId": t.project_id}
        for t in result
    ]
    await cache_set(cache_key, serialized, ttl=60)
    return serialized


@query.field("task")
def resolve_task(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return get_task_service(db, id, user.id, is_admin)


@query.field("getTaskById")
def resolve_get_task_by_id(_, info, id):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return get_task_service(db, id, user.id, is_admin)


@query.field("searchTasks")
def resolve_search_tasks(_, info, keyword):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    is_admin = user.role == "admin"
    return search_tasks_service(db, user.id, keyword, is_admin)


@query.field("taskLogs")
def resolve_task_logs(_, info, taskId):
    user = info.context["user"]
    db = info.context["db"]
    if not user:
        raise Exception("Not authenticated")
    return get_logs_for_task(db, taskId)


task_type = ObjectType("Task")

@task_type.field("userId")
def resolve_task_user_id(task, info):
    return task.user_id

@task_type.field("projectId")
def resolve_task_project_id(task, info):
    return task.project_id


activity_log_type = ObjectType("ActivityLog")

@activity_log_type.field("userId")
def resolve_log_user_id(log, info):
    return log.user_id

@activity_log_type.field("taskId")
def resolve_log_task_id(log, info):
    return log.task_id

@activity_log_type.field("createdAt")
def resolve_log_created_at(log, info):
    return log.created_at.isoformat()


@query.field("redisHealth")
async def resolve_redis_health(_, info):
    try:
        pong = await redis_client.ping()
        if pong:
            return "ok"
        return "fail"
    except Exception as e:
        return f"fail: {str(e)}"

