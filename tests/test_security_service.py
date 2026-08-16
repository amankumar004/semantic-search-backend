from app.services.security_service import SecurityService


def test_password_hashing():

    security_service = SecurityService()

    password = "mysecretpassword"

    password_hash = security_service.hash_password(password)

    assert password_hash != password
    assert password_hash


def test_password_verification():

    security_service = SecurityService()

    password = "mysecretpassword"

    password_hash = security_service.hash_password(password)

    assert security_service.verify_password(
        password,
        password_hash
    )


def test_wrong_password_fails():

    security_service = SecurityService()

    password = "mysecretpassword"

    password_hash = security_service.hash_password(password)

    assert not security_service.verify_password(
        "wrongpassword",
        password_hash
    )