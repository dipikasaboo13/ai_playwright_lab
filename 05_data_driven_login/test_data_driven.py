import json
import re
from pathlib import Path
import pytest
from playwright.sync_api import Page, expect

# Load credentials dataset from JSON
CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
    test_credentials = json.load(f)

@pytest.mark.parametrize("cred", test_credentials, ids=[c["username"] for c in test_credentials])
def test_data_driven_login(page: Page, cred: dict):
    """
    Data-driven login test scenario covering standard, locked out, and invalid user login flows.
    """
    page.goto("https://www.saucedemo.com/")
    
    # Fill in credentials
    page.fill("#user-name", cred["username"])
    page.fill("#password", cred["password"])
    page.click("#login-button")
    
    if cred["should_succeed"]:
        # Verify successful login redirection
        expect(page).to_have_url(re.compile(re.escape(cred["expected_url_substring"])))
        expect(page.locator(".title")).to_have_text("Products")
    else:
        # Verify validation error display
        error_locator = page.locator("[data-test='error']")
        expect(error_locator).to_be_visible()
        expect(error_locator).to_contain_text(cred["expected_error"])

