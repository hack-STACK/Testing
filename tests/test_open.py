from playwright.sync_api import sync_playwright


def test_open():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto("https://automationexercise.com")

        assert "Automation Exercise" in page.title()

        page.screenshot(path="screenshots/homepage.png")

        page.wait_for_timeout(3000)

        browser.close()