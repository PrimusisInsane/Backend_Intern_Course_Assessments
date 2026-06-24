from app.models.task_model import Task
from app.repositories.task_repo import create_task, get_task_by_id
from app.repositories.activity_log_repo import create_log
from fastapi import HTTPException


def create_task_service(db, title: str, project_id: int, user_id: int):
    task = create_task(db, title, project_id, user_id)
    create_log(db, user_id, "created", task_id=task.id, detail=f"Task '{title}' created")
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


def update_task_service(db, task_id: int, title: str, project_id: int, done: bool, user_id: int, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")

    if title is not None:
        task.title = title
        create_log(db, user_id, "updated", task_id=task.id, detail=f"Title changed to '{title}'")
    if project_id is not None:
        task.project_id = project_id
        create_log(db, user_id, "updated", task_id=task.id, detail=f"Moved to project {project_id}")
    if done is not None:
        task.done = done
        create_log(db, user_id, "status_changed", task_id=task.id, detail=f"Marked done={done}")

    db.commit()
    db.refresh(task)
    return task


def delete_task_service(db, task_id: int, user_id: int, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    create_log(db, user_id, "deleted", task_id=task.id, detail=f"Task '{task.title}' deleted")
    db.delete(task)
    db.commit()
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


def change_task_status_service(db, task_id: int, done: bool, user_id: int, is_admin: bool = False):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not is_admin and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    task.done = done
    create_log(db, user_id, "status_changed", task_id=task.id, detail=f"Status changed to done={done}")
    db.commit()
    db.refresh(task)
    return task