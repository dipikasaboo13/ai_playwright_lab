from typing import List
from playwright.sync_api import Page, Locator
from .base_page import BasePage

class CartPage(BasePage):
    """Page Object for the SauceDemo Cart page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_title: Locator = page.locator(".title")
        self.cart_items: Locator = page.locator(".cart_item")
        self.item_names: Locator = page.locator(".inventory_item_name")
        self.checkout_button: Locator = page.locator("#checkout")
        self.continue_shopping_button: Locator = page.locator("#continue-shopping")

    def get_item_names(self) -> List[str]:
        """Return a list of product names currently in the cart."""
        return self.item_names.all_inner_texts()

    def is_item_in_cart(self, item_name: str) -> bool:
        """Check if an item with the given name exists in the cart."""
        return item_name in self.get_item_names()

    def remove_item(self, item_name: str):
        """Remove an item from the cart by its product title."""
        item = self.cart_items.filter(has_text=item_name)
        remove_btn = item.locator("button")
        remove_btn.click()

    def click_checkout(self):
        """Click the checkout button."""
        self.checkout_button.click()
