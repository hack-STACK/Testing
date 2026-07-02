from pages.authentication.signup_page import SignupPage


def test_signup(page):

    signup = SignupPage(page)

    signup.open()

    signup.click_signup_login()

    assert signup.is_signup_visible()

    email = signup.signup("Juan Testing")

    print("Email:", email)

    assert signup.is_account_information_visible()

    signup.screenshot("signup")