from datetime import timedelta

from app.core.jwt import create_access_token
from app.models import User
from tests.conftest import TestingSession
from app.main import app as fastapi_app


REGISTER = fastapi_app.url_path_for("register")
LOGIN = fastapi_app.url_path_for("login")
ME = fastapi_app.url_path_for("read_current_user")

USER = {
    "first_name": "Ali",
    "last_name": "Khan",
    "email": "ali@example.com",
    "password": "StrongPass123",
}


def register_and_login(client) -> str:
    client.post(REGISTER, json=USER)
    r = client.post(LOGIN, json={"email": USER["email"], "password": USER["password"]})
    return r.json()["access_token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_me_success(client):
    token = register_and_login(client)
    r = client.get(ME, headers=auth(token))
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == USER["email"]
    assert body["first_name"] == "Ali"
    assert "password" not in body and "password_hash" not in body


def test_me_missing_token(client):
    assert client.get(ME).status_code == 401


def test_me_invalid_token(client):
    assert client.get(ME, headers=auth("not.a.jwt")).status_code == 401


def test_me_expired_token(client):
    register_and_login(client)
    token = create_access_token(1, expires_delta=timedelta(seconds=-1))
    assert client.get(ME, headers=auth(token)).status_code == 401


def test_me_user_deleted(client):
    token = register_and_login(client)
    db = TestingSession()
    db.query(User).delete()
    db.commit()
    db.close()
    assert client.get(ME, headers=auth(token)).status_code == 401


def test_me_inactive_user(client):
    token = register_and_login(client)
    db = TestingSession()
    db.query(User).update({"is_active": False})
    db.commit()
    db.close()
    assert client.get(ME, headers=auth(token)).status_code == 403