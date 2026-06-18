from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project_schema import ProjectCreate
from app.schemas.task_schema import TaskResponse
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_user
from app.services.project_service import (
    create_project_service, list_projects_service, get_project_service,
    delete_project_service, update_project_service,
    get_project_tasks_service
)

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_project_service(db, project, current_user.id)

@router.get("/")
def get_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_projects_service(db, current_user.id)

@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_project_service(db, project_id, current_user.id)

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_project_service(db, project_id, current_user.id)

@router.put("/{project_id}")
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_project_service(db, project_id, project, current_user.id)

@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_project_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_project_tasks_service(db, project_id, current_user.id)