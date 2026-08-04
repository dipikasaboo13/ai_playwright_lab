# Project 10: Payment Checkout Simulation (`10_payment_checkout`)

## Overview & Objectives
This project automates the end-to-end purchasing workflow on [SauceDemo](https://www.saucedemo.com/), validating checkout form inputs, price calculations, order completions, and form validation error states.

### Key Learning & Objectives:
- **E2E Shopping Flow**: Automating item additions, cart review, checkout step 1 details, checkout step 2 summary, and order finalization.
- **Subtotal & Tax Calculations Verification**: Extracting raw string prices from DOM elements, parsing floating point numeric values, and confirming `Item Total + Tax == Total`.
- **Form Error Handling**: Testing required form fields during checkout (e.g., missing postal code) and verifying error alerts.

---

## Solved Test Scenarios

1. **Successful Checkout Scenario** (`test_successful_checkout`):
   - Authenticates standard user into SauceDemo.
   - Adds multiple products ("Sauce Labs Backpack" and "Sauce Labs Bike Light") to the cart.
   - Navigates to cart and proceeds to Checkout Step One.
   - Populates First Name, Last Name, and Postal Code.
   - Verifies on Checkout Step Two that the subtotal (`Item total`), tax (`Tax`), and grand total (`Total`) math is mathematically accurate (`Item total + Tax == Total`).
   - Finalizes order and asserts landing on Checkout Complete page with "Thank you for your order!" message.

2. **Form Validation Error Scenario** (`test_missing_postal_code`):
   - Authenticates standard user, adds item to cart, and proceeds to checkout.
   - Populates First Name and Last Name while leaving Postal Code blank.
   - Clicks "Continue" and verifies the error alert `[data-test='error']` displays `"Error: Postal Code is required"`.

---

## Test Data & Parameters

| Parameter / Element | Value / Locator | Purpose |
| :--- | :--- | :--- |
| Login Username | `standard_user` | Valid test account |
| Login Password | `secret_sauce` | Valid password |
| Product 1 | `[data-test='add-to-cart-sauce-labs-backpack']` | Test item 1 |
| Product 2 | `[data-test='add-to-cart-sauce-labs-bike-light']` | Test item 2 |
| Checkout Form - First Name | `#first-name` (`Jane`) | Required form field |
| Checkout Form - Last Name | `#last-name` (`Doe`) | Required form field |
| Checkout Form - Postal Code | `#postal-code` (`90210`) | Required form field |
| Price Subtotal Locator | `.summary_subtotal_label` | Raw item total string |
| Tax Locator | `.summary_tax_label` | Calculated tax string |
| Total Locator | `.summary_total_label` | Grand total string |
| Validation Error Locator | `[data-test='error']` | Error banner selector |

---

## Command-Line Execution Instructions

Run all test cases in Project 10:
```bash
uv run pytest 10_payment_checkout/
```

Run specific test scenarios:
```bash
# Run successful checkout test
uv run pytest 10_payment_checkout/test_checkout.py -k "test_successful_checkout"

# Run form error test
uv run pytest 10_payment_checkout/test_checkout.py -k "test_missing_postal_code"
```
