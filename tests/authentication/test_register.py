from config.setting import REGISTER_DATA_FILE, USERS_FILE
from pages.authentication.signup_page import SignupPage
from pages.authentication.account_page import AccountPage

from utils.data_reader import load_json
from utils.user_manager import save_login_user


def test_register(page):

    user = load_json(REGISTER_DATA_FILE)

    account_data = user["account"]
    address_data = user["address"]

    signup = SignupPage(page)
    account = AccountPage(page)

    signup.open()

    signup.click_signup_login()

    assert signup.is_signup_visible()

    registered_user = signup.signup("Juan Testing")

    print(f"Registered User : {registered_user['email']}")

    page.wait_for_load_state("domcontentloaded")

    assert account.is_account_information_visible()

    account.screenshot("01_account_information")

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

    account.screenshot("02_filled_form")

    account.create_account()

    page.wait_for_load_state("domcontentloaded")

    assert account.is_account_created()

    account.screenshot("03_account_created")

    account.continue_account()

    page.wait_for_load_state("domcontentloaded")

    assert account.is_logged_in()

    account.screenshot("04_logged_in")

    save_login_user(
        email=registered_user["email"],
        password=account_data["password"]
    )

    print(f"Login data saved to {USERS_FILE}")

    # account.delete_account()

    # page.wait_for_load_state("domcontentloaded")

    # assert account.is_account_deleted()

    # account.screenshot("05_account_deleted")