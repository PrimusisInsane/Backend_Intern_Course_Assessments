from app.models.task_model import Task
from app.repositories.task_repo import create_task, get_task_by_id 
from fastapi import HTTPException


def create_task_service(db, data, user_id: int):
    return create_task(db, data.title, data.project_id, user_id)

def list_tasks_service(db, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task_service(db, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id)  
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    return task

def update_task_service(db, task_id: int, data, user_id: int):
    task = get_task_by_id(db, task_id)  
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your task")
    if data.title is not None:
        task.title = data.title
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