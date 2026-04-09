import pytest
from fastapi import status

def test_register_user(client):
    """Teste l'inscription d'un nouvel utilisateur."""
    payload = {
        "username": "newtester",
        "email": "newtester@example.com",
        "password": "Password123"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert "id" in data

def test_register_duplicate_email(client, registered_user):
    """Teste qu'on ne peut pas s'inscrire avec un email déjà existant."""
    # registered_user a déjà fait un post sur /auth/register
    response = client.post("/auth/register", json=registered_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "déjà utilisé" in response.json()["detail"].lower()

def test_login_success(client, registered_user):
    """Teste la connexion avec des identifiants valides."""
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client, registered_user):
    """Teste l'échec de connexion avec de mauvais identifiants."""
    payload = {
        "email": registered_user["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_me_success(client, auth_headers, registered_user):
    """Teste la récupération du profil de l'utilisateur connecté."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == registered_user["email"]
    assert data["username"] == registered_user["username"]

def test_get_me_unauthorized(client):
    """Teste l'accès au profil sans token."""
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
