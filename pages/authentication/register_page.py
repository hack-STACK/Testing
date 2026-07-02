import time

from config.setting import LOGIN_URL
from utils.base_page import BasePage


class RegisterPage(BasePage):

    URL = LOGIN_URL

    NAME = "input[data-qa='signup-name']"
    EMAIL = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"

    ACCOUNT_INFO = "text=Enter Account Information"

    def open(self):
        self.visit(self.URL)

    def generate_email(self):
        return f"juan{int(time.time())}@gmail.com"

    def register(self, name):
        email = self.generate_email()

        self.fill(self.NAME, name)
        self.fill(self.EMAIL, email)
        self.click(self.SIGNUP_BUTTON)

        return email

    def is_register_page_open(self):
        return self.page.locator(self.ACCOUNT_INFO).is_visible()