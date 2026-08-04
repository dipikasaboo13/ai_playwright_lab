from playwright.sync_api import Page

class BasePage:
    """Base Page Object class providing shared page operations and helper methods."""

    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigate to a specified URL."""
        self.page.goto(url)

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()
