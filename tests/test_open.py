from config.setting import BASE_URL, TIMEOUT
from playwright.sync_api import sync_playwright


def test_open():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

        assert "Automation Exercise" in page.title()

        page.screenshot(path="screenshots/homepage.png")

        browser.close()