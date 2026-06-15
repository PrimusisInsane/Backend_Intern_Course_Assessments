from sqlalchemy.orm import Session
from app.models.task_model import Task

def create_task(db: Session, title: str, project_id: int, user_id: int):
    task = Task(
        title=title,
        project_id=project_id,
        user_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session):
    return db.query(Task).all()


def update_task(db: Session, task_id: int, title: str = None, project_id: int = None, user_id: int = None):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    if title is not None:
        task.title = title
    if project_id is not None:
        task.project_id = project_id
    if user_id is not None:
        task.user_id = user_id
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

