import os

import pytest

from config.setting import BASE_URL, TIMEOUT
from playwright.sync_api import sync_playwright


def test_open():
    running_in_ci = os.getenv("GITHUB_ACTIONS", "").lower() == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=running_in_ci)

        page = browser.new_page()

        page.goto(BASE_URL)
        page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

        title = page.title()
        if running_in_ci and "One moment, please..." in title:
            pytest.skip("Cloudflare challenge on CI")

        assert "Automation Exercise" in title

        page.screenshot(path="screenshots/smoke/homepage.png")

        browser.close()