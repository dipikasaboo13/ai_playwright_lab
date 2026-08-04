# Project 17: Responsive Cross-Browser Regression Suite

## Description
Executes automated test flows across desktop engines (Chromium, Firefox, WebKit) and mobile/tablet viewports (`iPhone 13`, `Pixel 5`, `iPad Pro 11`) with automatic failure screenshot capture. Validates responsive UI elements, collapsible hamburger navigation drawers, side-cart drawers, and modal checkout workflows.

## Solved Test Cases
- **Task 17.1: Desktop Multi-Engine Execution Matrix** (`test_desktop_cross_browser_flow`):
  - Validates desktop navigation bar visibility, cart drawer interactions, modal checkout form submission, and order confirmation reference code display.
  - Executable across Chromium, Firefox, and WebKit desktop browser engines.
- **Task 17.2: Mobile & Tablet Viewport Responsive Layout Verification** (`test_mobile_viewport` & `test_tablet_viewport`):
  - Emulates mobile viewports (`iPhone 13`, `Pixel 5`) and tablet viewports (`iPad Pro 11`) using Playwright device profiles.
  - Asserts desktop navigation links hide and hamburger toggle button (`#hamburger-btn`) displays on mobile screen dimensions (< 768px).
  - Verifies hamburger menu click expands the mobile drawer navigation (`#mobile-menu`).
  - Executes touch-friendly mobile shopping cart and checkout flow.
  - Automatically captures full-page failure screenshots into `artifacts/screenshots/` if assertions fail.

## How to Run

### Run Desktop Multi-Engine Cross-Browser Suite
```bash
uv run pytest 17_responsive_cross_browser/test_responsive.py --browser=all
```

### Run Mobile Viewport Responsive Test Scenario
```bash
uv run pytest 17_responsive_cross_browser/test_responsive.py -k "test_mobile_viewport"
```

### Run Entire Subproject Suite with HTML Report Generation
```bash
uv run pytest 17_responsive_cross_browser/ --html=report.html --self-contained-html
```

## Parameter & Variable Reference

| Parameter | Description |
|-----------|-------------|
| `target_url` | Web page URL tested across browser engines and screen viewports (`server_url` fixture). |
| `device_profiles` | Playwright pre-configured device descriptors (`iPhone 13`, `Pixel 5`, `iPad Pro 11`). |
| `screenshot_dir` | Output directory (`artifacts/screenshots/`) where failure snapshots are saved. |
| `desktop_breakpoint` | Responsive layout breakpoint configured at `768px` in CSS media queries. |
