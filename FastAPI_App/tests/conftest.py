"""
conftest.py — Fixtures partagées pour les tests backend.
Utilise une base SQLite en mémoire pour isoler chaque test.
"""
import os
# Force une variable d'environnement pour éviter que config.py ne tente de se connecter à PostgreSQL
os.environ["DATABASE_APP_URL"] = "sqlite:///:memory:"

import pytest
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
# Import models here to ensure they are registered with Base.metadata
from app.models.user import User, PredictionHistory, UserFavoriteTeam

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Activer les clés étrangères dans SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Crée les tables avant chaque test et les supprime après."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Client HTTP de test avec override de la dépendance DB."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Helpers ──────────────────────────────────────────────────
@pytest.fixture
def registered_user(client):
    """Crée un utilisateur de test et retourne ses données."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "Pass1234"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return user_data


@pytest.fixture
def auth_headers(client, registered_user):
    """Retourne les headers d'authentification pour l'utilisateur de test."""
    login_resp = client.post("/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
