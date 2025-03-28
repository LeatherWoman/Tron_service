import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.utils.database import Base, get_db

# Устанавливаем тестовое окружение
os.environ["ENV"] = "TEST"

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Фикстура для создания и удаления тестовой базы данных."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db() -> Generator[Session, None, None]:
    """Переопределение зависимости базы данных для тестов."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client(setup_db) -> TestClient:
    """Фикстура для тестового клиента FastAPI."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def db_session(setup_db) -> Generator[Session, None, None]:
    """Фикстура для тестовой сессии базы данных."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()