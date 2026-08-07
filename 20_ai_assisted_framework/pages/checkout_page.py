"""
Checkout Page Object encapsulating cart breakdown, promo discount inputs,
total calculation getters, checkout submission, and order confirmation retrieval.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutPage(BasePage):
    # Locators
    CART_TABLE = "#cart-table"
    CART_QTY = "#cart-qty"
    CART_SUBTOTAL = "#cart-subtotal"
    PROMO_INPUT = "#promo-input"
    APPLY_PROMO_BUTTON = "#btn-apply-promo"
    PROMO_SUCCESS = "#promo-success"
    CHECKOUT_ERROR = "#checkout-error"
    DISCOUNT_VAL = "#discount-val"
    TOTAL_VAL = "#total-val"
    SUBMIT_ORDER_BUTTON = "#btn-submit-order"
    CONFIRMATION_CODE = "#confirmation-code"
    CONFIRMED_TOTAL = "#confirmed-total"
    BACK_DASHBOARD_LINK = "#link-back-dashboard"

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate_to_checkout(self, base_url: str) -> None:
        """Directly navigate to checkout endpoint."""
        self.navigate(f"{base_url.rstrip('/')}/checkout")

    def apply_promo_code(self, promo_code: str) -> None:
        """Fill promo code input and click apply button."""
        self.fill(self.PROMO_INPUT, promo_code)
        self.click(self.APPLY_PROMO_BUTTON)

    def get_discount_text(self) -> str:
        """Retrieve applied discount amount text string."""
        return self.get_text(self.DISCOUNT_VAL)

    def get_total_text(self) -> str:
        """Retrieve total calculated order amount text string."""
        return self.get_text(self.TOTAL_VAL)

    def get_promo_success_message(self) -> str:
        """Retrieve success banner text after applying valid promo code."""
        return self.get_text(self.PROMO_SUCCESS)

    def get_checkout_error_message(self) -> str:
        """Retrieve error banner text on invalid promo code or checkout error."""
        return self.get_text(self.CHECKOUT_ERROR)

    def submit_order(self) -> None:
        """Click complete purchase button to finalize checkout order."""
        self.click(self.SUBMIT_ORDER_BUTTON)

    def get_confirmation_code(self) -> str:
        """Retrieve order confirmation reference code from confirmation card."""
        return self.get_text(self.CONFIRMATION_CODE)

    def get_confirmed_total(self) -> str:
        """Retrieve confirmed order total charged amount from confirmation card."""
        return self.get_text(self.CONFIRMED_TOTAL)
