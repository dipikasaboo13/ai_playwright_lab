"""
Checkout Test Suite for Project 20 AI-Assisted Test Framework.
Validates promo code discount calculations, total order amounts, and order confirmation flows.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.checkout_page import CheckoutPage


@pytest.mark.smoke
@pytest.mark.regression
def test_checkout_valid_promo_discount(page: Page, server_url: str):
    """
    Verify applying valid promo code 'AI20' deducts 20% discount and updates total amount.
    """
    checkout_page = CheckoutPage(page)
    checkout_page.navigate_to_checkout(server_url)

    # Apply promo code AI20 (20% off $300 subtotal = $60 discount, $240 total)
    checkout_page.apply_promo_code("AI20")

    assert checkout_page.get_promo_success_message() == 'Promo code "AI20" applied! (20% Off)'
    assert checkout_page.get_discount_text() == "-$60.00"
    assert checkout_page.get_total_text() == "$240.00"


@pytest.mark.regression
def test_checkout_invalid_promo_code(page: Page, server_url: str):
    """
    Verify applying invalid promo code triggers error banner and retains full total amount.
    """
    checkout_page = CheckoutPage(page)
    checkout_page.navigate_to_checkout(server_url)

    checkout_page.apply_promo_code("INVALID_CODE")

    assert checkout_page.get_checkout_error_message() == "Invalid promo code: INVALID_CODE"
    assert checkout_page.get_discount_text() == "-$0.00"
    assert checkout_page.get_total_text() == "$300.00"


@pytest.mark.smoke
@pytest.mark.regression
def test_checkout_order_completion(page: Page, server_url: str):
    """
    Verify completing purchase submits order and renders confirmation page with reference code.
    """
    checkout_page = CheckoutPage(page)
    checkout_page.navigate_to_checkout(server_url)

    checkout_page.apply_promo_code("HALFPRICE")
    checkout_page.submit_order()

    # Verify confirmation card
    conf_code = checkout_page.get_confirmation_code()
    assert conf_code.startswith("CONF-")
    assert checkout_page.get_confirmed_total() == "$150.00"
