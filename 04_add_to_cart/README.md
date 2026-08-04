# Project 4: Add Product to Cart (`04_add_to_cart`)

## Overview
This subproject automates adding products to the shopping cart, handling browser native dialog alerts (`"Product added"`), verifying item lists within the cart UI, and asserting accurate subtotal price calculations before and after deleting products on [Demoblaze](https://demoblaze.com/).

## Objectives
- Automate multi-product selection and handle web native alert dialogs during cart insertion.
- Verify presence of selected products inside the cart item table.
- Calculate price differences upon item removal and assert that subtotal updates dynamically.

## Solved Test Cases
- `test_add_to_cart_and_verify_subtotal`:
  1. Navigates to Demoblaze and selects "Samsung galaxy s6" (Product A).
  2. Handles alert dialog on "Add to cart" click.
  3. Navigates back home and selects "Nokia lumia 1520" (Product B).
  4. Handles alert dialog on "Add to cart" click.
  5. Opens the Cart page and verifies both products are visible in the cart table.
  6. Evaluates total price before and after deleting Product A.
  7. Asserts that the new total is reduced by Product A's exact price.

## Execution Instructions

Run tests in the `04_add_to_cart` directory using `uv`:

```bash
uv run pytest 04_add_to_cart/test_cart.py
```

To run with browser UI visible (headed mode):
```bash
uv run pytest 04_add_to_cart/test_cart.py --headed
```

## Parameter & Selector References
- Target URL: `https://demoblaze.com/`
- Products Tested: `Samsung galaxy s6`, `Nokia lumia 1520`
- Cart Link: `page.get_by_role("link", name="Cart", exact=True)`
- Cart Table Rows: `#tbodyid tr`
- Total Price Selector: `#totalp`
- Dialog Handling: `page.once("dialog", handler)`
