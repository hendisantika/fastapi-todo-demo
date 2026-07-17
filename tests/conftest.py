"""Shared pytest fixtures.

The application talks to MySQL in production, but CI has no MySQL server.
We point the app at an in-memory SQLite database *before* importing it, then
override the ``get_db`` dependency so every test runs against an isolated,
fresh schema. This keeps the tests fast and free of external services.
"""
import os

# Must be set before `database`/`main` are imported: database.py reads DB_URL at
# import time and main.py calls create_all() against that engine on import.
os.environ.setdefault("DB_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from main import app, get_db

# A single shared in-memory SQLite connection (StaticPool) so the schema created
# in the fixture is visible to the request handlers.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
