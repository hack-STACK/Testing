from utils.base_page import BasePage


class LoginPage(BasePage):

    URL = "https://automationexercise.com/login"

    EMAIL = "input[data-qa='login-email']"
    PASSWORD = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"

    LOGGED_IN = "text=Logged in as"
    LOGIN_ERROR = "text=Your email or password is incorrect!"

    LOGOUT_BUTTON = "a[href='/logout']"

    def open(self):
        self.visit(self.URL)

    def login(self, email, password):
        self.fill(self.EMAIL, email)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)

    def is_login_success(self):
        return self.page.locator(self.LOGGED_IN).is_visible()

    def is_login_failed(self):
        return self.page.locator(self.LOGIN_ERROR).is_visible()