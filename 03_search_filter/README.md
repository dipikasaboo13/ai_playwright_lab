# Project 3: Search and Filter Products (`03_search_filter`)

## Overview
This project contains automated test scenarios for validating product filtering functionality by category on the [Demoblaze](https://demoblaze.com/) e-commerce web application using Playwright Python.

## Objectives
- Automate category selection ("Laptops") on the catalog homepage.
- Assert that laptop category items are loaded and displayed.
- Verify that non-matching items (e.g. phones) are hidden/absent post-filtering.

## Solved Test Cases
- `test_category_filter_laptops`: Navigates to Demoblaze, clicks on the "Laptops" category menu, and asserts that laptops (e.g., "Sony vaio i5") are visible while phone items (e.g., "Samsung galaxy s6", "Nokia lumia 1520") are not visible.

## Execution Instructions

Run tests in the `03_search_filter` directory using `uv`:

```bash
uv run pytest 03_search_filter/test_search_filter.py
```

To run with browser UI visible (headed mode):
```bash
uv run pytest 03_search_filter/test_search_filter.py --headed
```

## Parameter & Selector References
- Target URL: `https://demoblaze.com/`
- Category Selector: `page.get_by_role("link", name="Laptops")`
- Expected Visible Laptop Item: `page.get_by_role("link", name="Sony vaio i5")`
- Expected Absent Phone Items: `page.get_by_role("link", name="Samsung galaxy s6")`, `page.get_by_role("link", name="Nokia lumia 1520")`
