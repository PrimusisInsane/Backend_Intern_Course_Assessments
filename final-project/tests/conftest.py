from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402

os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "")

import pytest  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.db.database import Base  # noqa: E402

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create all tables once before the test session, drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Fresh session per test, rolled back afterward so tests never leak state."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_user(db_session):
    """A real registered user, ready to use in any test that needs one."""
    from app.services.auth_service import register_service

    user = register_service(
        db_session,
        name="Fixture User",
        email="fixture@example.com",
        age=30,
        password="fixturepass123",
    )
    return user


@pytest.fixture
def test_user_token(test_user):
    """A valid JWT for the fixture user, for tests needing an authenticated request."""
    from app.db.security import create_access_token

    return create_access_token({"sub": str(test_user.id), "role": test_user.role})
