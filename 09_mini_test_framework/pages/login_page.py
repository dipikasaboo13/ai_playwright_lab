from playwright.sync_api import Page, Locator
from .base_page import BasePage

class LoginPage(BasePage):
    """Page Object for the SauceDemo Login page."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.locator("#user-name")
        self.password_input: Locator = page.locator("#password")
        self.login_button: Locator = page.locator("#login-button")
        self.error_container: Locator = page.locator("[data-test='error']")

    def navigate(self):
        """Navigate to the login page."""
        self.navigate_to(self.URL)

    def login(self, username: str, password: str):
        """Fill credentials and submit the login form."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        """Get the text content of the error message container."""
        return self.error_container.inner_text()

    def is_error_visible(self) -> bool:
        """Check if the error container is visible."""
        return self.error_container.is_visible()
