from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task_schema import TaskCreate
from app.services.task_service import create_task_service, list_tasks_service, update_task_service, delete_task_service, get_task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task_service(db, task)


@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    return list_tasks_service(db)

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_service(db, task_id)

@router.put("/{task_id}")
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    return update_task_service(db, task_id, task)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return delete_task_service(db, task_id)

