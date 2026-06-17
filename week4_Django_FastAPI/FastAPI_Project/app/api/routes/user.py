from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserCreate
from app.schemas.task_schema import TaskResponse
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_user
from app.services.user_service import (
    create_user_service, list_users_service, get_user_service,
    delete_user_service, update_user_service, get_user_by_id_service,
    get_user_tasks_service
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_user_service(db, user)

@router.get("/")
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_users_service(db)

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_by_id_service(db, user_id)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_user_service(db, user_id)

@router.put("/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_user_service(db, user_id, user)

@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
def get_user_tasks(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_tasks_service(db, user_id)