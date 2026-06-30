import pytest
from fastapi import HTTPException

from app.db.security import hash_password, verify_password
from app.services.auth_service import login_service, register_service


def test_password_hash_is_not_plaintext():
    raw_password = "mysecretpassword"
    hashed = hash_password(raw_password)
    assert hashed != raw_password
    assert hashed.startswith("$2b$")


def test_password_verification_succeeds_with_correct_password():
    raw_password = "correcthorsebatterystaple"
    hashed = hash_password(raw_password)
    assert verify_password(raw_password, hashed) is True


def test_password_verification_fails_with_wrong_password():
    hashed = hash_password("therightpassword")
    assert verify_password("thewrongpassword", hashed) is False


def test_register_creates_a_user_with_hashed_password(db_session):
    user = register_service(
        db_session, name="Test User", email="testuser@example.com", age=25, password="plaintext123"
    )
    assert user.id is not None
    assert user.password != "plaintext123"
    assert user.role == "member"


def test_register_rejects_duplicate_email(db_session):
    register_service(db_session, name="First", email="dupe@example.com", age=30, password="pass1")
    with pytest.raises(HTTPException) as exc_info:
        register_service(
            db_session, name="Second", email="dupe@example.com", age=31, password="pass2"
        )
    assert exc_info.value.status_code == 400


def test_login_succeeds_with_correct_credentials(db_session):
    register_service(
        db_session, name="Login Test", email="login@example.com", age=28, password="rightpassword"
    )
    result = login_service(db_session, email="login@example.com", password="rightpassword")
    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_fails_with_wrong_password(db_session):
    register_service(
        db_session,
        name="Login Test 2",
        email="login2@example.com",
        age=28,
        password="rightpassword",
    )
    with pytest.raises(HTTPException) as exc_info:
        login_service(db_session, email="login2@example.com", password="wrongpassword")
    assert exc_info.value.status_code == 401


def test_login_fails_for_nonexistent_user(db_session):
    with pytest.raises(HTTPException) as exc_info:
        login_service(db_session, email="ghost@example.com", password="anything")
    assert exc_info.value.status_code == 401
