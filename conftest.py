import os
import shutil
from pathlib import Path

import pytest

from config.setting import BROWSER, HEADLESS
from playwright.sync_api import sync_playwright


def get_module_from_test_path(test_path):
    """Extract module name from test path.
    
    Examples:
        'tests/authentication/test_login.py' -> 'authentication'
        'tests/product/test_search.py' -> 'product'
        'tests/cart/test_checkout.py' -> 'cart'
        'tests/smoke/test_home.py' -> 'smoke'
    """
    parts = test_path.split("/")
    if len(parts) >= 2 and parts[0] == "tests":
        return parts[1]
    return "other"


def organize_video(test_path, test_name):
    """Move and rename video file to organized folder structure.
    
    Videos are recorded with random GUIDs by Playwright.
    This function moves them to: videos/{module}/{test_name}.webm
    """
    module = get_module_from_test_path(test_path)
    videos_dir = Path("videos")
    module_dir = videos_dir / module
    
    # Create module directory
    module_dir.mkdir(parents=True, exist_ok=True)
    
    # Find the most recent video file (latest by modification time)
    video_files = sorted(
        videos_dir.glob("page@*.webm"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    
    if video_files:
        latest_video = video_files[0]
        new_path = module_dir / f"{test_name}.webm"
        
        try:
            shutil.move(str(latest_video), str(new_path))
        except Exception:
            # If move fails, just leave the original file
            pass


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
        
        # Organize video after test completes
        test_path = request.node.nodeid.split("::")[0]
        test_name = request.node.name
        organize_video(test_path, test_name)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)