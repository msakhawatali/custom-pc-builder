from app.core.jwt import create_access_token
from app.core.security import hash_password
from app.main import app as fastapi_app
from app.models import User
from tests.conftest import TestingSession

DASHBOARD = fastapi_app.url_path_for("admin_dashboard")


def make_user(email: str, role: str, is_active: bool = True) -> int:
    db = TestingSession()
    try:
        user = User(
            first_name="Test",
            last_name="User",
            email=email,
            password_hash=hash_password("StrongPass123"),
            role=role,
            is_active=is_active,
        )
        db.add(user)
        db.commit()
        return user.id
    finally:
        db.close()


def auth(user_id: int) -> dict:
    return {"Authorization": f"Bearer {create_access_token(user_id)}"}


def test_admin_can_access_dashboard(client):
    admin_id = make_user("admin@example.com", "admin")
    r = client.get(DASHBOARD, headers=auth(admin_id))
    assert r.status_code == 200
    assert r.json() == {"message": "Welcome to the admin dashboard"}


def test_regular_user_cannot_access_dashboard(client):
    user_id = make_user("user@example.com", "user")
    r = client.get(DASHBOARD, headers=auth(user_id))
    assert r.status_code == 403


def test_missing_token_returns_401(client):
    assert client.get(DASHBOARD).status_code == 401


def test_invalid_token_returns_401(client):
    r = client.get(DASHBOARD, headers={"Authorization": "Bearer not.a.valid.token"})
    assert r.status_code == 401


def test_inactive_admin_cannot_access_dashboard(client):
    admin_id = make_user("inactive@example.com", "admin", is_active=False)
    r = client.get(DASHBOARD, headers=auth(admin_id))
    assert r.status_code == 403