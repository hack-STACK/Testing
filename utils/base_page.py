class BasePage:
    def __init__(self, page):
        self.page = page

    def visit(self, url):
        self.page.goto(url)

    def click(self, selector):
        self.page.locator(selector).click()

    def fill(self, selector, text):
        self.page.locator(selector).fill(text)

    def text(self, selector):
        return self.page.locator(selector).text_content()

    def screenshot(self, name):
        self.page.screenshot(path=f"screenshots/{name}.png")