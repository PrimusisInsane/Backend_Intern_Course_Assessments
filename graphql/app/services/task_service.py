from app.models.task_model import Task
from app.repositories.task_repo import create_task, get_task_by_id
from fastapi import HTTPException


def create_task_service(db, title: str, project_id: int, user_id: int):
    return create_task(db, title, project_id, user_id)

def list_tasks_service(db, user_id: int, limit = None, offset= None, done = None):
    query =  db.query(Task).filter(Task.user_id == user_id)
    if done is not None:
        query = query.filter(Task.done == done)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_task_service(db, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    return task

def update_task_service(db, task_id: int, title: str, project_id: int, done: bool, user_id: int):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    if title is not None:
        task.title = title
    if project_id is not None:
        task.project_id = project_id
    if done is not None:
        task.done = done
    db.commit()
    db.refresh(task)
    return task

def delete_task_service(db, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    db.delete(task)
    db.commit()
    return True