from playwright.sync_api import Page, Locator
from .base_page import BasePage

class InventoryPage(BasePage):
    """Page Object for the SauceDemo Inventory/Products page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(".title")
        self.inventory_items: Locator = page.locator(".inventory_item")
        self.shopping_cart_link: Locator = page.locator(".shopping_cart_link")
        self.shopping_cart_badge: Locator = page.locator(".shopping_cart_badge")

    def get_page_title(self) -> str:
        """Get the main title text of the inventory page."""
        return self.page_title.inner_text()

    def add_item_to_cart(self, item_name: str):
        """Add a specific item to cart by its product title."""
        item = self.inventory_items.filter(has_text=item_name)
        add_btn = item.locator("button")
        add_btn.click()

    def get_cart_badge_count(self) -> int:
        """Get the integer count displayed on the cart badge, or 0 if empty."""
        if self.shopping_cart_badge.is_visible():
            return int(self.shopping_cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        """Click the shopping cart link to navigate to the cart page."""
        self.shopping_cart_link.click()
