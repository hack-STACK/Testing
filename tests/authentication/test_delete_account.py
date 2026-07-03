from config.setting import REGISTER_DATA_FILE
from pages.authentication.login_page import LoginPage
from pages.authentication.account_page import AccountPage
from pages.authentication.signup_page import SignupPage
from utils.data_reader import load_json
from utils.test_user import generate_user


def test_delete_account(page):

    user = generate_user()

    account_data = load_json(REGISTER_DATA_FILE)["account"]
    address_data = load_json(REGISTER_DATA_FILE)["address"]

    signup = SignupPage(page)
    account = AccountPage(page)
    login = LoginPage(page)

    # Create account (prerequisite for delete account test)
    signup.open()
    signup.click_signup_login()
    assert signup.is_signup_visible()

    signup.signup(user["name"], user["email"])
    page.wait_for_load_state("domcontentloaded")

    assert account.is_account_information_visible()

    account.select_title(account_data["title"])
    account.enter_password(account_data["password"])
    account.select_date_of_birth(
        account_data["day"],
        account_data["month"],
        account_data["year"]
    )

    account.subscribe_newsletter()
    account.subscribe_special_offers()
    account.fill_address(address_data)
    account.create_account()

    page.wait_for_load_state("domcontentloaded")
    assert account.is_account_created()

    account.continue_account()
    page.wait_for_load_state("domcontentloaded")
    assert account.is_logged_in()

    account.screenshot("authentication/01_logged_in")

    # Test delete account scenario
    account.delete_account()

    page.wait_for_load_state("domcontentloaded")

    assert account.is_account_deleted()

    account.screenshot("authentication/02_account_deleted")

    account.continue_after_delete()

    page.wait_for_load_state("domcontentloaded")