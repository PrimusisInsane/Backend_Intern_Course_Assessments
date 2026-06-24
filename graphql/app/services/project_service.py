from fastapi import HTTPException
from app.repositories.project_repo import create_project, get_projects, get_project_by_id, delete_project, update_project
from app.repositories.activity_log_repo import create_log
from app.models.task_model import Task
from app.models.membership_model import Membership
from app.models.project_model import Project

def create_project_service(db, name: str, user_id: int):
    project = create_project(db, name)
    membership = Membership(user_id=user_id, project_id=project.id)
    db.add(membership)
    db.commit()
    create_log(db, user_id, "created", project_id=project.id, detail=f"Project '{name}' created")
    return project

def list_projects_service(db, user_id: int, is_admin: bool = False, limit=None, offset=None):
    if is_admin:
        query = db.query(Project)
    else:
        query = db.query(Project).join(Membership).filter(Membership.user_id == user_id)
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_project_service(db, project_id, user_id: int, is_admin : bool = False):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if is_admin:
        return project
    membership = db.query(Membership).filter(
        Membership.project_id == project_id,
        Membership.user_id == user_id
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not your project")
    return project

def update_project_service(db, project_id, name: str, user_id: int, is_admin: bool = False):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not is_admin:
        membership = db.query(Membership).filter(
            Membership.project_id == project_id,
            Membership.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(status_code=403, detail="Not your project")
    create_log(db, user_id, "updated", project_id=project_id, detail=f"Name changed to '{name}'")
    return update_project(db, project_id, name)


def delete_project_service(db, project_id, user_id: int, is_admin: bool = False):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if not is_admin:
        membership = db.query(Membership).filter(
            Membership.project_id == project_id,
            Membership.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(status_code=403, detail="Not your project")
    create_log(db, user_id, "deleted", project_id=project_id, detail=f"Project '{project.name}' deleted")
    return delete_project(db, project_id)


def get_project_tasks_service(db, project_id, user_id: int, is_admin: bool = False):
    if not is_admin:
        membership = db.query(Membership).filter(
            Membership.project_id == project_id,
            Membership.user_id == user_id
        ).first()
        if not membership:
            raise HTTPException(status_code=403, detail="Not your project")
    return db.query(Task).filter(Task.project_id == project_id).all()


def search_projects_service(db, user_id: int, keyword: str, is_admin: bool = False):
    if is_admin:
        query = db.query(Project).filter(Project.name.ilike(f"%{keyword}%"))
    else:
        query = db.query(Project).join(Membership).filter(
            Membership.user_id == user_id,
            Project.name.ilike(f"%{keyword}%")
        )
    return query.all()