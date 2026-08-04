# 01_open_verify: Open and Verify Webpage

## Description & Objectives
This subproject demonstrates basic web page navigation and structural assertions using Playwright with Python and `pytest`.

## Solved Test Scenarios
- **Page Title Assertion**: Verifies that navigating to `https://playwright.dev/python/` returns a page title containing "Playwright".
- **Primary Heading Verification**: Asserts that the primary (`h1`) heading element on the page is visible and contains expected text.

## Test Execution Commands

Run all tests in this subproject:
```bash
uv run pytest 01_open_verify/
```

Run specific test file:
```bash
uv run pytest 01_open_verify/test_open_verify.py
```

## Parameter Reference & Test Data
- **Target URL**: `https://playwright.dev/python/`
- **Expected Page Title Match**: Regex matching `Playwright`
- **Target Heading Locator**: `page.get_by_role("heading", level=1)`
