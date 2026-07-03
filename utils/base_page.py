from pathlib import Path

from config.setting import TIMEOUT
from playwright.sync_api import TimeoutError


class BasePage:
    """Shared base page object with common browser actions."""

    def __init__(self, page):
        self.page = page

    def is_visible(self, selector):
        """Return whether a selector is visible within the configured timeout."""
        locator = self.page.locator(selector)
        try:
            locator.wait_for(state="visible", timeout=TIMEOUT)
            return True
        except TimeoutError:
            return False

    def visit(self, url):
        """Open a URL and wait for DOM content to load."""
        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=TIMEOUT
        )

    def click(self, selector):
        """Wait for an element to become visible and click it."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=TIMEOUT)
        locator.click()

    def fill(self, selector, text):
        """Wait for an input to become visible and fill text."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=TIMEOUT)
        locator.fill(text)

    def text(self, selector):
        """Return visible text content from a locator."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=TIMEOUT)
        return locator.text_content()

    def screenshot(self, name):
        path = Path("screenshots") / f"{name}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path))