"""
Dashboard Page Object encapsulating navigation bar elements, key metric indicators,
product search form interactions, and navigation actions.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class DashboardPage(BasePage):
    # Locators
    CURRENT_USER = "#current-user"
    WELCOME_MESSAGE = "#welcome-message"
    NAV_CHECKOUT = "#nav-checkout"
    NAV_LOGOUT = "#nav-logout"
    METRIC_SALES = "#metric-sales"
    METRIC_USERS = "#metric-users"
    METRIC_ORDERS = "#metric-orders"
    SEARCH_INPUT = "#search-input"
    SEARCH_BUTTON = "#btn-search"
    SEARCH_RESULTS = "#search-results"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_current_username(self) -> str:
        """Retrieve active logged in username from welcome banner."""
        return self.get_text(self.CURRENT_USER)

    def get_metrics(self) -> dict:
        """Return dictionary containing current dashboard card metric values."""
        return {
            "sales": self.get_text(self.METRIC_SALES),
            "users": self.get_text(self.METRIC_USERS),
            "orders": self.get_text(self.METRIC_ORDERS)
        }

    def search_product(self, query: str) -> None:
        """Fill search input and submit query form."""
        self.fill(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def get_search_results_text(self) -> str:
        """Retrieve rendered search result banner text."""
        return self.get_text(self.SEARCH_RESULTS)

    def navigate_to_checkout(self) -> None:
        """Click Checkout link in top navbar."""
        self.click(self.NAV_CHECKOUT)

    def logout(self) -> None:
        """Click Logout button in navbar."""
        self.click(self.NAV_LOGOUT)
