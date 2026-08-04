import pytest
from playwright.sync_api import Page, Playwright, expect


def test_api_query_setup(playwright: Playwright):
    """
    Task 6.1: API Query Setup
    - Objective: Trigger request to Demoblaze catalog API.
    - Steps: Retrieve data from https://api.demoblaze.com/entries and save to an in-memory dictionary.
    - Validation: Confirm response code is 200 and parses successfully into dictionary structure.
    """
    request_context = playwright.request.new_context()
    
    # Send GET request to Demoblaze catalog API endpoint
    response = request_context.get("https://api.demoblaze.com/entries")
    
    # Assert response status code is 200 OK
    assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
    
    json_data = response.json()
    assert "Items" in json_data, "Response JSON does not contain expected 'Items' key"
    
    # Parse API response items into in-memory dictionary
    catalog_dict = {}
    for item in json_data["Items"]:
        clean_title = item["title"].strip()
        catalog_dict[clean_title] = float(item["price"])
        
    assert len(catalog_dict) > 0, "Catalog dictionary should contain at least 1 product item"
    
    # Cleanup request context
    request_context.dispose()


def test_frontend_matching_assertions(page: Page, playwright: Playwright):
    """
    Task 6.2: Frontend Matching Assertions
    - Objective: Cross-reference API payloads against frontend DOM elements.
    - Steps: Launch browser, load catalog homepage, and assert elements have matching titles/prices.
    """
    # 1. Retrieve catalog data from API
    request_context = playwright.request.new_context()
    response = request_context.get("https://api.demoblaze.com/entries")
    assert response.status == 200, f"API query failed with status code {response.status}"
    
    api_items = response.json().get("Items", [])
    assert len(api_items) > 0, "API returned empty product list"
    
    # Build lookup map of API products
    api_catalog = {item["title"].strip(): float(item["price"]) for item in api_items}
    request_context.dispose()

    # 2. Navigate to frontend catalog homepage
    page.goto("https://demoblaze.com/")
    page.wait_for_load_state("domcontentloaded")

    # Wait for product card elements to render on UI
    page.wait_for_selector(".card")

    # Locate all product card elements
    cards = page.locator(".card")
    card_count = cards.count()
    assert card_count > 0, "No product cards were found on the UI catalog page"

    # 3. Iterate through DOM product cards and validate against API catalog payload
    for i in range(card_count):
        card = cards.nth(i)
        
        # Extract title from UI card link
        title_element = card.locator(".card-title a")
        expect(title_element).to_be_visible()
        ui_title = title_element.text_content().strip()
        
        # Extract price string from UI card (format e.g., "$360")
        price_element = card.locator("h5")
        expect(price_element).to_be_visible()
        ui_price_str = price_element.text_content().strip()
        
        # Convert "$360" string to numeric float value 360.0
        ui_price = float(ui_price_str.replace("$", "").replace(",", "").strip())
        
        # Assert item title exists in API data payload
        assert ui_title in api_catalog, f"Product '{ui_title}' displayed on UI was not present in API entries payload"
        
        # Assert price on UI matches API price payload
        expected_api_price = api_catalog[ui_title]
        assert ui_price == expected_api_price, (
            f"Price mismatch for '{ui_title}': UI displays ${ui_price}, but API payload specifies ${expected_api_price}"
        )
