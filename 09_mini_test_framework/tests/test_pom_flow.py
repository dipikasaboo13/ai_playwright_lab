import pytest
from playwright.sync_api import Page, expect
from pages import LoginPage, InventoryPage, CartPage

def test_pom_successful_login_and_cart_flow(page: Page):
    """Verify standard user login, adding item to cart, and checking cart page using POM."""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # 1. Navigate and Login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # 2. Assert Inventory Page loaded
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    assert inventory_page.get_page_title() == "Products"

    # 3. Add item to cart
    item_name = "Sauce Labs Backpack"
    inventory_page.add_item_to_cart(item_name)
    assert inventory_page.get_cart_badge_count() == 1

    # 4. Navigate to Cart and verify item
    inventory_page.go_to_cart()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    assert cart_page.is_item_in_cart(item_name)

def test_pom_invalid_login_error(page: Page):
    """Verify error message displayed on locked out user login using POM."""
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("locked_out_user", "secret_sauce")

    assert login_page.is_error_visible()
    assert "Epic sadface: Sorry, this user has been locked out." in login_page.get_error_text()

def test_pom_cart_item_removal(page: Page):
    """Verify adding multiple items and removing one item from cart using POM."""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    item1 = "Sauce Labs Backpack"
    item2 = "Sauce Labs Bike Light"

    inventory_page.add_item_to_cart(item1)
    inventory_page.add_item_to_cart(item2)
    assert inventory_page.get_cart_badge_count() == 2

    inventory_page.go_to_cart()
    assert cart_page.is_item_in_cart(item1)
    assert cart_page.is_item_in_cart(item2)

    cart_page.remove_item(item1)
    assert not cart_page.is_item_in_cart(item1)
    assert cart_page.is_item_in_cart(item2)

def test_forced_failure_for_artifact_capture(page: Page):
    """Intentional failure test case to demonstrate conftest failure hook capturing screenshots and traces."""
    login_page = LoginPage(page)
    login_page.navigate()
    # Intentionally fail assertion to trigger failure hook artifact generation
    assert page.title() == "Non Existent Title - Force Failure"
