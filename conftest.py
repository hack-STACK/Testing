import os
import pytest

from config.setting import BROWSER, HEADLESS
from playwright.sync_api import sync_playwright


@pytest.fixture
def page(request):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            channel=BROWSER,
            headless=HEADLESS,
            args=["--start-maximized"]
        )

        context = browser.new_context(
            viewport=None,
            record_video_dir="videos/"
        )

        page = context.new_page()

        yield page

        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:

            os.makedirs("screenshots/failed", exist_ok=True)

            page.screenshot(
                path=f"screenshots/failed/{request.node.name}.png",
                full_page=True
            )

        context.close()
        browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)


def pytest_collection_modifyitems(session, config, items):
    """Ensure authentication tests run in the intended sequential order."""
    auth_order = {
        "tests/authentication/test_register.py": 0,
        "tests/authentication/test_login.py": 1,
        "tests/authentication/test_logout.py": 2,
        "tests/authentication/test_delete_account.py": 3,
        "tests/authentication/test_signup.py": 4,
    }

    def sort_key(item):
        file_path = item.nodeid.split("::", 1)[0]
        if file_path in auth_order:
            return (0, auth_order[file_path], item.nodeid)
        return (1, file_path, item.nodeid)

    items.sort(key=sort_key)