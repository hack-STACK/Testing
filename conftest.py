import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel="msedge",
            headless=False,
            args=["--start-maximized"]
        )

        context = browser.new_context(viewport=None)

        page = context.new_page()

        yield page

        browser.close()