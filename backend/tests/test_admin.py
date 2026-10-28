from app.core.jwt import create_access_token
from app.core.security import hash_password
from app.main import app as fastapi_app
from app.models import User
from tests.conftest import TestingSession
from app.api.admin import admin_list_users

DASHBOARD = fastapi_app.url_path_for("admin_dashboard")
USERS = fastapi_app.url_path_for("admin_list_users")


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


def test_admin_can_list_users(client):
    admin_id = make_user("admin@example.com", "admin")
    make_user("user@example.com", "user")
    r = client.get(USERS, headers=auth(admin_id))
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)
    assert len(body) == 2
    assert {u["email"] for u in body} == {"admin@example.com", "user@example.com"}


def test_users_list_has_expected_fields(client):
    admin_id = make_user("admin@example.com", "admin")
    response = client.get(USERS, headers=auth(admin_id))

    assert response.status_code == 200
    user = response.json()[0]

    assert set(user) == {
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "created_at",
    }


def test_users_list_never_exposes_passwords(client):
    admin_id = make_user("admin@example.com", "admin")
    response = client.get(USERS, headers=auth(admin_id))

    assert response.status_code == 200

    for user in response.json():
        assert "password" not in user
        assert "password_hash" not in user


def test_regular_user_cannot_list_users(client):
    user_id = make_user("user@example.com", "user")
    assert client.get(USERS, headers=auth(user_id)).status_code == 403


def test_list_users_missing_token(client):
    assert client.get(USERS).status_code == 401


def test_list_users_invalid_token(client):
    r = client.get(USERS, headers={"Authorization": "Bearer not.a.valid.token"})
    assert r.status_code == 401


def test_inactive_admin_cannot_list_users(client):
    admin_id = make_user("inactive@example.com", "admin", is_active=False)
    assert client.get(USERS, headers=auth(admin_id)).status_code == 403


def test_list_users_empty_database(client):
    admin_id = make_user("admin@example.com", "admin")

    # Test database mein abhi admin user maujood hai,
    # is liye use delete kar dein.
    db = TestingSession()
    try:
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

    response = client.get(USERS, headers=auth(admin_id))

    assert response.status_code == 401


def user_url(user_id: int) -> str:
    return fastapi_app.url_path_for("admin_get_user", user_id=user_id)


def test_admin_can_get_user_by_id(client):
    admin_id = make_user("admin@example.com", "admin")
    target_id = make_user("target@example.com", "user")
    r = client.get(user_url(target_id), headers=auth(admin_id))
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == target_id
    assert body["email"] == "target@example.com"


def test_get_user_response_matches_user_read_fields(client):
    admin_id = make_user("admin@example.com", "admin")
    body = client.get(user_url(admin_id), headers=auth(admin_id)).json()
    assert set(body) == {
        "id", "first_name", "last_name", "email", "is_active", "created_at",
    }


def test_get_user_never_exposes_password(client):
    admin_id = make_user("admin@example.com", "admin")
    r = client.get(user_url(admin_id), headers=auth(admin_id))
    assert "password" not in r.text


def test_get_nonexistent_user_returns_404(client):
    admin_id = make_user("admin@example.com", "admin")
    r = client.get(user_url(99999), headers=auth(admin_id))
    assert r.status_code == 404


def test_regular_user_cannot_get_user_by_id(client):
    user_id = make_user("user@example.com", "user")
    r = client.get(user_url(user_id), headers=auth(user_id))
    assert r.status_code == 403


def test_regular_user_gets_403_even_for_nonexistent_id(client):
    user_id = make_user("user@example.com", "user")
    r = client.get(user_url(99999), headers=auth(user_id))
    assert r.status_code == 403


def test_get_user_missing_token_returns_401(client):
    assert client.get(user_url(1)).status_code == 401


def test_get_user_invalid_token_returns_401(client):
    r = client.get(user_url(1), headers={"Authorization": "Bearer not.a.valid.token"})
    assert r.status_code == 401


def test_inactive_admin_cannot_get_user_by_id(client):
    admin_id = make_user("inactive@example.com", "admin", is_active=False)
    r = client.get(user_url(admin_id), headers=auth(admin_id))
    assert r.status_code == 403
