from app.models.task_model import Task
from app.repositories.task_repo import create_task, get_tasks , update_task, delete_task

def create_task_service(db, data):
    return create_task(db, data.title, data.project_id, data.user_id)

def list_tasks_service(db):
    return db.query(Task).all()

def get_task_service(db, task_id):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_service(db, task_id, data):
    return update_task(db, task_id, data.title, data.project_id, data.user_id)

def delete_task_service(db, task_id):
    return delete_task(db, task_id)


