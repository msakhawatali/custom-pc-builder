from app.main import app as fastapi_app
from app.models import User
from tests.conftest import TestingSession

REGISTER = fastapi_app.url_path_for("register")
LOGIN = fastapi_app.url_path_for("login")

VALID_USER = {
    "first_name": "Ali",
    "last_name": "Khan",
    "email": "ali@example.com",
    "password": "StrongPass123",
}


def register(client, **overrides):
    return client.post(REGISTER, json={**VALID_USER, **overrides})


def login(client, email=VALID_USER["email"], password=VALID_USER["password"]):
    return client.post(LOGIN, json={"email": email, "password": password})


# ---------- Registration ----------


def test_register_success(client):
    r = register(client)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == VALID_USER["email"]
    assert body["first_name"] == "Ali"
    assert body["last_name"] == "Khan"
    assert body["is_active"] is True
    assert "id" in body


def test_register_never_returns_password(client):
    body = register(client).json()
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email(client):
    register(client)
    r = register(client)
    assert r.status_code == 409


def test_register_invalid_email(client):
    assert register(client, email="not-an-email").status_code == 422


def test_register_short_password(client):
    assert register(client, password="short").status_code == 422


def test_register_missing_field(client):
    payload = {k: v for k, v in VALID_USER.items() if k != "last_name"}
    assert client.post(REGISTER, json=payload).status_code == 422


# ---------- Login ----------


def test_login_success(client):
    register(client)
    r = login(client)
    assert r.status_code == 200
    body = r.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    register(client)
    assert login(client, password="WrongPass123").status_code == 401


def test_login_unknown_email(client):
    assert login(client, email="nobody@example.com").status_code == 401


def test_login_invalid_credentials_same_message(client):
    register(client)
    wrong_pw = login(client, password="WrongPass123")
    unknown = login(client, email="nobody@example.com")
    assert wrong_pw.json() == unknown.json()


def test_login_inactive_user(client):
    register(client)

    db = TestingSession()
    try:
        db.query(User).filter(
            User.email == VALID_USER["email"]
        ).update({"is_active": False})
        db.commit()
    finally:
        db.close()

    assert login(client).status_code == 403
