import pytest
from fastapi import HTTPException

from app.models.membership_model import Membership
from app.repositories.project_repo import create_project
from app.repositories.task_repo import create_task
from app.services.auth_service import register_service
from app.services.project_service import get_project_service
from app.services.task_service import get_task_service, list_tasks_service


def test_user_can_get_their_own_task(db_session):
    user = register_service(
        db_session, name="Owner", email="owner@example.com", age=25, password="pass"
    )
    project = create_project(db_session, name="My Project")
    task = create_task(db_session, title="My Task", project_id=project.id, user_id=user.id)

    result = get_task_service(db_session, task_id=task.id, user_id=user.id)
    assert result.id == task.id


def test_user_cannot_get_another_users_task(db_session):
    owner = register_service(
        db_session, name="Owner", email="owner2@example.com", age=25, password="pass"
    )
    other = register_service(
        db_session, name="Other", email="other@example.com", age=25, password="pass"
    )
    project = create_project(db_session, name="Project")
    task = create_task(db_session, title="Secret Task", project_id=project.id, user_id=owner.id)

    with pytest.raises(HTTPException) as exc_info:
        get_task_service(db_session, task_id=task.id, user_id=other.id)
    assert exc_info.value.status_code == 403


def test_admin_can_get_any_task(db_session):
    owner = register_service(
        db_session, name="Owner", email="owner3@example.com", age=25, password="pass"
    )
    admin = register_service(
        db_session, name="Admin", email="admin@example.com", age=30, password="adminpass"
    )
    project = create_project(db_session, name="Project")
    task = create_task(db_session, title="Owner Task", project_id=project.id, user_id=owner.id)

    result = get_task_service(db_session, task_id=task.id, user_id=admin.id, is_admin=True)
    assert result.id == task.id


def test_list_tasks_only_returns_own_tasks(db_session):
    user_a = register_service(
        db_session, name="User A", email="usera@example.com", age=25, password="pass"
    )
    user_b = register_service(
        db_session, name="User B", email="userb@example.com", age=25, password="pass"
    )
    project = create_project(db_session, name="Shared Project")
    create_task(db_session, title="A's Task", project_id=project.id, user_id=user_a.id)
    create_task(db_session, title="B's Task", project_id=project.id, user_id=user_b.id)

    results = list_tasks_service(db_session, user_id=user_a.id)
    assert all(t.user_id == user_a.id for t in results)
    assert len(results) == 1


def test_admin_list_tasks_returns_all(db_session):
    user_a = register_service(
        db_session, name="User A2", email="usera2@example.com", age=25, password="pass"
    )
    user_b = register_service(
        db_session, name="User B2", email="userb2@example.com", age=25, password="pass"
    )
    project = create_project(db_session, name="Project")
    create_task(db_session, title="Task 1", project_id=project.id, user_id=user_a.id)
    create_task(db_session, title="Task 2", project_id=project.id, user_id=user_b.id)

    results = list_tasks_service(db_session, user_id=user_a.id, is_admin=True)
    user_ids = {t.user_id for t in results}
    assert user_a.id in user_ids
    assert user_b.id in user_ids


def test_user_can_access_project_with_membership(db_session):
    user = register_service(
        db_session, name="Member", email="member@example.com", age=25, password="pass"
    )
    project = create_project(db_session, name="My Project")
    db_session.add(Membership(user_id=user.id, project_id=project.id))
    db_session.commit()

    result = get_project_service(db_session, project_id=project.id, user_id=user.id)
    assert result.id == project.id


def test_user_cannot_access_project_without_membership(db_session):
    user = register_service(
        db_session, name="Non-member", email="nonmember@example.com", age=25, password="pass"
    )
    project = create_project(db_session, name="Restricted Project")

    with pytest.raises(HTTPException) as exc_info:
        get_project_service(db_session, project_id=project.id, user_id=user.id)
    assert exc_info.value.status_code == 403


def test_admin_can_access_project_without_membership(db_session):
    admin = register_service(
        db_session, name="Admin2", email="admin2@example.com", age=30, password="pass"
    )
    project = create_project(db_session, name="Any Project")

    result = get_project_service(db_session, project_id=project.id, user_id=admin.id, is_admin=True)
    assert result.id == project.id


def test_get_task_raises_404_for_missing_task(db_session):
    user = register_service(
        db_session, name="Ghost User", email="ghost@example.com", age=25, password="pass"
    )

    with pytest.raises(HTTPException) as exc_info:
        get_task_service(db_session, task_id=999999, user_id=user.id)
    assert exc_info.value.status_code == 404


def test_get_project_raises_404_for_missing_project(db_session):
    user = register_service(
        db_session, name="Ghost2", email="ghost2@example.com", age=25, password="pass"
    )

    with pytest.raises(HTTPException) as exc_info:
        get_project_service(db_session, project_id=999999, user_id=user.id)
    assert exc_info.value.status_code == 404
