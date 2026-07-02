from utils.base_page import BasePage
from playwright.sync_api import TimeoutError
import time


class SignupPage(BasePage):

    URL = "https://automationexercise.com"

    # Home Page
    SIGNUP_LOGIN_BUTTON = "a[href='/login']"

    # Signup Form
    SIGNUP_TITLE = "text=New User Signup!"

    NAME_INPUT = "input[data-qa='signup-name']"
    EMAIL_INPUT = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"

    # Next Page
    ACCOUNT_INFORMATION_TITLE = "text=Enter Account Information"

    def open(self):
        self.visit(self.URL)

    def click_signup_login(self):
        self.click(self.SIGNUP_LOGIN_BUTTON)

    def is_signup_visible(self):
        try:
            self.page.wait_for_selector(
                self.SIGNUP_TITLE,
                state="visible",
                timeout=10000
            )
            return True
        except TimeoutError:
            return False

    def generate_email(self):
        timestamp = int(time.time())
        return f"juan.testing{timestamp}@gmail.com"

    def signup(self, name, email=None):

        if email is None:
            email = self.generate_email()

        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.click(self.SIGNUP_BUTTON)

        return{
            "name": name,
            "email": email
        }

    def is_account_information_visible(self):
        return self.page.locator(
            self.ACCOUNT_INFORMATION_TITLE
        ).is_visible()