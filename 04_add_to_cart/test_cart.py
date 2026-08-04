import pytest
from playwright.sync_api import Page, expect

def test_add_to_cart_and_verify_subtotal(page: Page):
    """
    Test Scenario for Project 4: Add Product to Cart
    - Task 4.1: Cart Addition and Dialog Interaction (Handle alerts, select products)
    - Task 4.2: Cart Deletion & Pricing Verification (Verify cart contents, price calculations, and deletion)
    """
    # 1. Navigate to Demoblaze homepage
    page.goto("https://demoblaze.com/")
    page.wait_for_load_state("domcontentloaded")

    # --- Select Product A (e.g., Samsung galaxy s6) ---
    product_a_name = "Samsung galaxy s6"
    page.get_by_role("link", name=product_a_name).click()
    expect(page.get_by_role("heading", name=product_a_name)).to_be_visible()

    # Set up dialog handler for Product A
    def handle_dialog_a(dialog):
        assert "Product added" in dialog.message or dialog.message != ""
        dialog.accept()

    page.once("dialog", handle_dialog_a)
    page.get_by_role("link", name="Add to cart").click()
    page.wait_for_timeout(1500)  # Ensure dialog processing completes

    # Return home
    page.get_by_role("link", name="Home").click()
    page.wait_for_load_state("domcontentloaded")

    # --- Select Product B (e.g., Nokia lumia 1520) ---
    product_b_name = "Nokia lumia 1520"
    page.get_by_role("link", name=product_b_name).click()
    expect(page.get_by_role("heading", name=product_b_name)).to_be_visible()

    # Set up dialog handler for Product B
    def handle_dialog_b(dialog):
        assert "Product added" in dialog.message or dialog.message != ""
        dialog.accept()

    page.once("dialog", handle_dialog_b)
    page.get_by_role("link", name="Add to cart").click()
    page.wait_for_timeout(1500)

    # --- Task 4.2: Cart Deletion & Pricing Verification ---
    page.get_by_role("link", name="Cart", exact=True).click()
    page.wait_for_load_state("domcontentloaded")

    # Verify presence of Product A and Product B in cart table
    table_rows = page.locator("#tbodyid tr")
    expect(table_rows.filter(has_text=product_a_name)).to_be_visible()
    expect(table_rows.filter(has_text=product_b_name)).to_be_visible()

    # Wait for total price element to populate
    total_price_locator = page.locator("#totalp")
    expect(total_price_locator).to_be_visible()

    initial_total_text = total_price_locator.inner_text().strip()
    initial_total = int(initial_total_text)

    # Get price of Product A from table row
    row_a = table_rows.filter(has_text=product_a_name)
    price_a_text = row_a.locator("td:nth-child(3)").inner_text().strip()
    price_a = int(price_a_text)

    # Delete Product A
    row_a.get_by_role("link", name="Delete").click()

    # Assert row A is removed
    expect(table_rows.filter(has_text=product_a_name)).not_to_be_visible()

    # Wait dynamically for total price to update to expected subtotal
    expected_total = initial_total - price_a
    expect(total_price_locator).to_have_text(str(expected_total))

    new_total = int(total_price_locator.inner_text().strip())
    assert new_total == expected_total
