from pages.authentication.login_page import LoginPage
from pages.authentication.account_page import AccountPage
from utils.user_manager import load_users


def test_delete_account(page):

    users = load_users()["users"]

    user = users[0]

    login = LoginPage(page)
    account = AccountPage(page)

    login.open()

    login.login(
        user["email"],
        user["password"]
    )

    page.wait_for_load_state("domcontentloaded")

    assert login.is_login_success()

    account.screenshot("01_logged_in")

    account.delete_account()

    page.wait_for_load_state("domcontentloaded")

    assert account.is_account_deleted()

    account.screenshot("02_account_deleted")

    account.continue_after_delete()

    page.wait_for_load_state("domcontentloaded")