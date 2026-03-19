"""
Tests UNITAIRES — AuthService
Vérifient la logique métier isolée (hashing, validation, CRUD utilisateur).
"""
import pytest
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.schemas.user import UserRegister, UserLogin


# ── Inscription ──────────────────────────────────────────────
class TestRegisterUser:
    def test_register_success(self, db):
        data = UserRegister(username="alice", email="alice@test.com", password="Pass1234")
        user = AuthService.register_user(db, data)

        assert user.username == "alice"
        assert user.email == "alice@test.com"
        assert user.hashed_password != "Pass1234"  # mot de passe bien hashé

    def test_register_duplicate_email(self, db):
        data = UserRegister(username="bob", email="dup@test.com", password="Pass1234")
        AuthService.register_user(db, data)

        with pytest.raises(HTTPException) as exc:
            AuthService.register_user(
                db, UserRegister(username="charlie", email="dup@test.com", password="Pass1234")
            )
        assert exc.value.status_code == 400

    def test_register_duplicate_username(self, db):
        data = UserRegister(username="samename", email="a@test.com", password="Pass1234")
        AuthService.register_user(db, data)

        with pytest.raises(HTTPException) as exc:
            AuthService.register_user(
                db, UserRegister(username="samename", email="b@test.com", password="Pass1234")
            )
        assert exc.value.status_code == 400


# ── Authentification ─────────────────────────────────────────
class TestAuthenticateUser:
    def test_authenticate_success(self, db):
        AuthService.register_user(
            db, UserRegister(username="auth1", email="auth@test.com", password="Pass1234")
        )
        user = AuthService.authenticate_user(
            db, UserLogin(email="auth@test.com", password="Pass1234")
        )
        assert user is not False
        assert user.email == "auth@test.com"

    def test_authenticate_wrong_password(self, db):
        AuthService.register_user(
            db, UserRegister(username="auth2", email="auth2@test.com", password="Pass1234")
        )
        result = AuthService.authenticate_user(
            db, UserLogin(email="auth2@test.com", password="WrongPwd")
        )
        assert result is False

    def test_authenticate_unknown_email(self, db):
        result = AuthService.authenticate_user(
            db, UserLogin(email="ghost@test.com", password="Pass1234")
        )
        assert result is False


# ── Mise à jour du profil ────────────────────────────────────
class TestUpdateProfile:
    def test_update_username(self, db):
        user = AuthService.register_user(
            db, UserRegister(username="old", email="up@test.com", password="Pass1234")
        )
        updated = AuthService.update_user_profile(db, user, {"username": "new"})
        assert updated.username == "new"
        assert updated.email == "up@test.com"

    def test_update_email_conflict(self, db):
        AuthService.register_user(
            db, UserRegister(username="u1", email="taken@test.com", password="Pass1234")
        )
        user2 = AuthService.register_user(
            db, UserRegister(username="u2", email="free@test.com", password="Pass1234")
        )
        with pytest.raises(HTTPException) as exc:
            AuthService.update_user_profile(db, user2, {"email": "taken@test.com"})
        assert exc.value.status_code == 400


# ── Suppression de compte ────────────────────────────────────
class TestDeleteAccount:
    def test_delete_success(self, db):
        user = AuthService.register_user(
            db, UserRegister(username="del", email="del@test.com", password="Pass1234")
        )
        result = AuthService.delete_user_account(db, user)
        assert result is True
        assert AuthService.get_user_by_email(db, "del@test.com") is None


# ── Changement de mot de passe ───────────────────────────────
class TestChangePassword:
    def test_change_password_success(self, db):
        user = AuthService.register_user(
            db, UserRegister(username="chg", email="chg@test.com", password="OldPass1")
        )
        result = AuthService.change_user_password(db, user, "OldPass1", "NewPass2")
        assert result is True
        # Vérifier que le nouveau mot de passe fonctionne
        logged = AuthService.authenticate_user(
            db, UserLogin(email="chg@test.com", password="NewPass2")
        )
        assert logged is not False

    def test_change_password_wrong_old(self, db):
        user = AuthService.register_user(
            db, UserRegister(username="chg2", email="chg2@test.com", password="OldPass1")
        )
        with pytest.raises(HTTPException) as exc:
            AuthService.change_user_password(db, user, "WrongOld", "NewPass2")
        assert exc.value.status_code == 400


# ── Forgot / Reset Password ─────────────────────────────────
class TestForgotPassword:
    def test_forgot_existing_email(self, db):
        AuthService.register_user(
            db, UserRegister(username="fg", email="fg@test.com", password="Pass1234")
        )
        result = AuthService.forgot_password(db, "fg@test.com")
        assert "message" in result

    def test_forgot_unknown_email(self, db):
        result = AuthService.forgot_password(db, "unknown@test.com")
        assert "message" in result  # ne doit pas lever d'erreur
