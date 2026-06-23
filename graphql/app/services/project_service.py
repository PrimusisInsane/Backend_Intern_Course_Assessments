from fastapi import HTTPException
from app.repositories.project_repo import create_project, get_projects, get_project_by_id, delete_project, update_project
from app.models.task_model import Task
from app.models.membership_model import Membership
from app.models.project_model import Project

def create_project_service(db, name: str, user_id: int):
    project = create_project(db, name)
    membership = Membership(user_id=user_id, project_id=project.id)
    db.add(membership)
    db.commit()
    return project

def list_projects_service(db, user_id: int, limit=None, offset=None):
    query = db.query(Project).join(Membership).filter(Membership.user_id == user_id)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_project_service(db, project_id, user_id: int):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    membership = db.query(Membership).filter(
        Membership.project_id == project_id,
        Membership.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not your project")
    return project

def delete_project_service(db, project_id, user_id: int):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    membership = db.query(Membership).filter(
        Membership.project_id == project_id,
        Membership.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not your project")
    return delete_project(db, project_id)

def update_project_service(db, project_id, name: str, user_id: int):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    membership = db.query(Membership).filter(
        Membership.project_id == project_id,
        Membership.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not your project")
    return update_project(db, project_id, name)

def get_project_tasks_service(db, project_id, user_id: int):
    membership = db.query(Membership).filter(
        Membership.project_id == project_id,
        Membership.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not your project")
    return db.query(Task).filter(Task.project_id == project_id).all()