from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to the given URL."""
        self.page.goto(url)
        return self

    def click(self, selector: str):
        """Click an element specified by the selector."""
        self.page.click(selector)
        return self

    def fill(self, selector: str, text: str):
        """Fill a text input with the given text."""
        self.page.fill(selector, text)
        return self

    def get_text(self, selector: str) -> str:
        """Get the text content of an element."""
        return self.page.text_content(selector)

    def assert_text(self, selector: str, expected_text: str):
        """Assert that the text content of an element matches the expected text."""
        element = self.page.locator(selector)
        expect(element).to_have_text(expected_text)
        return self

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible on the page."""
        return self.page.is_visible(selector)
