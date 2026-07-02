import pytest

from pages.login_page import LoginPage
from utils.data_reader import load_json

users = load_json("data/users.json")["users"]


@pytest.mark.parametrize("user", users)
def test_login(page, user):

    login = LoginPage(page)

    login.open()

    login.login(
        user["email"],
        user["password"]
    )

    if user["expected"] == "success":

        assert login.is_login_success()

        login.screenshot("login_success")

        login.logout()

    else:

        assert login.is_login_failed()

        login.screenshot("login_failed")