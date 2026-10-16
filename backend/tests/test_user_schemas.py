from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models import User
from app.schemas import UserCreate, UserRead


def test_valid_user_create():
    user = UserCreate(first_name="Ali", last_name="Khan", email="ali@example.com", password="StrongPass123")
    assert user.email == "ali@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(first_name="Ali", last_name="Khan", email="not-an-email", password="StrongPass123")


def test_short_password():
    with pytest.raises(ValidationError):
        UserCreate(first_name="Ali", last_name="Khan", email="ali@example.com", password="123")


def test_admin_field_rejected():
    with pytest.raises(ValidationError):
        UserCreate(first_name="Ali", last_name="Khan", email="ali@example.com",
                   password="StrongPass123", is_admin=True)


def test_user_read_hides_password_hash():
    orm_user = User(id=1, first_name="Ali", last_name="Khan", email="ali@example.com",
                    password_hash="$argon2...", is_active=True, created_at=datetime.now(timezone.utc))
    data = UserRead.model_validate(orm_user).model_dump()
    assert "password" not in data
    assert "password_hash" not in data