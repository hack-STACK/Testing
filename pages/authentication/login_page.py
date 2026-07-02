from config.setting import LOGIN_URL, TIMEOUT
from playwright.sync_api import TimeoutError
from utils.base_page import BasePage


class LoginPage(BasePage):

    URL = LOGIN_URL

    # ==========================
    # Login Form
    # ==========================

    EMAIL = "input[data-qa='login-email']"
    PASSWORD = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"

    # ==========================
    # Navigation
    # ==========================

    LOGOUT_BUTTON = "a[href='/logout']"

    # ==========================
    # Validation
    # ==========================

    LOGGED_IN = "text=Logged in as"
    LOGIN_ERROR = "text=Your email or password is incorrect!"

    # =====================================================

    def open(self):
        self.visit(self.URL)

    # =====================================================

    def login(self, email, password):
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

        try:
            self.page.wait_for_selector(self.LOGGED_IN, timeout=TIMEOUT)
            return True
        except TimeoutError:
            self.page.wait_for_selector(self.LOGIN_ERROR, timeout=TIMEOUT)
            return False

    # =====================================================

    def logout(self):
        self.click(self.LOGOUT_BUTTON)
        self.page.wait_for_selector(self.LOGIN_BUTTON, timeout=TIMEOUT)

    # =====================================================

    def is_login_success(self):
        return self.page.locator(
            self.LOGGED_IN
        ).is_visible()

    def is_login_failed(self):
        return self.page.locator(
            self.LOGIN_ERROR
        ).is_visible()

    def is_logout_success(self):
        return self.page.locator(
            self.LOGIN_BUTTON
        ).is_visible()