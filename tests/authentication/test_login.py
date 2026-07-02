import pytest

from pages.authentication.login_page import LoginPage
from utils.user_manager import load_users


def test_login(page):
    users = load_users()["users"]

    for user in users:
        login = LoginPage(page)

        login.open()

        login_success = login.login(
            user["email"],
            user["password"]
        )

        assert login_success is not None

        if user["expected"] == "success":
            assert login_success
            login.screenshot("login_success")
            login.logout()
            assert login.is_logout_success()
        else:
            assert not login_success
            login.screenshot("login_failed")
