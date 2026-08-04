import pytest
from playwright.sync_api import Page, expect

def test_successful_checkout(page: Page):
    # 1. Navigate to SauceDemo & login
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # 2. Add items to cart
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("[data-test='add-to-cart-sauce-labs-bike-light']")

    # 3. Navigate to cart
    page.click(".shopping_cart_link")
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    # 4. Proceed to checkout step one
    page.click("#checkout")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    # 5. Fill customer details
    page.fill("#first-name", "Jane")
    page.fill("#last-name", "Doe")
    page.fill("#postal-code", "90210")
    page.click("#continue")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    # 6. Verify subtotal calculations (items total + tax = final total)
    subtotal_text = page.locator(".summary_subtotal_label").text_content()
    tax_text = page.locator(".summary_tax_label").text_content()
    total_text = page.locator(".summary_total_label").text_content()

    assert subtotal_text is not None and tax_text is not None and total_text is not None

    item_total = float(subtotal_text.split("$")[1])
    tax = float(tax_text.split("$")[1])
    total = float(total_text.split("$")[1])

    assert round(item_total + tax, 2) == round(total, 2)

    # 7. Finalize purchase
    page.click("#finish")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    expect(page.locator(".complete-header")).to_contain_text("Thank you for your order!")


def test_missing_postal_code(page: Page):
    # 1. Navigate to SauceDemo & login
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # 2. Add an item and navigate to checkout step one
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    page.click(".shopping_cart_link")
    page.click("#checkout")
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    # 3. Fill first and last name, but leave postal code empty
    page.fill("#first-name", "Jane")
    page.fill("#last-name", "Doe")
    page.click("#continue")

    # 4. Assert dynamic error message
    error_element = page.locator("[data-test='error']")
    expect(error_element).to_be_visible()
    expect(error_element).to_contain_text("Error: Postal Code is required")
