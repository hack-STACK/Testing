def test_home(page):

    page.goto("https://automationexercise.com")

    assert "Automation Exercise" in page.title()

    page.screenshot(path="screenshots/home.png")