import pytest
from playwright.sync_api import Page, expect

def test_successful_login(page: Page):
    # 1. Navigate to https://www.saucedemo.com/
    page.goto("https://www.saucedemo.com/")
    
    # 2. Fill user credentials
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    
    # 3. Click login button
    page.click("#login-button")
    
    # Assert landing URL contains /inventory.html
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_failed_login(page: Page):
    # 1. Navigate to the login page
    page.goto("https://www.saucedemo.com/")
    
    # 2. Input incorrect credentials and click login
    page.fill("#user-name", "invalid_user")
    page.fill("#password", "invalid_password")
    page.click("#login-button")
    
    # 3. Assert the visibility of the expected validation error element and text
    error_element = page.locator("[data-test='error']")
    expect(error_element).to_be_visible()
    expect(error_element).to_contain_text("Username and password do not match any user in this service")
