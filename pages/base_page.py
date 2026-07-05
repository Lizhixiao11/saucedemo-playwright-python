from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ---------- Navigation ----------
    def open(self, url: str):
        """Open a URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Get current URL."""
        return self.page.url

    # ---------- Element Actions ----------
    def click(self, locator: str):
        """Click an element."""
        self.page.locator(locator).click()

    def fill(self, locator: str, value: str):
        """Fill input field."""
        self.page.locator(locator).fill(value)

    def type(self, locator: str, value: str):
        """Type into input field."""
        self.page.locator(locator).type(value)

    def press(self, locator: str, key: str):
        """Press keyboard key."""
        self.page.locator(locator).press(key)

    # ---------- Element Information ----------
    def get_text(self, locator: str) -> str:
        """Get text content."""
        return self.page.locator(locator).inner_text().strip()

    def get_value(self, locator: str) -> str:
        """Get input value."""
        return self.page.locator(locator).input_value()

    # ---------- State ----------
    def is_visible(self, locator: str) -> bool:
        """Check element visibility."""
        return self.page.locator(locator).is_visible()

    def is_enabled(self, locator: str) -> bool:
        """Check element enabled."""
        return self.page.locator(locator).is_enabled()

    # ---------- Wait ----------
    def wait_for_visible(self, locator: str):
        """Wait until element is visible."""
        expect(self.page.locator(locator)).to_be_visible()

    def wait_for_hidden(self, locator: str):
        """Wait until element is hidden."""
        expect(self.page.locator(locator)).to_be_hidden()

    # ---------- Assertion ----------
    def should_have_text(self, locator: str, text: str):
        """Assert element text."""
        expect(self.page.locator(locator)).to_have_text(text)

    def should_contain_text(self, locator: str, text: str):
        """Assert element contains text."""
        expect(self.page.locator(locator)).to_contain_text(text)

    def should_have_url(self, url: str):
        """Assert current URL."""
        expect(self.page).to_have_url(url)

    # ---------- Screenshot ----------
    def screenshot(self, path: str):
        """Take screenshot."""
        self.page.screenshot(path=path)