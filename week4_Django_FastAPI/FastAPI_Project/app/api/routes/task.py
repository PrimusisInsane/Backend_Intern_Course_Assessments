from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.task_schema import TaskCreate
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_user
from app.services.task_service import create_task_service, list_tasks_service, update_task_service, delete_task_service, get_task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_task_service(db, task, current_user.id)

@router.get("/")
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_tasks_service(db, current_user.id)  

@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_task_service(db, task_id, current_user.id)  

@router.put("/{task_id}")
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_task_service(db, task_id, task, current_user.id) 

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_task_service(db, task_id, current_user.id) 
