from sqlalchemy.orm import Session

from app.models.activity_log_model import ActivityLog


def create_log(
    db: Session,
    user_id: int,
    action: str,
    task_id: int = None,
    project_id: int = None,
    detail: str = None,
):
    log = ActivityLog(
        user_id=user_id, task_id=task_id, project_id=project_id, action=action, detail=detail
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_logs_for_task(db: Session, task_id: int):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.task_id == task_id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def get_logs_for_project(db: Session, project_id: int):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.project_id == project_id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )
