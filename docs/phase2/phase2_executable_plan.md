# Executable Implementation Plan: Playwright Python Lab - Phase 2

This document breaks down the Phase 2 development process into atomic, independent, and verifiable tasks. Each task defines clear deliverables, step-by-step instructions, and an independent verification method.

---

## Workspace & Core Tooling Tasks

### Task 0: Phase 2 Environment & Dependency Setup
* **Objective**: Verify Python virtual environment, extend dependencies for Phase 2 HTML reporting, and validate browser runtimes.
* **Steps**:
  1. Verify the project-level Python setup managed by `uv`.
  2. Install Phase 2 dependencies:
     ```bash
     uv add pytest-html
     ```
  3. Ensure Playwright browser binaries are installed:
     ```bash
     uv run playwright install
     ```
* **Validation**:
  ```bash
  uv run pytest --version
  uv run playwright --version
  ```

---

## Subproject Tasks

### Project 11: Role-Based Employee Management Portal (`11_role_based_portal`)
* **Task 11.1: Admin User Management & Account Disabling Test Scenario**
  * **Objective**: Write test script steps for admin creation of employee profiles and status toggling to `Disabled`.
  * **Steps**:
    1. Navigate to portal admin management page.
    2. Log in with admin credentials (`admin_creds`).
    3. Fill employee creation form, assign role `Sales Specialist`, and submit.
    4. Update status to `Disabled` and assert table record reflects `Disabled`.
  * **Validation**:
    ```bash
    uv run pytest 11_role_based_portal/test_role_portal.py -k "test_admin_disable_user"
    ```
* **Task 11.2: Multi-Context Role & Permission Verification Test Scenario**
  * **Objective**: Test employee login using an isolated browser context and verify menu restrictions.
  * **Steps**:
    1. Create an isolated `BrowserContext` for the employee session.
    2. Log in with employee credentials.
    3. Assert visibility of role-permitted navigation tabs.
    4. Assert absence/disablement of admin-restricted action buttons.
  * **Validation**:
    ```bash
    uv run pytest 11_role_based_portal/test_role_portal.py -k "test_employee_permissions"
    ```
* **Task 11.3: Project Documentation**
  * **Objective**: Create `11_role_based_portal/README.md`.
  * **Validation**: Confirm file exists and details description, solved test cases, execution instructions, and parameter references.

---

### Project 12: End-to-End Travel Booking Flow (`12_travel_booking`)
* **Task 12.1: Successful Travel Search & Booking Test Scenario**
  * **Objective**: Automate multi-step flight/hotel search, date selection, passenger form completion, and booking confirmation.
  * **Steps**:
    1. Navigate to booking portal and select origin/destination locations.
    2. Pick travel dates from interactive calendar picker widget.
    3. Apply price and rating filters to narrow search results.
    4. Fill passenger information form and submit booking.
    5. Assert confirmation reference code and total price calculation.
  * **Validation**:
    ```bash
    uv run pytest 12_travel_booking/test_travel_booking.py -k "test_successful_booking"
    ```
* **Task 12.2: Form Validation & Dynamic Price Change Test Scenario**
  * **Objective**: Validate handling for invalid dates, missing form input, and price change alerts.
  * **Steps**:
    1. Attempt search with invalid date ranges and verify warning alert banner.
    2. Submit passenger form with missing required fields and assert inline validation messages.
  * **Validation**:
    ```bash
    uv run pytest 12_travel_booking/test_travel_booking.py -k "test_booking_validations"
    ```
* **Task 12.3: Project Documentation**
  * **Objective**: Create `12_travel_booking/README.md`.
  * **Validation**: Confirm file exists with parameter reference table.

---

### Project 13: Order Management with API Setup (`13_order_management_api`)
* **Task 13.1: API Test Data Seeding Setup**
  * **Objective**: Use Playwright `APIRequestContext` to create customer and order records.
  * **Steps**:
    1. Send HTTP POST request to `/api/v1/orders` with customer payload.
    2. Save returned `order_id` in test state.
  * **Validation**: Confirm HTTP response status code is 201/200 and JSON response contains valid `order_id`.
* **Task 13.2: UI Search & Status Update with API Cross-Validation**
  * **Objective**: Locate seeded order in UI, update status to `Shipped`, verify via GET API request, and teardown via DELETE API.
  * **Steps**:
    1. Log into UI dashboard and search for `order_id`.
    2. Click status dropdown and select `Shipped`.
    3. Issue GET API request to verify status backend value is `Shipped`.
    4. Issue DELETE API request to clean up seeded test record.
  * **Validation**:
    ```bash
    uv run pytest 13_order_management_api/test_order_mgmt.py
    ```
* **Task 13.3: Project Documentation**
  * **Objective**: Create `13_order_management_api/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 14: Webhook and Notification Validation (`14_webhook_notification`)
* **Task 14.1: UI Trigger & Webhook Event Interception**
  * **Objective**: Trigger UI action and intercept outbound HTTP POST webhook event.
  * **Steps**:
    1. Submit order or form action on web page.
    2. Intercept outbound network request or poll webhook receiver endpoint.
    3. Assert event payload contains expected keys (`event_type`, `timestamp`, `data`).
  * **Validation**:
    ```bash
    uv run pytest 14_webhook_notification/test_webhook_notification.py -k "test_webhook_payload"
    ```
* **Task 14.2: Real-Time In-App Toast Notification Assertion**
  * **Objective**: Verify UI toast notification message.
  * **Steps**: Assert real-time toast alert is visible on DOM with expected text string.
  * **Validation**:
    ```bash
    uv run pytest 14_webhook_notification/test_webhook_notification.py -k "test_ui_notification"
    ```
* **Task 14.3: Project Documentation**
  * **Objective**: Create `14_webhook_notification/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 15: Multi-File Import and Error Report Validation (`15_file_import_reports`)
* **Task 15.1: Create Test Dataset Files**
  * **Objective**: Create sample files for clean and corrupted file import testing.
  * **Steps**:
    1. Create `valid_records.csv` containing valid rows.
    2. Create `invalid_records.csv` containing malformed rows and duplicate keys.
  * **Validation**: Verify files exist in subproject directory.
* **Task 15.2: Clean File Import Verification Test Scenario**
  * **Objective**: Upload valid file and assert successful processing banner.
  * **Steps**: Upload `valid_records.csv` via input element and assert success summary counter.
  * **Validation**:
    ```bash
    uv run pytest 15_file_import_reports/test_file_import.py -k "test_valid_import"
    ```
* **Task 15.3: Corrupted File Import & Downloadable Error Report Parsing**
  * **Objective**: Upload invalid CSV, verify failure count, trigger report download, and parse downloaded error file.
  * **Steps**:
    1. Upload `invalid_records.csv`.
    2. Assert row-level error breakdown table.
    3. Capture download via `page.expect_download()` and save to disk.
    4. Parse saved file content to verify error message strings per row.
  * **Validation**:
    ```bash
    uv run pytest 15_file_import_reports/test_file_import.py -k "test_invalid_import_report"
    ```
* **Task 15.4: Project Documentation**
  * **Objective**: Create `15_file_import_reports/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 16: Mock External Dependency Failures (`16_mock_dependency_failures`)
* **Task 16.1: Intercept & Mock Payment Gateway HTTP 500 & Timeout Failures**
  * **Objective**: Mock API route to simulate server failure and assert error banner.
  * **Steps**:
    1. Set up route interception using `page.route("**/api/payment", handler)`.
    2. Fulfill route with status HTTP 500 or abort request.
    3. Trigger checkout action and assert UI error alert display.
  * **Validation**:
    ```bash
    uv run pytest 16_mock_dependency_failures/test_mock_failures.py -k "test_mock_server_error"
    ```
* **Task 16.2: Mock Response Delay & Partial Data Resilience Testing**
  * **Objective**: Inject artificial network delay (5000ms) and partial JSON responses to test UI spinners and resilience.
  * **Steps**:
    1. Fulfill route with artificial delay and partial JSON data.
    2. Assert loading indicators appear during pending state and fallback view triggers gracefully.
  * **Validation**:
    ```bash
    uv run pytest 16_mock_dependency_failures/test_mock_failures.py -k "test_mock_delay_resilience"
    ```
* **Task 16.3: Project Documentation**
  * **Objective**: Create `16_mock_dependency_failures/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 17: Responsive Cross-Browser Regression Suite (`17_responsive_cross_browser`)
* **Task 17.1: Desktop Multi-Engine Execution Matrix**
  * **Objective**: Run user flows across Chromium, Firefox, and WebKit desktop browsers.
  * **Steps**: Execute core test script configuring browser engines.
  * **Validation**:
    ```bash
    uv run pytest 17_responsive_cross_browser/test_responsive.py --browser=all
    ```
* **Task 17.2: Mobile & Tablet Viewport Responsive Layout Verification**
  * **Objective**: Test responsive layouts on simulated mobile viewports (`iPhone 13`, `Pixel 5`).
  * **Steps**:
    1. Initialize page with mobile viewport dimensions and user agent.
    2. Click hamburger navigation menu and assert menu drawer expands correctly.
    3. Save failure screenshots automatically if assertions fail.
  * **Validation**:
    ```bash
    uv run pytest 17_responsive_cross_browser/test_responsive.py -k "test_mobile_viewport"
    ```
* **Task 17.3: Project Documentation**
  * **Objective**: Create `17_responsive_cross_browser/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 18: Visual Regression Testing for Key Screens (`18_visual_regression`)
* **Task 18.1: Baseline Screenshot Generation with Dynamic Element Masking**
  * **Objective**: Generate baseline snapshots for key screens masking dynamic timestamps and session tags.
  * **Steps**:
    1. Navigate to target screen (e.g. Dashboard/Checkout).
    2. Pass array of dynamic element locators to `mask` option in `expect(page).to_have_screenshot()`.
    3. Run with `--update-snapshots` flag to store baseline images in `snapshots/`.
  * **Validation**: Confirm baseline PNG files are saved in `snapshots/` folder.
* **Task 18.2: Visual Drift Assertion & Snapshot Update Workflow**
  * **Objective**: Assert visual regression against reference baselines.
  * **Steps**: Run visual test suite without update flag and verify zero pixel diff failures.
  * **Validation**:
    ```bash
    uv run pytest 18_visual_regression/test_visual.py
    ```
* **Task 18.3: Project Documentation**
  * **Objective**: Create `18_visual_regression/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 19: Payment Transaction Lifecycle Simulation (`19_payment_lifecycle`)
* **Task 19.1: End-to-End Payment Authorization & Settlement Lifecycle**
  * **Objective**: Walk transaction through Initiate -> Authorize -> Pending -> Complete state machine.
  * **Steps**:
    1. Initiate payment charge via UI form.
    2. Transition payment status state.
    3. Assert account ledger balance math updates and transaction table status shows `Completed`.
  * **Validation**:
    ```bash
    uv run pytest 19_payment_lifecycle/test_payment_lifecycle.py -k "test_payment_completion"
    ```
* **Task 19.2: Transaction Reversal & Refund Ledger Math Verification**
  * **Objective**: Initiate full/partial refund and verify ledger deduction.
  * **Steps**:
    1. Click refund button for completed transaction.
    2. Assert updated balance and status change to `Refunded`.
  * **Validation**:
    ```bash
    uv run pytest 19_payment_lifecycle/test_payment_lifecycle.py -k "test_payment_refund"
    ```
* **Task 19.3: Project Documentation**
  * **Objective**: Create `19_payment_lifecycle/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 20: AI-Assisted Test Automation Framework (`20_ai_assisted_framework`)
* **Task 20.1: Build Page Object Model & Centralized Configuration**
  * **Objective**: Construct modular POM page classes (`base_page.py`, `login_page.py`, `checkout_page.py`, `dashboard_page.py`).
  * **Steps**: Implement Page Object patterns encapsulating locators and reusable action methods.
  * **Validation**: Verify POM classes import cleanly and expose method interfaces.
* **Task 20.2: AI-Generated Dataset Integration**
  * **Objective**: Create static AI-generated test data matrix file `data/ai_generated_dataset.json`.
  * **Steps**: Populate JSON file with test variations (`positive`, `negative`, `boundary`, `exception`).
  * **Validation**: Confirm file is valid JSON and loadable via Pytest.
* **Task 20.3: Pytest Hooks, Tracing, & HTML Report Generation**
  * **Objective**: Setup `conftest.py` failure screenshot capture, zip traces, and HTML report output.
  * **Steps**: Configure Pytest hooks to automatically attach artifacts on failure and format HTML reports.
  * **Validation**: Run test suite generating `report.html` file.
* **Task 20.4: Tagged Test Suite Execution**
  * **Objective**: Execute tagged smoke suite and parameterized regression suite.
  * **Validation**:
    ```bash
    uv run pytest 20_ai_assisted_framework/tests/ --html=report.html --self-contained-html -m smoke
    ```
* **Task 20.5: Project Documentation**
  * **Objective**: Create `20_ai_assisted_framework/README.md`.
  * **Validation**: Confirm file exists with architecture breakdown and run instructions.
