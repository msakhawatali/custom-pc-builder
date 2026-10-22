from datetime import timedelta

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_user
from app.core.jwt import create_access_token
from app.db.dependencies import get_db
from app.models import User

from tests.conftest import TestingSession, engine
from app.db.base import Base

import pytest

probe_app = FastAPI()


@probe_app.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id}


@pytest.fixture()
def probe():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    probe_app.dependency_overrides[get_db] = override_get_db
    yield TestClient(probe_app)
    probe_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def make_user(is_active=True) -> int:
    db = TestingSession()
    user = User(first_name="Ali", last_name="Khan", email="ali@example.com",
                password_hash="x", is_active=is_active)
    db.add(user)
    db.commit()
    uid = user.id
    db.close()
    return uid


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_valid_token(probe):
    uid = make_user()
    r = probe.get("/me", headers=auth(create_access_token(uid)))
    assert r.status_code == 200
    assert r.json()["id"] == uid


def test_missing_token(probe):
    assert probe.get("/me").status_code == 401


def test_invalid_token(probe):
    assert probe.get("/me", headers=auth("not.a.jwt")).status_code == 401


def test_expired_token(probe):
    uid = make_user()
    token = create_access_token(uid, expires_delta=timedelta(seconds=-1))
    assert probe.get("/me", headers=auth(token)).status_code == 401


def test_user_does_not_exist(probe):
    assert probe.get("/me", headers=auth(create_access_token(9999))).status_code == 401


def test_inactive_user(probe):
    uid = make_user(is_active=False)
    r = probe.get("/me", headers=auth(create_access_token(uid)))
    assert r.status_code == 403