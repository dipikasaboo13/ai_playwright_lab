# Requirements Specification: Playwright Python Lab - Phase 2

This document defines the requirements, tooling, project structure, and detailed specifications for Projects 11 to 20 in Phase 2 of the Playwright Python Lab.

---

## 1. Technical Stack & Tooling

The projects in Phase 2 are implemented using **Python** and **uv** (an extremely fast Python package and project manager). 

### Prerequisites
- Python 3.10 or higher
- `uv` command-line tool

### Workspace Setup Guidelines
Each subproject should run within a virtual environment managed by `uv`. The general dependency stack includes:
- `pytest` - Test runner framework
- `pytest-playwright` - Playwright integration plugin for Pytest
- `playwright` - Core browser automation library
- `pytest-html` - HTML test report generation (used for advanced frameworks)
- `pillow` / `opencv-python` - Image processing tools for advanced visual snapshot handling (if needed)

To set up the workspace, developers will use:
```bash
# Initialize Python project using uv (if not already done)
uv init

# Add required dependencies
uv add pytest pytest-playwright pytest-html

# Install Playwright browser binaries
uv run playwright install
```

---

## 2. General Subproject Requirements

To ensure consistency, readability, and ease of learning, every subproject directory must adhere to the following rules:

### A. Dedicated `README.md` File
Each subproject directory (e.g., `11_role_based_portal/`) must contain a dedicated `README.md` with:
1. **Project Description**: A clear summary of what the project is doing and why.
2. **Test Cases Solved**: A structured list of test scenarios covered in the project.
3. **Execution Instructions**: The exact command(s) to run the tests using `uv run pytest`.
4. **Parameter Dictionary**: A detailed breakdown of every parameter, variable, fixture, or credential used in the test scripts and what they do.

### B. Comprehensive Code Commenting
All code files must be heavily documented with comments explaining:
- The purpose of specific fixtures (e.g., `page`, `browser`, `browser_context`, custom fixtures).
- The intent behind complex locators, routes, and action APIs (`page.route`, `context.new_page`, `page.expect_download`, `page.expect_event`, etc.).
- The assertion logic and expected UI/API states.
- Error handling, timeouts, retries, and network mocks.

---

## 3. Subproject Specifications

Below are the detailed requirements and test cases for Phase 2 subprojects (Projects 11 to 20).

---

### Project 11: Role-Based Employee Management Portal (`11_role_based_portal`)
* **Goal**: Automate role-based access control (RBAC), multi-user permissions, and account lifecycle management using isolated browser contexts.
* **Target Webpage**: Role-Based Admin & Employee Portal (FastAPI or Web Application)
* **Test Cases**:
  * **Test Case 1 (Admin User Management & Account Disabling)**:
    1. Log in as an Administrator.
    2. Create a new employee record and assign a specific role (e.g., `Sales Specialist`).
    3. Update the account status to `Disabled`.
    4. Assert that the employee status reflects `Disabled` in the user registry table.
  * **Test Case 2 (Employee Role & Permission Verification)**:
    1. Create a isolated browser context (`Employee` context).
    2. Attempt to log in with the created employee credentials.
    3. Verify available vs. restricted menus, navigation tabs, and action buttons based on permissions.
* **Execution Command**:
  ```bash
  uv run pytest 11_role_based_portal/test_role_portal.py
  ```
* **Required Parameters & Variables**:
  * `admin_creds`: Credentials for the administrator user.
  * `employee_creds`: Credentials for the newly created employee user.
  * `assigned_role`: Role string assigned during creation (`Sales Specialist`).
  * `account_status`: Account state (`Active` / `Disabled`).
  * `expected_allowed_menus`: List of UI elements/menus accessible to the role.
  * `expected_restricted_menus`: List of UI elements/menus hidden or disabled.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 11: Role-Based Employee Management Portal
  
  ## Description
  Tests role-based permission verification, multi-context browser isolation, and user account status lifecycle.
  
  ## Test Cases Solved
  - Admin creation of employee account, role assignment, and disabling.
  - Verification of role-specific UI menus and restricted action enforcement in isolated browser sessions.
  
  ## How to Run
  ```bash
  uv run pytest 11_role_based_portal/test_role_portal.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `admin_creds` | Administrative credentials for portal management. |
  | `employee_creds` | Account credentials for role test user. |
  | `assigned_role` | Permission role applied to the employee profile. |
  | `account_status` | Account state (Active/Disabled). |
  | `expected_allowed_menus` | List of navigation items expected for the assigned role. |
  | `expected_restricted_menus` | List of navigation items blocked for the assigned role. |
  ```

---

### Project 12: End-to-End Travel Booking Flow (`12_travel_booking`)
* **Goal**: Validate complex multi-step search, date pickers, dynamic pricing updates, passenger input validation, and exception handling.
* **Target Webpage**: Travel & Hotel Booking Application
* **Test Cases**:
  * **Test Case 1 (Successful Travel Booking)**:
    1. Navigate to the Travel Booking application.
    2. Search flights/hotels by origin, destination, and calendar date range.
    3. Filter results by price and rating criteria.
    4. Input multi-passenger traveller details and submit booking.
    5. Verify booking confirmation reference number and invoice total.
  * **Test Case 2 (Validation & Price Change Handling)**:
    1. Select unavailable or invalid date ranges and assert error validation banners.
    2. Leave required passenger fields blank and verify inline form validation.
    3. Handle dynamic price update alerts during reservation lock.
* **Execution Command**:
  ```bash
  uv run pytest 12_travel_booking/test_travel_booking.py
  ```
* **Required Parameters & Variables**:
  * `booking_url`: Target travel application URL.
  * `origin` / `destination`: Travel location strings.
  * `departure_date` / `return_date`: Target travel dates for calendar widget.
  * `passenger_list`: Array of passenger dictionaries (name, passport/ID, contact).
  * `expected_booking_status`: Expected final status (`Confirmed`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 12: End-to-End Travel Booking Flow
  
  ## Description
  Automates travel search, dynamic pricing assertion, date picker interactions, and multi-passenger input validation.
  
  ## Test Cases Solved
  - Complete flight/hotel search, date selection, filtering, and booking confirmation.
  - Validation handling for unavailable dates, incomplete form fields, and dynamic price adjustments.
  
  ## How to Run
  ```bash
  uv run pytest 12_travel_booking/test_travel_booking.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `booking_url` | Travel application portal URL. |
  | `origin` | Departure city/airport code. |
  | `destination` | Arrival city/airport code. |
  | `departure_date` | Date string selected in calendar widget. |
  | `passenger_list` | Collection of passenger details submitted for booking. |
  ```

---

### Project 13: Order Management with API Setup (`13_order_management_api`)
* **Goal**: Implement hybrid API/UI test patterns by seeding data via HTTP REST endpoints, executing UI workflows, and cross-validating via API.
* **Target Resources**:
  - API: REST Order Endpoints (`/api/v1/orders`, `/api/v1/customers`)
  - UI Webpage: Order Management Dashboard
* **Test Case Description**:
  1. Send an HTTP POST API request using Playwright's `request` context to create customer and order records.
  2. Log into the UI dashboard and search for the newly seeded order ID.
  3. Update order status from `Pending` to `Shipped` via UI actions.
  4. Perform an HTTP GET API request to verify the order status reflects `Shipped` in the database backend.
  5. Cleanup seeded test data via an HTTP DELETE API endpoint.
* **Execution Command**:
  ```bash
  uv run pytest 13_order_management_api/test_order_mgmt.py
  ```
* **Required Parameters & Variables**:
  * `api_base_url`: Endpoint for REST API requests.
  * `ui_url`: Frontend application web URL.
  * `order_payload`: JSON dict payload used for order creation API.
  * `updated_status`: Target status applied via UI (`Shipped`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 13: Order Management with API Setup
  
  ## Description
  Combines API-based test data seeding and cleanup with UI verification and state update testing.
  
  ## Test Cases Solved
  - Seeding customer and order records via REST API.
  - Searching and updating order lifecycle state in the UI.
  - Cross-validating updated state via GET API requests and cleaning up via DELETE API.
  
  ## How to Run
  ```bash
  uv run pytest 13_order_management_api/test_order_mgmt.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `api_base_url` | Base URL for REST API endpoints. |
  | `ui_url` | Web dashboard URL. |
  | `order_payload` | Test dataset sent via API to seed order. |
  | `updated_status` | Status string verified after UI update. |
  ```

---

### Project 14: Webhook and Notification Validation (`14_webhook_notification`)
* **Goal**: Validate asynchronous event-driven architectures, network request interception, polling/retry logic, and in-app notification toasts.
* **Target Webpage**: Event-driven Web Application with Webhook Service
* **Test Case Description**:
  1. Trigger an action in the UI (e.g., submitting a request or placing an order).
  2. Intercept outbound network requests or poll webhook listener endpoints to confirm event dispatch.
  3. Validate the structure and payload fields of the dispatched webhook JSON event.
  4. Assert the presence and text of the real-time notification toast in the UI.
* **Execution Command**:
  ```bash
  uv run pytest 14_webhook_notification/test_webhook_notification.py
  ```
* **Required Parameters & Variables**:
  * `app_url`: Application URL under test.
  * `webhook_listener_url`: Internal endpoint receiving triggered event payloads.
  * `expected_event_type`: Event name identifier (e.g., `order.created`).
  * `expected_notification_msg`: UI toast message string.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 14: Webhook and Notification Validation
  
  ## Description
  Intercepts network events and verifies asynchronous webhook delivery alongside real-time UI notification alerts.
  
  ## Test Cases Solved
  - UI action triggering outbound event generation.
  - Webhook payload structure and field validation.
  - In-app toast notification verification.
  
  ## How to Run
  ```bash
  uv run pytest 14_webhook_notification/test_webhook_notification.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `app_url` | Target application URL. |
  | `webhook_listener_url` | Target URL for captured webhook payloads. |
  | `expected_event_type` | Event name expected in the webhook payload. |
  | `expected_notification_msg` | Toast message string to verify on screen. |
  ```

---

### Project 15: Multi-File Import and Error Report Validation (`15_file_import_reports`)
* **Goal**: Process bulk batch file uploads (CSV/Excel), validate row-level database imports, and parse downloadable error log files.
* **Target Webpage**: Batch Import & Data Processing Portal
* **Test Cases**:
  * **Test Case 1 (Valid File Import)**:
    1. Upload a structured valid CSV file (`valid_records.csv`).
    2. Assert success summary banner and verify records present in UI data grid.
  * **Test Case 2 (Invalid File & Downloadable Error Report)**:
    1. Upload an invalid file (`invalid_records.csv`) containing malformed rows and duplicates.
    2. Verify row-level failure counters displayed in UI.
    3. Trigger download of error report file via `page.expect_download()`.
    4. Save and parse downloadable report file content, asserting exact failure details per row.
* **Execution Command**:
  ```bash
  uv run pytest 15_file_import_reports/test_file_import.py
  ```
* **Required Parameters & Variables**:
  * `import_url`: Target file upload portal URL.
  * `valid_file_path`: Path to clean dataset file.
  * `invalid_file_path`: Path to file with corrupted/duplicate rows.
  * `download_dir`: Destination directory for downloaded error reports.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 15: Multi-File Import and Error Report Validation
  
  ## Description
  Tests batch CSV/Excel processing, row-level validation feedback, and downloadable error log inspection.
  
  ## Test Cases Solved
  - Successful import of clean CSV files.
  - Error detection for corrupted records, capturing error summary logs, and verifying parsed report contents.
  
  ## How to Run
  ```bash
  uv run pytest 15_file_import_reports/test_file_import.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `import_url` | File upload form web URL. |
  | `valid_file_path` | Local filesystem path to valid import asset. |
  | `invalid_file_path` | Local filesystem path to malformed import asset. |
  | `download_dir` | Local storage folder for intercepted download reports. |
  ```

---

### Project 16: Mock External Dependency Failures (`16_mock_dependency_failures`)
* **Goal**: Leverage Playwright's `page.route()` API to intercept network calls and mock third-party API failure modes.
* **Target Webpage**: E-Commerce Checkout / Banking Portal
* **Test Cases**:
  * **Test Case 1 (Payment Gateway Timeout & 500 Error)**:
    1. Intercept payment API route (`**/api/v1/payment`) using `page.route()`.
    2. Abort request or return HTTP status 500 with error payload.
    3. Assert user-friendly error message banner on UI without page crash.
  * **Test Case 2 (Slow Response & Partial Data)**:
    1. Intercept network request and inject artificial delay (e.g. 5000ms delay).
    2. Return partial or malformed JSON payload.
    3. Verify loading spinners, timeout handling, and graceful UI degrade modes.
* **Execution Command**:
  ```bash
  uv run pytest 16_mock_dependency_failures/test_mock_failures.py
  ```
* **Required Parameters & Variables**:
  * `app_url`: Application web URL.
  * `target_route_glob`: Glob pattern of API route to mock (`**/api/payment`).
  * `mock_status_code`: Simulated HTTP status code (e.g., `500`, `504`).
  * `mock_delay_ms`: Network response delay in milliseconds.
  * `expected_ui_banner`: Expected user-facing error text.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 16: Mock External Dependency Failures
  
  ## Description
  Simulates third-party service failures, network timeouts, and HTTP errors using Playwright route interception.
  
  ## Test Cases Solved
  - Intercepting checkout requests to mock HTTP 500 and timeout failures.
  - Validating frontend resilience, loading indicators, and graceful error banners.
  
  ## How to Run
  ```bash
  uv run pytest 16_mock_dependency_failures/test_mock_failures.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `target_route_glob` | Route pattern intercepted by `page.route()`. |
  | `mock_status_code` | HTTP status code returned by mock route. |
  | `mock_delay_ms` | Simulated latency added to the network response. |
  | `expected_ui_banner` | Asserted error banner text in frontend UI. |
  ```

---

### Project 17: Responsive Cross-Browser Regression Suite (`17_responsive_cross_browser`)
* **Goal**: Configure multi-browser and device-emulation matrix executions across Chromium, Firefox, WebKit, Mobile Chrome, and Mobile Safari.
* **Target Webpage**: Responsive E-Commerce Application / Web Portal
* **Test Case Description**:
  1. Execute a critical core flow (login, navigation, cart checkout) across desktop and mobile device viewports (`iPhone 13`, `Pixel 5`, `iPad Pro`).
  2. Verify that responsive UI elements (hamburger menu, mobile cart drawer, collapsible tables) behave correctly on small screen dimensions.
  3. Automatically capture visual screenshots on test failure for cross-browser debugging.
* **Execution Command**:
  ```bash
  uv run pytest 17_responsive_cross_browser/test_responsive.py --browser=all
  ```
* **Required Parameters & Variables**:
  * `target_url`: Website URL under test.
  * `device_profiles`: List of Playwright pre-configured device descriptors (`iPhone 13`, `Pixel 5`).
  * `screenshot_dir`: Output directory for failure artifacts.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 17: Responsive Cross-Browser Regression Suite
  
  ## Description
  Executes automated test flows across desktop engines (Chromium, Firefox, WebKit) and mobile viewports with failure screenshots.
  
  ## Test Cases Solved
  - Multi-browser execution matrix validation.
  - Mobile layout navigation and touch-friendly UI verification.
  - Automatic failure screenshot capture.
  
  ## How to Run
  ```bash
  uv run pytest 17_responsive_cross_browser/test_responsive.py --browser=all
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `target_url` | Web page tested across engine viewports. |
  | `device_profiles` | Playwright device emulation profiles configured for run. |
  | `screenshot_dir` | Directory path where failure snapshots are saved. |
  ```

---

### Project 18: Visual Regression Testing for Key Screens (`18_visual_regression`)
* **Goal**: Master visual visual comparison workflows using `toHaveScreenshot()`, snapshot baseline maintenance, and dynamic content masking.
* **Target Webpage**: Web Application Key Screens (Login, Dashboard, Checkout, Invoice)
* **Test Case Description**:
  1. Navigate to key application screens.
  2. Mask dynamic elements such as timestamps, transaction IDs, user session names, and dynamic advertisements.
  3. Execute `expect(page).to_have_screenshot()` visual comparison against reference baseline images.
  4. Detect visual regressions and update baselines via command-line flags.
* **Execution Command**:
  ```bash
  uv run pytest 18_visual_regression/test_visual.py --update-snapshots
  ```
* **Required Parameters & Variables**:
  * `snapshot_name`: Target image filename for visual reference.
  * `mask_locators`: Array of locators identifying dynamic elements to blackout during snapshot generation.
  * `threshold`: Acceptable pixel difference ratio (e.g. `0.05`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 18: Visual Regression Testing for Key Screens
  
  ## Description
  Performs pixel-perfect visual snapshot comparisons with dynamic data masking using Playwright's `toHaveScreenshot()`.
  
  ## Test Cases Solved
  - Creating visual baseline snapshots for key screens.
  - Masking dynamic elements (timestamps, user badges) to prevent false positives.
  - Visual drift detection and baseline updating.
  
  ## How to Run
  ```bash
  uv run pytest 18_visual_regression/test_visual.py --update-snapshots
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `snapshot_name` | Name of the baseline screenshot file. |
  | `mask_locators` | Playwright locators for dynamic elements to conceal. |
  | `threshold` | Pixel discrepancy tolerance ratio. |
  ```

---

### Project 19: Payment Transaction Lifecycle Simulation (`19_payment_lifecycle`)
* **Goal**: Model state machine transitions (Initiate -> Authorize -> Pending -> Complete -> Refund) and assert UI/API integrity at every stage.
* **Target Webpage**: Financial Platform / Payment Sandbox Application
* **Test Case Description**:
  1. Initiate a payment transaction via the checkout interface.
  2. Transition transaction states through Authorization and Pending states.
  3. Validate UI ledger entries, database record status via API, and system notifications after successful charge.
  4. Trigger a full/partial refund and assert balance calculation updates across UI panels and API responses.
* **Execution Command**:
  ```bash
  uv run pytest 19_payment_lifecycle/test_payment_lifecycle.py
  ```
* **Required Parameters & Variables**:
  * `initial_account_balance`: Numeric balance prior to payment execution.
  * `charge_amount`: Transaction amount deducted during payment.
  * `refund_amount`: Refund amount returned during reversal.
  * `expected_status_flow`: Ordered list of expected status states (`['Initiated', 'Authorized', 'Completed', 'Refunded']`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 19: Payment Transaction Lifecycle Simulation
  
  ## Description
  Simulates a financial state transition lifecycle with step-by-step UI and API audit verification.
  
  ## Test Cases Solved
  - End-to-end payment authorization, pending hold, completion, and refund lifecycle.
  - Account ledger balance math updates and transaction log validation.
  
  ## How to Run
  ```bash
  uv run pytest 19_payment_lifecycle/test_payment_lifecycle.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `initial_account_balance` | Starting monetary balance in test account. |
  | `charge_amount` | Value charged in the payment test step. |
  | `refund_amount` | Value reversed during refund execution. |
  | `expected_status_flow` | Sequential list of status states asserted at each transition. |
  ```

---

### Project 20: AI-Assisted Test Automation Framework (`20_ai_assisted_framework`)
* **Goal**: Construct an enterprise-grade scalable Playwright framework incorporating POM, reusable fixtures, test tagging, API setup, HTML reporting, and AI-generated test data variations.
* **Target Webpage**: Comprehensive SaaS / E-Commerce Demo System
* **Test Cases**:
  * **Test Case 1 (Smoke Test Suite Execution)**:
    1. Execute tagged smoke tests (`@pytest.mark.smoke`) verifying core login and checkout flows.
    2. Generate single-file HTML reports and failure execution traces.
  * **Test Case 2 (AI-Generated Data Regression Suite)**:
    1. Load AI-generated dataset variations (`positive`, `negative`, `boundary`, `exception`).
    2. Parameterize regression suite (`@pytest.mark.parametrize`).
    3. Assert framework setup/teardown hooks properly clean up resources upon completion.
* **Execution Command**:
  ```bash
  uv run pytest 20_ai_assisted_framework/tests/ --html=report.html --self-contained-html -m smoke
  ```
* **Required Parameters & Variables**:
  * `env_config`: Dictionary containing environment parameters (URLs, timeouts).
  * `ai_dataset`: Parameterized dataset containing boundary and edge-case inputs.
  * `report_file`: Output location for standalone HTML test runner report.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 20: AI-Assisted Test Automation Framework
  
  ## Description
  Implements an enterprise Playwright Python framework architecture with POM, custom Pytest fixtures, test tagging, HTML reports, and AI-generated test datasets.
  
  ## Test Cases Solved
  - Smoke test execution filtering with `@pytest.mark.smoke`.
  - Data-driven regression testing using AI-generated edge-case and boundary inputs.
  - Automatic HTML report and trace zip asset generation.
  
  ## How to Run
  ```bash
  uv run pytest 20_ai_assisted_framework/tests/ --html=report.html --self-contained-html -m smoke
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `env_config` | Target environment configuration dict. |
  | `ai_dataset` | Parameterized test input matrix (edge/boundary cases). |
  | `report_file` | File path where execution HTML report is created. |
  ```

---

## 4. Vibe-Coding Workflow Cycle

When working on Phase 2 tasks:
1. **Define the requirement** in plain English.
2. **Generate the code** using AI assistance.
3. **Run tests** and diagnose failures line-by-line.
4. **Refactor and optimize** code structure and ensure clear commenting.
5. **Update local README.md** parameter details.
