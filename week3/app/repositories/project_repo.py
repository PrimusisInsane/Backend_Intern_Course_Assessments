from sqlalchemy.orm import Session
from app.models.project_model import Project

def create_project(db: Session, name: str, project_id: int):
    project = Project(name=name, id=project_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_projects(db: Session):
    return db.query(Project).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        return True
    return False


def update_project(db: Session, project_id: int, name: str = None):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    if name is not None:
        project.name = name
    db.commit()
    db.refresh(project)
    return project


