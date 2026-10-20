REGISTER = "/v1/auth/register"
LOGIN = "/v1/auth/login"

USER = {
    "first_name": "Ali",
    "last_name": "Khan",
    "email": "ali@example.com",
    "password": "StrongPass123",
}


def register(client):
    return client.post(REGISTER, json=USER)


def test_login_success(client):
    register(client)
    r = client.post(LOGIN, json={"email": USER["email"], "password": USER["password"]})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert "password" not in body and "password_hash" not in body


def test_login_wrong_password(client):
    register(client)
    r = client.post(LOGIN, json={"email": USER["email"], "password": "WrongPass999"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"


def test_login_unknown_email(client):
    r = client.post(LOGIN, json={"email": "nobody@example.com", "password": "StrongPass123"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"


def test_login_inactive_user(client):
    from tests.conftest import TestingSession
    from app.models import User

    register(client)
    db = TestingSession()
    db.query(User).filter(User.email == USER["email"]).update({"is_active": False})
    db.commit()
    db.close()

    r = client.post(LOGIN, json={"email": USER["email"], "password": USER["password"]})
    assert r.status_code == 403