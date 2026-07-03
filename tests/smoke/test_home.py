from config.setting import BASE_URL, TIMEOUT


def test_home(page):

    page.goto(BASE_URL)
    page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT)

    assert "Automation Exercise" in page.title()

    page.screenshot(path="screenshots/smoke/home.png")