# Implementation Plan: Playwright Python Lab - Phase 2

This document defines the step-by-step implementation roadmap for completing Phase 2 (Projects 11 to 20) of the Playwright Python Lab.

---

## Phase 1: Environment Initialization & Setup

### Task 1.1: Dependency Verification & Extension
- Verify the `uv` virtual environment and dependency set.
- Add required reporting tools:
  ```bash
  uv add pytest-html
  ```
- Ensure Playwright browser runtimes are available:
  ```bash
  uv run playwright install
  ```

### Task 1.2: Directory Layout Setup
- Create subproject directories (`11_role_based_portal/` through `20_ai_assisted_framework/`).

---

## Phase 2: Sequential Subproject Execution

Each Phase 2 project will adhere to the standard vibe-coding workflow cycle:
1. **Directory Setup**: Create subproject folder and necessary asset sub-folders.
2. **Test Implementation**: Write automated test files with clear, comprehensive code comments.
3. **Execution & Debugging**: Run tests using `uv run pytest <project_folder>/`.
4. **Subproject Documentation**: Write a detailed `README.md` covering description, solved test cases, run commands, and parameter tables.

---

### Project 11: Role-Based Employee Management Portal (`11_role_based_portal`)
- **Step 1**: Create directory `11_role_based_portal/`.
- **Step 2**: Implement `test_role_portal.py` covering:
  - Admin login, user creation, role assignment (`Sales Specialist`), and setting account state to `Disabled`.
  - Multi-context browser isolation testing for role permissions and restricted navigation elements.
- **Step 3**: Execute: `uv run pytest 11_role_based_portal/`
- **Step 4**: Create `11_role_based_portal/README.md`.

---

### Project 12: End-to-End Travel Booking Flow (`12_travel_booking`)
- **Step 1**: Create directory `12_travel_booking/`.
- **Step 2**: Implement `test_travel_booking.py` covering:
  - Flight/hotel search, date selection in calendar widget, price/rating filtering, multi-passenger form submission, and booking confirmation.
  - Validation handling for unavailable dates, empty input fields, and dynamic price adjustments.
- **Step 3**: Execute: `uv run pytest 12_travel_booking/`
- **Step 4**: Create `12_travel_booking/README.md`.

---

### Project 13: Order Management with API Setup (`13_order_management_api`)
- **Step 1**: Create directory `13_order_management_api/`.
- **Step 2**: Implement `test_order_mgmt.py` covering:
  - Pre-test API data seeding (`POST /api/orders`) via `APIRequestContext`.
  - UI search for seeded order, status update to `Shipped`.
  - Backend status verification via GET API and pre-teardown deletion via DELETE API.
- **Step 3**: Execute: `uv run pytest 13_order_management_api/`
- **Step 4**: Create `13_order_management_api/README.md`.

---

### Project 14: Webhook and Notification Validation (`14_webhook_notification`)
- **Step 1**: Create directory `14_webhook_notification/`.
- **Step 2**: Implement `test_webhook_notification.py` covering:
  - Triggering UI action, intercepting outbound HTTP POST events, and validating payload JSON keys.
  - Asserting visibility and text of real-time in-app toast notification elements.
- **Step 3**: Execute: `uv run pytest 14_webhook_notification/`
- **Step 4**: Create `14_webhook_notification/README.md`.

---

### Project 15: Multi-File Import and Error Report Validation (`15_file_import_reports`)
- **Step 1**: Create directory `15_file_import_reports/`.
- **Step 2**: Add sample dataset files: `valid_records.csv` and `invalid_records.csv`.
- **Step 3**: Implement `test_file_import.py` covering:
  - Clean CSV upload and table record verification.
  - Malformed CSV upload, row error counter verification, downloading error report via `page.expect_download()`, and parsing report content.
- **Step 4**: Execute: `uv run pytest 15_file_import_reports/`
- **Step 5**: Create `15_file_import_reports/README.md`.

---

### Project 16: Mock External Dependency Failures (`16_mock_dependency_failures`)
- **Step 1**: Create directory `16_mock_dependency_failures/`.
- **Step 2**: Implement `test_mock_failures.py` covering:
  - Route interception (`page.route()`) returning HTTP 500 error / network timeout, and verifying error banner display.
  - Route delay injection (5000ms latency) and partial payload handling to verify loading spinners and timeout resilience.
- **Step 3**: Execute: `uv run pytest 16_mock_dependency_failures/`
- **Step 4**: Create `16_mock_dependency_failures/README.md`.

---

### Project 17: Responsive Cross-Browser Regression Suite (`17_responsive_cross_browser`)
- **Step 1**: Create directory `17_responsive_cross_browser/`.
- **Step 2**: Implement `test_responsive.py` covering:
  - Executing user flows across desktop engines (Chromium, Firefox, WebKit) and mobile viewports (`iPhone 13`, `Pixel 5`).
  - Verifying touch-friendly hamburger menus and responsive UI elements.
- **Step 3**: Execute: `uv run pytest 17_responsive_cross_browser/ --browser=all`
- **Step 4**: Create `17_responsive_cross_browser/README.md`.

---

### Project 18: Visual Regression Testing for Key Screens (`18_visual_regression`)
- **Step 1**: Create directory `18_visual_regression/` and `snapshots/` folder.
- **Step 2**: Implement `test_visual.py` covering:
  - Masking dynamic elements (timestamps, user badges, IDs) with locator arrays.
  - Visual assertion using `expect(page).to_have_screenshot()` and baseline snapshot management.
- **Step 3**: Execute: `uv run pytest 18_visual_regression/ --update-snapshots`
- **Step 4**: Create `18_visual_regression/README.md`.

---

### Project 19: Payment Transaction Lifecycle Simulation (`19_payment_lifecycle`)
- **Step 1**: Create directory `19_payment_lifecycle/`.
- **Step 2**: Implement `test_payment_lifecycle.py` covering:
  - State transitions: Initiate -> Authorize -> Pending -> Completed -> Refunded.
  - Asserting balance ledger math, API response states, and transaction status logs.
- **Step 3**: Execute: `uv run pytest 19_payment_lifecycle/`
- **Step 4**: Create `19_payment_lifecycle/README.md`.

---

### Project 20: AI-Assisted Test Automation Framework (`20_ai_assisted_framework`)
- **Step 1**: Create directory `20_ai_assisted_framework/` with sub-folders `pages/`, `data/`, and `tests/`.
- **Step 2**: Create `data/ai_generated_dataset.json` with AI-generated test variations (`positive`, `negative`, `boundary`, `exception`).
- **Step 3**: Build POM classes (`base_page.py`, `login_page.py`, `checkout_page.py`, `dashboard_page.py`) and setup `conftest.py` hooks.
- **Step 4**: Implement `tests/test_ai_framework.py` with `@pytest.mark.smoke` tagging and parameterized data execution.
- **Step 5**: Execute: `uv run pytest 20_ai_assisted_framework/tests/ --html=report.html --self-contained-html -m smoke`
- **Step 6**: Create `20_ai_assisted_framework/README.md`.

---

## Phase 3: Final Integration & Verification
- Execute full Phase 2 test suite using `uv run pytest`.
- Verify every subproject folder contains its dedicated `README.md` and thoroughly commented source files.
