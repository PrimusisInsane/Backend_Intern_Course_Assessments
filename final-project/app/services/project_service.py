from fastapi import HTTPException

from app.db.redis import cache_delete_pattern
from app.models.membership_model import Membership
from app.models.project_model import Project
from app.models.task_model import Task
from app.repositories.project_repo import (
    create_project,
    delete_project,
    get_project_by_id,
    update_project,
)


async def create_project_service(db, name: str, user_id: int, redis_pool):
    project = create_project(db, name)
    membership = Membership(user_id=user_id, project_id=project.id)
    db.add(membership)
    db.commit()
    await redis_pool.enqueue_job(
        "write_activity_log",
        user_id=user_id,
        action="created",
        project_id=project.id,
        detail=f"Project '{name}' created",
    )
    await cache_delete_pattern(f"projects:{user_id}:list:*")
    return project


def list_projects_service(db, user_id: int, is_admin: bool = False, limit=None, offset=None):
    if is_admin:
        query = db.query(Project)
    else:
        query = db.query(Project).join(Membership).filter(Membership.user_id == user_id)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()


def get_project_service(db, project_id, user_id: int, is_admin: bool = False):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if is_admin:
        return project
    membership = (
        db.query(Membership)
        .filter(Membership.project_id == project_id, Membership.user_id == user_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Not your project")
    return project


async def delete_project_service(db, project_id, user_id: int, redis_pool, is_admin: bool = False):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not is_admin:
        membership = (
            db.query(Membership)
            .filter(Membership.project_id == project_id, Membership.user_id == user_id)
            .first()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Not your project")
    name = project.name
    await redis_pool.enqueue_job(
        "write_activity_log",
        user_id=user_id,
        action="deleted",
        project_id=project_id,
        detail=f"Project '{name}' deleted",
    )
    result = delete_project(db, project_id)
    await cache_delete_pattern(f"projects:{user_id}:list:*")
    return result


async def update_project_service(
    db, project_id, name: str, user_id: int, redis_pool, is_admin: bool = False
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not is_admin:
        membership = (
            db.query(Membership)
            .filter(Membership.project_id == project_id, Membership.user_id == user_id)
            .first()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Not your project")
    await redis_pool.enqueue_job(
        "write_activity_log",
        user_id=user_id,
        action="updated",
        project_id=project_id,
        detail=f"Name changed to '{name}'",
    )
    result = update_project(db, project_id, name)
    await cache_delete_pattern(f"projects:{user_id}:list:*")
    return result


def get_project_tasks_service(db, project_id, user_id: int, is_admin: bool = False):
    if not is_admin:
        membership = (
            db.query(Membership)
            .filter(Membership.project_id == project_id, Membership.user_id == user_id)
            .first()
        )
        if not membership:
            raise HTTPException(status_code=403, detail="Not your project")
    return db.query(Task).filter(Task.project_id == project_id).all()


def search_projects_service(db, user_id: int, keyword: str, is_admin: bool = False):
    if is_admin:
        query = db.query(Project).filter(Project.name.ilike(f"%{keyword}%"))
    else:
        query = (
            db.query(Project)
            .join(Membership)
            .filter(Membership.user_id == user_id, Project.name.ilike(f"%{keyword}%"))
        )
    return query.all()
