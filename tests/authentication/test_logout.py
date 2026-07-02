from pages.authentication.login_page import LoginPage
from utils.user_manager import load_users


def test_logout(page):

    users = load_users()["users"]

    user = users[0]

    login = LoginPage(page)

    login.open()

    login_success = login.login(
        user["email"],
        user["password"]
    )

    assert login_success

    login.screenshot("01_login_success")

    login.logout()

    assert login.is_logout_success()

    login.screenshot("02_logout_success")