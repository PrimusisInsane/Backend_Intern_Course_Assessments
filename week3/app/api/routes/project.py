from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project_schema import ProjectCreate
from app.schemas.task_schema import TaskResponse
from app.services.project_service import (
    create_project_service, list_projects_service, get_project_service,
    delete_project_service, update_project_service,
    get_project_tasks_service  
)

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return create_project_service(db, project)

@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return list_projects_service(db)

@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    return get_project_service(db, project_id)

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    return delete_project_service(db, project_id)

@router.put("/{project_id}")
def update_project(project_id: int, project: ProjectCreate, db: Session = Depends(get_db)):
    return update_project_service(db, project_id, project)

@router.get("/{project_id}/tasks", response_model=list[TaskResponse])  
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    return get_project_tasks_service(db, project_id)