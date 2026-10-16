from app.core.security import hash_password, verify_password


def test_hash_is_not_plain_text():
    hashed = hash_password("StrongPass123")
    assert hashed != "StrongPass123"


def test_verify_correct_password():
    hashed = hash_password("StrongPass123")
    assert verify_password("StrongPass123", hashed) is True


def test_verify_wrong_password():
    hashed = hash_password("StrongPass123")
    assert verify_password("WrongPass999", hashed) is False