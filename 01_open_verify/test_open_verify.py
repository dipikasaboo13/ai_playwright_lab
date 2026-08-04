import re
from playwright.sync_api import Page, expect

def test_open_verify(page: Page):
    # Step 1: Navigate to target URL
    page.goto("https://playwright.dev/python/")

    # Step 2: Assert title contains "Playwright"
    expect(page).to_have_title(re.compile(r"Playwright"))

    # Step 3: Assert visibility of heading (h1 or primary heading containing Playwright)
    heading = page.get_by_role("heading", level=1)
    expect(heading).to_be_visible()
    expect(heading).to_contain_text("Playwright")



