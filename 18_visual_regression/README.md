# Project 18: Visual Regression Testing for Key Screens (`18_visual_regression`)

## Overview & Objectives
This subproject implements automated visual regression testing using Playwright Python (`expect(page).to_have_screenshot()`). It demonstrates how to perform baseline screenshot capture, dynamic element masking (for real-time clocks, timestamps, session tokens, and random metrics), and pixel-by-pixel drift assertion across key portal screens.

## Architecture & Server Layout
The subproject includes a dedicated FastAPI application (`server.py`) serving key enterprise screens:
- **Executive Analytics Dashboard (`/dashboard`)**: Displays system status, active user count metrics, session tokens, live clocks, and timestamp headers.
- **Payment Checkout (`/checkout`)**: Renders transaction summary with dynamic transaction reference numbers and timestamp tokens.

## Solved Test Scenarios
1. **Task 18.1: Executive Dashboard Visual Regression (`test_dashboard_visual_regression`)**
   - Navigates to `/dashboard`.
   - Defines a locator array masking dynamic UI elements (`#dynamic-timestamp`, `#session-id`, `#live-clock`, `#active-users-count`).
   - Asserts visual equality against reference baseline image `snapshots/dashboard_page.png`.
2. **Task 18.2: Payment Checkout Visual Regression (`test_checkout_visual_regression`)**
   - Navigates to `/checkout`.
   - Masks dynamic transaction elements (`#checkout-tx-id`, `#checkout-timestamp`).
   - Asserts layout pixel consistency against baseline `snapshots/checkout_page.png`.

## Test Execution Commands

- **Generate/Update Reference Baseline Snapshots (Task 18.1)**:
  ```bash
  uv run pytest 18_visual_regression/test_visual.py --update-snapshots
  ```
- **Execute Visual Regression Regression Suite (Task 18.2)**:
  ```bash
  uv run pytest 18_visual_regression/test_visual.py
  ```
- **Generate HTML Test Execution Report**:
  ```bash
  uv run pytest 18_visual_regression/test_visual.py --html=report.html --self-contained-html
  ```

## Key Parameter Reference & Fixtures

| Parameter / Fixture | Description |
| :--- | :--- |
| `name` | File name for baseline screenshot stored in `snapshots/` (e.g. `dashboard_page.png`). |
| `mask` | Array of Playwright `Locator` objects to draw solid mask overlays over dynamic content before screenshot capture. |
| `threshold` | Maximum allowed pixel difference ratio (default `0.2` or 20%). |
| `--update-snapshots` | Custom Pytest CLI flag to force overwrite of baseline reference images. |
| `server_url` | Module-scoped Pytest fixture that launches `server.py` on an ephemeral TCP port and polls `/health`. |
