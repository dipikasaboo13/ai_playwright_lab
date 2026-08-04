import pytest
from playwright.sync_api import Page, expect


def test_category_filter_laptops(page: Page):
    """
    Test scenario for Task 3.1: Category Filter Test Scenario
    1. Navigate to https://demoblaze.com/
    2. Click on the 'Laptops' category menu link.
    3. Verify laptop items are shown, and items like phones are absent.
    """
    # 1. Navigate to https://demoblaze.com/
    page.goto("https://demoblaze.com/")
    page.wait_for_load_state("domcontentloaded")

    # Assert initial product items are present (e.g. Samsung galaxy s6)
    expect(page.get_by_role("link", name="Samsung galaxy s6")).to_be_visible()

    # 2. Click on the "Laptops" category menu link
    page.get_by_role("link", name="Laptops").click()

    # Wait for catalog items to update/reload
    # "Sony vaio i5" or "MacBook air" are laptops on demoblaze
    expect(page.get_by_role("link", name="Sony vaio i5")).to_be_visible()

    # 3. Verify laptop items are shown, and items like phones are absent
    laptop_item = page.get_by_role("link", name="Sony vaio i5")
    expect(laptop_item).to_be_visible()

    # Verify phone items (like "Samsung galaxy s6" or "Nokia lumia 1520") are absent / not visible
    expect(page.get_by_role("link", name="Samsung galaxy s6")).not_to_be_visible()
    expect(page.get_by_role("link", name="Nokia lumia 1520")).not_to_be_visible()
