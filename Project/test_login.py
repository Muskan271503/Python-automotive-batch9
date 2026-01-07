# test_login.py
import pytest
import time
from login import SecureLoginSystem


@pytest.fixture
def login_system():
    return SecureLoginSystem(max_attempts=3, lock_duration=2)


def test_successful_login(login_system):
    result = login_system.attempt_login("user1", "password123")
    assert result["success"] is True
    assert result["message"] == "Login successful!"


def test_invalid_password(login_system):
    result = login_system.attempt_login("user1", "wrong")
    assert result["success"] is False
    assert "Invalid username or password" in result["message"]


def test_nonexistent_user(login_system):
    result = login_system.attempt_login("ghost", "pass")
    assert result["success"] is False
    # No crash, generic message returned → test passes


def test_empty_input(login_system):
    result = login_system.attempt_login("", "password123")
    assert result["success"] is False
    assert "empty" in result["message"].lower()


def test_lock_after_three_failures(login_system):
    for _ in range(3):
        result = login_system.attempt_login("admin", "wrong")
        assert result["success"] is False

    result = login_system.attempt_login("admin", "secretadmin")
    assert result["success"] is False
    assert "locked" in result["message"].lower()
    assert login_system.is_account_locked("admin") is True


def test_lock_expires(login_system):
    for _ in range(3):
        login_system.attempt_login("user1", "wrong")

    assert login_system.is_account_locked("user1") is True
    time.sleep(3)
    assert login_system.is_account_locked("user1") is False

    result = login_system.attempt_login("user1", "password123")
    assert result["success"] is True