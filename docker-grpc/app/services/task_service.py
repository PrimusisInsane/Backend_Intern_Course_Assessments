from app.models.task_model import Task
from app.repositories.task_repo import create_task, get_task_by_id
from app.db.redis import cache_delete_pattern
from fastapi import HTTPException


async def create_task_service(db, title: str, project_id: int, user_id: int, redis_pool):
    task = create_task(db, title, project_id, user_id)
    await redis_pool.enqueue_job(
        "write_activity_log",
        user_id=user_id,
        action="created",
        task_id=task.id,
        detail=f"Task '{title}' created"
    )
    await cache_delete_pattern(f"tasks:{user_id}:list:*")
    return task


def list_tasks_service(db, user_id: int, is_admin: bool = False, limit=None, offset=None, done=None):
    if is_admin:
        query = db.query(Task)
    else:
        query = db.query(Task).filter(Task.user_id == user_id)
    if done is not None:
        query = query.filter(Task.done == done)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()


def get_task_service(db, task_id: int, user_id: int, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    return task


async def update_task_service(db, task_id: int, title: str, project_id: int, done: bool, user_id: int, redis_pool, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")

    if title is not None:
        task.title = title
        await redis_pool.enqueue_job(
            "write_activity_log", user_id=user_id, action="updated",
            task_id=task.id, detail=f"Title changed to '{title}'"
        )
    if project_id is not None:
        task.project_id = project_id
        await redis_pool.enqueue_job(
            "write_activity_log", user_id=user_id, action="updated",
            task_id=task.id, detail=f"Moved to project {project_id}"
        )
    if done is not None:
        task.done = done
        await redis_pool.enqueue_job(
            "write_activity_log", user_id=user_id, action="status_changed",
            task_id=task.id, detail=f"Marked done={done}"
        )

    db.commit()
    db.refresh(task)
    await cache_delete_pattern(f"tasks:{user_id}:list:*")
    return task


async def delete_task_service(db, task_id: int, user_id: int, redis_pool, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    title = task.title
    await redis_pool.enqueue_job(
        "write_activity_log", user_id=user_id, action="deleted",
        task_id=task.id, detail=f"Task '{title}' deleted"
    )
    db.delete(task)
    db.commit()
    await cache_delete_pattern(f"tasks:{user_id}:list:*")
    return True


def search_tasks_service(db, user_id: int, keyword: str, is_admin: bool = False):
    if is_admin:
        query = db.query(Task).filter(Task.title.ilike(f"%{keyword}%"))
    else:
        query = db.query(Task).filter(
            Task.user_id == user_id,
            Task.title.ilike(f"%{keyword}%")
        )
    return query.all()


async def change_task_status_service(db, task_id: int, done: bool, user_id: int, redis_pool, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    task.done = done
    await redis_pool.enqueue_job(
        "write_activity_log", user_id=user_id, action="status_changed",
        task_id=task.id, detail=f"Status changed to done={done}"
    )
    db.commit()
    db.refresh(task)
    await cache_delete_pattern(f"tasks:{user_id}:list:*")
    return task