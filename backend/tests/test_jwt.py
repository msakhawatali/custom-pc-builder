from datetime import timedelta

from app.core.jwt import create_access_token, decode_access_token


def test_generate_and_decode_valid_token():
    token = create_access_token(42)
    assert isinstance(token, str)
    assert decode_access_token(token) == 42


def test_expired_token_returns_none():
    token = create_access_token(42, expires_delta=timedelta(seconds=-1))
    assert decode_access_token(token) is None


def test_malformed_token_returns_none():
    assert decode_access_token("not.a.jwt") is None


def test_tampered_token_returns_none():
    token = create_access_token(42)
    assert decode_access_token(token[:-2] + "xx") is None