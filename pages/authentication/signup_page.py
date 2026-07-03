from uuid import uuid4

from config.setting import BASE_URL, TIMEOUT
from utils.base_page import BasePage


class SignupPage(BasePage):

    URL = BASE_URL

    # ==========================
    # Home Page
    # ==========================

    SIGNUP_LOGIN_BUTTON = "a[href='/login']"

    # ==========================
    # Signup Form
    # ==========================

    SIGNUP_TITLE = "text=New User Signup!"

    NAME_INPUT = "input[data-qa='signup-name']"
    EMAIL_INPUT = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"

    # ==========================
    # Account Page
    # ==========================

    ACCOUNT_INFORMATION = "text=Enter Account Information"

    # =====================================================

    def open(self):
        self.visit(self.URL)

    def click_signup_login(self):
        self.click(self.SIGNUP_LOGIN_BUTTON)

    # =====================================================

    def is_signup_visible(self):
        return self.is_visible(self.SIGNUP_TITLE)

    # =====================================================

    def generate_email(self):
        return f"juan.testing.{uuid4().hex[:8]}@gmail.com"

    # =====================================================

    def signup(self, name, email=None):

        if email is None:
            email = self.generate_email()

        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)

        self.click(self.SIGNUP_BUTTON)

        self.page.wait_for_selector(
            self.ACCOUNT_INFORMATION,
            state="visible",
            timeout=TIMEOUT
        )

        return {
            "name": name,
            "email": email
        }

    def is_account_information_visible(self):
        return self.is_visible(self.ACCOUNT_INFORMATION)
