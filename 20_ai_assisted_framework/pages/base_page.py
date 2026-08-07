"""
Base Page Object class encapsulating common Playwright interactions and locator utilities.
All specific domain page objects inherit from this base class.
"""

from playwright.sync_api import Page, Locator, expect
from typing import Optional


class BasePage:
    def __init__(self, page: Page):
        """Initialize BasePage with Playwright Page object instance."""
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to target URL and wait for DOM load state."""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def click(self, selector: str) -> None:
        """Wait for element matching selector and trigger click action."""
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)

    def fill(self, selector: str, text: str) -> None:
        """Clear existing input and fill text into matching element selector."""
        self.page.wait_for_selector(selector, state="visible")
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Retrieve trimmed inner text from matching element selector."""
        self.page.wait_for_selector(selector, state="visible")
        return self.page.inner_text(selector).strip()

    def is_visible(self, selector: str) -> bool:
        """Return True if element matching selector is visible on the page."""
        try:
            return self.page.is_visible(selector)
        except Exception:
            return False

    def wait_for_selector(self, selector: str, timeout: Optional[float] = None) -> Locator:
        """Explicitly wait for selector to be present on DOM and return locator."""
        return self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def get_title(self) -> str:
        """Return current document page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return current browser location page URL."""
        return self.page.url
