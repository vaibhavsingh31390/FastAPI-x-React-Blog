from collections.abc import Generator
import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config.main_db import Base, get_db
from main import app as main_app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, None, None]:
    """Create a fresh schema for each test function."""
    Base.metadata.create_all(bind=engine)
    yield main_app
    main_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[Session, None, None]:
    """Provide a database session wrapped in a rollback transaction."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, None, None]:
    """Create a TestClient that uses the test database instead of the real one."""

    def _get_test_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as test_client:
        yield test_client
