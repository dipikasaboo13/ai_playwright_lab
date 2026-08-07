"""
Login Page Object encapsulating locators, form field inputs, submission actions,
and error validation assertions for the login page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#btn-login"
    ERROR_BANNER = "#error-message"
    LOGIN_FORM = "#login-form"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page)
        self.base_url = base_url

    def navigate_to_login(self, base_url: str = "") -> None:
        """Navigate to portal login endpoint."""
        target_url = base_url or self.base_url
        self.navigate(f"{target_url.rstrip('/')}/login")

    def login(self, username: str, password: str) -> None:
        """Fill username and password fields and submit login form."""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Retrieve displayed error banner text message."""
        return self.get_text(self.ERROR_BANNER)

    def is_error_visible(self) -> bool:
        """Check if error banner element is visible on page."""
        return self.is_visible(self.ERROR_BANNER)
