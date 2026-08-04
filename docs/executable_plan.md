# Executable Implementation Plan: Playwright Python Lab

This document breaks down the development process into atomic, independent, and verifiable tasks. Each task defines clear deliverables and an independent verification method.

---

## Workspace & Core Tooling Tasks

### Task 0: Environment Initialization
* **Objective**: Establish the Python 3.10+ virtual environment and install core browser libraries.
* **Steps**:
  1. Initialize project-level Python setup using `uv init`.
  2. Add `pytest` and `pytest-playwright` dependencies.
  3. Install core browsers via `uv run playwright install`.
  4. Create a `.gitignore` ignoring `.venv/`, `__pycache__/`, `artifacts/`, and `.pytest_cache/`.
* **Validation**:
  ```bash
  uv run pytest --version
  uv run playwright --version
  ```

---

## Subproject Tasks

### Project 1: Open and Verify Webpage (`01_open_verify`)
* **Task 1.1: Implement Test Script**
  * **Objective**: Write `test_open_verify.py` to navigate and check headings.
  * **Steps**:
    1. Navigate to `https://playwright.dev/python/`.
    2. Assert title contains "Playwright".
    3. Assert visibility of heading "Playwright enables reliable end-to-end testing".
  * **Validation**:
    ```bash
    uv run pytest 01_open_verify/test_open_verify.py
    ```
* **Task 1.2: Project Documentation**
  * **Objective**: Create `01_open_verify/README.md`.
  * **Validation**: Confirm file exists and contains the project description, solved test cases, execution commands, and parameter references.

---

### Project 2: Login Form Automation (`02_login_form`)
* **Task 2.1: Success Login Test Scenario**
  * **Objective**: Write positive login test to redirect to inventory page.
  * **Steps**:
    1. Navigate to `https://www.saucedemo.com/`.
    2. Fill user credentials (`standard_user` / `secret_sauce`).
    3. Click login button and assert landing URL contains `/inventory.html`.
  * **Validation**:
    ```bash
    uv run pytest 02_login_form/test_login.py -k "test_successful_login"
    ```
* **Task 2.2: Failure Login Test Scenario**
  * **Objective**: Write negative login test asserting dynamic error string.
  * **Steps**:
    1. Navigate to the login page.
    2. Input incorrect credentials and click login.
    3. Assert the visibility of the expected validation error element and text.
  * **Validation**:
    ```bash
    uv run pytest 02_login_form/test_login.py -k "test_failed_login"
    ```
* **Task 2.3: Project Documentation**
  * **Objective**: Create `02_login_form/README.md`.
  * **Validation**: Confirm file exists and details all valid/invalid parameters.

---

### Project 3: Search and Filter Products (`03_search_filter`)
* **Task 3.1: Category Filter Test Scenario**
  * **Objective**: Automate categories selection and list assertions.
  * **Steps**:
    1. Navigate to `https://demoblaze.com/`.
    2. Click on the "Laptops" category menu link.
    3. Verify laptop items are shown, and items like phones are absent.
  * **Validation**:
    ```bash
    uv run pytest 03_search_filter/test_search_filter.py
    ```
* **Task 3.2: Project Documentation**
  * **Objective**: Create `03_search_filter/README.md`.
  * **Validation**: Confirm file exists with parameter listings.

---

### Project 4: Add Product to Cart (`04_add_to_cart`)
* **Task 4.1: Cart Addition and Dialog Interaction**
  * **Objective**: Handle dynamic alerts during cart insertions.
  * **Steps**:
    1. Navigate to Demoblaze, select Product A, and handle dialog confirmation.
    2. Return to home, select Product B, and handle dialog confirmation.
  * **Validation**: Run the initial addition script and verify no browser blockages.
* **Task 4.2: Cart Deletion & Pricing Verification**
  * **Objective**: Parse lists and evaluate numerical differences.
  * **Steps**:
    1. Open the shopping cart page.
    2. Assert presence of Product A and Product B.
    3. Store cart subtotal, delete Product A, and assert that the subtotal is reduced by Product A's exact price.
  * **Validation**:
    ```bash
    uv run pytest 04_add_to_cart/test_cart.py
    ```
* **Task 4.3: Project Documentation**
  * **Objective**: Create `04_add_to_cart/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 5: Data-Driven Login Tests (`05_data_driven_login`)
* **Task 5.1: Create Test Data Source**
  * **Objective**: Prepare input files.
  * **Steps**: Create `credentials.json` with standard, locked, and invalid credentials.
  * **Validation**: Confirm the file is readable as valid JSON.
* **Task 5.2: Parameterized Test Implementation**
  * **Objective**: Setup pytest parametrizations reading from JSON file.
  * **Steps**: Use `@pytest.mark.parametrize` to loop over credentials and assert outcomes.
  * **Validation**:
    ```bash
    uv run pytest 05_data_driven_login/test_data_driven.py
    ```
* **Task 5.3: Project Documentation**
  * **Objective**: Create `05_data_driven_login/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 6: API + UI Validation (`06_api_ui_validation`)
* **Task 6.1: API Query Setup**
  * **Objective**: Trigger POST request to Demoblaze catalog.
  * **Steps**: Retrieve data from `https://api.demoblaze.com/entries` and save to an in-memory dictionary.
  * **Validation**: Confirm response code is 200 and parses successfully.
* **Task 6.2: Frontend Matching Assertions**
  * **Objective**: Cross-reference API payloads against frontend DOM elements.
  * **Steps**: Launch browser, load catalog homepage, and assert elements have matching titles/prices.
  * **Validation**:
    ```bash
    uv run pytest 06_api_ui_validation/test_api_ui.py
    ```
* **Task 6.3: Project Documentation**
  * **Objective**: Create `06_api_ui_validation/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 7: File Upload and Download (`07_upload_download`)
* **Task 7.1: Upload Test Scenario**
  * **Objective**: Upload local test asset and verify submission header.
  * **Steps**:
    1. Create a template file `test_upload.txt`.
    2. Upload via input chooser on `the-internet.herokuapp.com/upload`.
    3. Assert success heading element text.
  * **Validation**:
    ```bash
    uv run pytest 07_upload_download/test_files.py -k "test_upload"
    ```
* **Task 7.2: Download Test Scenario**
  * **Objective**: Capture and save down download event data.
  * **Steps**:
    1. Trigger download on target page using `page.expect_download()`.
    2. Write download to disk and assert size > 0.
  * **Validation**:
    ```bash
    uv run pytest 07_upload_download/test_files.py -k "test_download"
    ```
* **Task 7.3: Project Documentation**
  * **Objective**: Create `07_upload_download/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 8: Multi-User Approval Workflow (`08_multi_user_approval`)
* **Task 8.1: Create Mock Backend Server**
  * **Objective**: Write simple local server to support testing.
  * **Steps**: Code a lightweight `server.py` in FastAPI with dynamic endpoints for submissions and approval.
  * **Validation**: Run server and query health endpoint using `curl`.
* **Task 8.2: Implement Dual Browser Context Test**
  * **Objective**: Orchestrate User A & User B workflows.
  * **Steps**:
    1. Launch two separate contexts (`user_a_context` and `user_b_context`).
    2. User A creates request.
    3. User B approves request.
    4. Verify User A sees status updated to "Approved".
  * **Validation**:
    ```bash
    uv run pytest 08_multi_user_approval/test_approval.py
    ```
* **Task 8.3: Project Documentation**
  * **Objective**: Create `08_multi_user_approval/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 9: Build a Mini Test Framework (`09_mini_test_framework`)
* **Task 9.1: Page Object Classes**
  * **Objective**: Construct modular locators and action pages.
  * **Steps**: Write `LoginPage`, `InventoryPage`, and `CartPage`.
  * **Validation**: Check that classes contain selectors and expose logical action methods.
* **Task 9.2: conftest.py Capture Setup**
  * **Objective**: Build failure hook tracking.
  * **Steps**: Configure Pytest post-run checks to capture screenshots/traces to a local repository folder.
  * **Validation**: Force a test failure and confirm screenshot and trace zip file outputs are created in the workspace.
* **Task 9.3: POM E2E Test Execution**
  * **Objective**: Create tests utilizing POM elements.
  * **Validation**:
    ```bash
    uv run pytest 09_mini_test_framework/tests/test_pom_flow.py
    ```
* **Task 9.4: Project Documentation**
  * **Objective**: Create `09_mini_test_framework/README.md`.
  * **Validation**: Confirm file exists.

---

### Project 10: Payment Checkout Simulation (`10_payment_checkout`)
* **Task 10.1: Success Checkout Test Scenario**
  * **Objective**: Automate purchasing flow and math confirmations.
  * **Steps**: Add items, fill checkout form, check subtotal calculations (items total + tax = final total), and finalize.
  * **Validation**:
    ```bash
    uv run pytest 10_payment_checkout/test_checkout.py -k "test_successful_checkout"
    ```
* **Task 10.2: Form Validation Error Test Scenario**
  * **Objective**: Verify error fields logic.
  * **Steps**: Leave postal code empty during checkout step and assert form alert validation messages.
  * **Validation**:
    ```bash
    uv run pytest 10_payment_checkout/test_checkout.py -k "test_missing_postal_code"
    ```
* **Task 10.3: Project Documentation**
  * **Objective**: Create `10_payment_checkout/README.md`.
  * **Validation**: Confirm file exists.
