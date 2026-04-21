"""
Tests FONCTIONNELS — Routes /auth/*
Vérifient le comportement de l'API via le TestClient HTTP (status codes, JSON, auth).
"""
from fastapi import status


# ── Inscription ──────────────────────────────────────────────
class TestRegisterRoute:
    def test_register_success(self, client):
        resp = client.post("/auth/register", json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "Pass1234"
        })
        assert resp.status_code == status.HTTP_201_CREATED
        body = resp.json()
        assert body["username"] == "newuser"
        assert body["email"] == "new@test.com"
        assert "id" in body

    def test_register_duplicate_email(self, client, registered_user):
        resp = client.post("/auth/register", json={
            "username": "other",
            "email": registered_user["email"],  # déjà pris
            "password": "Pass1234"
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ── Login ────────────────────────────────────────────────────
class TestLoginRoute:
    def test_login_success(self, client, registered_user):
        resp = client.post("/auth/login", json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_wrong_password(self, client, registered_user):
        resp = client.post("/auth/login", json={
            "email": registered_user["email"],
            "password": "WrongPwd"
        })
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED


# ── Profil (GET / PUT / DELETE /auth/me) ─────────────────────
class TestProfileRoutes:
    def test_get_me(self, client, auth_headers):
        resp = client.get("/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["username"] == "testuser"
        assert body["email"] == "test@example.com"

    def test_get_me_unauthorized(self, client):
        resp = client.get("/auth/me")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, client, auth_headers):
        resp = client.put("/auth/me", headers=auth_headers, json={
            "username": "updated_name"
        })
        assert resp.status_code == 200
        assert resp.json()["username"] == "updated_name"

    def test_delete_account(self, client, auth_headers):
        resp = client.delete("/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["message"] == "Compte supprimé"
        # Vérifier que le compte est bien supprimé
        resp2 = client.get("/auth/me", headers=auth_headers)
        assert resp2.status_code == status.HTTP_401_UNAUTHORIZED


# ── Statistiques et Favoris ──────────────────────────────────
class TestStatsFavoritesRoutes:
    def test_get_stats(self, client, auth_headers):
        resp = client.get("/auth/me/stats", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "total_predictions" in body
        assert "favorite_teams_count" in body

    def test_add_favorite(self, client, auth_headers):
        resp = client.post("/auth/me/favorites", headers=auth_headers, json={
            "team_id": 1
        })
        assert resp.status_code == 200
        assert resp.json()["team_id"] == 1

    def test_get_favorites(self, client, auth_headers):
        # Add one first
        client.post("/auth/me/favorites", headers=auth_headers, json={"team_id": 2})
        
        resp = client.get("/auth/me/favorites", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_remove_favorite(self, client, auth_headers):
        # Add
        client.post("/auth/me/favorites", headers=auth_headers, json={"team_id": 3})
        # Remove
        resp = client.delete("/auth/me/favorites/3", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["message"] == "Favori supprimé"


# ── Changement de mot de passe ───────────────────────────────
class TestChangePasswordRoute:
    def test_change_password_success(self, client, registered_user, auth_headers):
        resp = client.post("/auth/change-password", headers=auth_headers, json={
            "old_password": registered_user["password"],
            "new_password": "NewPass99"
        })
        assert resp.status_code == 200

    def test_change_password_wrong_old(self, client, auth_headers):
        resp = client.post("/auth/change-password", headers=auth_headers, json={
            "old_password": "WrongOld",
            "new_password": "NewPass99"
        })
        assert resp.status_code == 400


# ── Forgot Password ─────────────────────────────────────────
class TestForgotPasswordRoute:
    def test_forgot_password_existing_email(self, client, registered_user):
        resp = client.post("/auth/forgot-password", json={
            "email": registered_user["email"]
        })
        assert resp.status_code == 200
        assert "message" in resp.json()

    def test_forgot_password_unknown_email(self, client):
        resp = client.post("/auth/forgot-password", json={
            "email": "nobody@test.com"
        })
        assert resp.status_code == 200  # ne doit pas révéler que l'email n'existe pas
