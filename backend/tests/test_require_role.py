import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import require_role
from app.db.dependencies import get_db
from app.core.jwt import create_access_token
from app.core.roles import UserRole
from app.core.security import hash_password
from app.models import User
from tests.conftest import TestingSession


def _override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


def _make_user(role: str, email: str) -> int:
    db = TestingSession()
    user = User(
        first_name="T", last_name="U", email=email,
        password_hash=hash_password("StrongPass123"), role=role,
    )
    db.add(user)
    db.commit()
    uid = user.id
    db.close()
    return uid


@pytest.fixture
def role_client(client):  # `client` fixture tables create karta hai
    app = FastAPI()
    app.dependency_overrides[get_db] = _override_get_db

    @app.get("/admin-only")
    def admin_only(user: User = Depends(require_role(UserRole.ADMIN))):
        return {"id": user.id}

    @app.get("/staff")
    def staff(user: User = Depends(require_role(UserRole.ADMIN, UserRole.USER))):
        return {"id": user.id}

    return TestClient(app)


def _h(uid):
    return {"Authorization": f"Bearer {create_access_token(uid)}"}


def test_allowed_role(role_client):
    uid = _make_user("admin", "a@example.com")
    assert role_client.get("/admin-only", headers=_h(uid)).status_code == 200


def test_forbidden_role(role_client):
    uid = _make_user("user", "u@example.com")
    assert role_client.get("/admin-only", headers=_h(uid)).status_code == 403


def test_multiple_allowed_roles(role_client):
    uid = _make_user("user", "m@example.com")
    assert role_client.get("/staff", headers=_h(uid)).status_code == 200


def test_missing_token(role_client):
    assert role_client.get("/admin-only").status_code == 401


def test_invalid_token(role_client):
    r = role_client.get("/admin-only", headers={"Authorization": "Bearer bad.token"})
    assert r.status_code == 401

def test_inactive_admin_forbidden(role_client):
    uid = _make_user("admin", "inactive@example.com")

    db = TestingSession()
    db.query(User).filter(User.id == uid).update({"is_active": False})
    db.commit()
    db.close()

    response = role_client.get("/admin-only", headers=_h(uid))

    assert response.status_code == 403
    assert response.json()["detail"] == "Account is inactive"