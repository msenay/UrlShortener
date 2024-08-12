import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.database.session import get_db

# Create an SQLite engine for the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def mock_redis(mocker):
    redis_mock = mocker.patch("app.cache.url_shortener.store")
    redis_mock.get.return_value = None
    redis_mock.setex.return_value = True
    return redis_mock


# Database session fixture
@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new database session for each test function.

    This fixture creates the database tables before the test starts and drops them after the test ends.

    Yields:
        Session: A SQLAlchemy session.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# FastAPI TestClient fixture
@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides a TestClient instance for the FastAPI application.

    This fixture overrides the application's database dependency to use the test session.

    Args:
        db_session (Session): The SQLAlchemy session provided by the db_session fixture.

    Yields:
        TestClient: A TestClient instance for testing.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# Example URL fixture
@pytest.fixture
def example_url():
    """
    Provides a sample URL for use in tests.

    Yields:
        dict: A dictionary containing an example original URL.
    """
    return {"original_url": "https://www.example.com"}
