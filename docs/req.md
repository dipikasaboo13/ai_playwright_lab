# Requirements Specification: Playwright Python Lab

This document defines the requirements, tooling, project structure, and detailed specifications for each of the 10 practical Playwright projects.

---

## 1. Technical Stack & Tooling

The projects in this repository are implemented using **Python** and **uv** (an extremely fast Python package and project manager). 

### Prerequisites
- Python 3.10 or higher
- `uv` command-line tool

### Workspace Setup Guidelines
Each subproject should run within a virtual environment managed by `uv`. The general dependency stack includes:
- `pytest` - Test runner framework
- `pytest-playwright` - Playwright integration plugin for Pytest
- `playwright` - Core browser automation library

To set up the workspace, developers will use:
```bash
# Initialize Python project using uv (if not already done)
uv init

# Add required dependencies
uv add pytest pytest-playwright

# Install Playwright browser binaries
uv run playwright install
```

---

## 2. General Subproject Requirements

To ensure consistency, readability, and ease of learning, every subproject directory must adhere to the following rules:

### A. Dedicated `README.md` File
Each subproject directory (e.g., `01_open_verify/`) must contain a dedicated `README.md` with:
1. **Project Description**: A clear summary of what the project is doing and why.
2. **Test Cases Solved**: A structured list of test scenarios covered in the project.
3. **Execution Instructions**: The exact command(s) to run the tests using `uv run pytest`.
4. **Parameter Dictionary**: A detailed breakdown of every parameter, variable, or credential used in the test scripts and what they do.

### B. Comprehensive Code Commenting
All code files must be heavily documented with comments explaining:
- The purpose of specific fixtures (e.g., `page`, `browser`, custom fixtures).
- The intent behind complex locators and action APIs (`page.goto`, `locator.click`, `fill`, etc.).
- The assertion logic and expected UI states.
- Error handling, timeouts, or dialog-handling setups.

---

## 3. Subproject Specifications

Below are the detailed requirements and test cases for each of the 10 subprojects.

---

### Project 1: Open and Verify a Webpage (`01_open_verify`)
* **Goal**: Learn the basics of initializing Playwright, page navigation, and executing basic assertions.
* **Target Webpage**: [Playwright Python Documentation](https://playwright.dev/python/)
* **Test Case Description**:
  1. Navigate to the Playwright Python page.
  2. Verify that the page title contains "Playwright".
  3. Verify that the main page heading "Playwright enables reliable end-to-end testing" is visible on the screen.
* **Execution Command**:
  ```bash
  uv run pytest 01_open_verify/test_open_verify.py
  ```
* **Required Parameters & Variables**:
  * `target_url`: The URL to navigate to (`https://playwright.dev/python/`).
  * `expected_title`: The expected substring in the page title (`Playwright`).
  * `expected_heading`: The heading text to assert visibility for (`Playwright enables reliable end-to-end testing`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 1: Open and Verify Webpage
  
  ## Description
  This subproject covers Playwright setup, basic page navigation, and heading text assertions.
  
  ## Test Cases Solved
  - Navigating to the official Playwright Python homepage.
  - Verifying page title matches expected text.
  - Asserting the presence and visibility of the main hero heading.
  
  ## How to Run
  ```bash
  uv run pytest 01_open_verify/test_open_verify.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `target_url` | The URL under test. |
  | `expected_title` | The string expected to be in the browser title bar. |
  | `expected_heading` | The hero header text to verify on the page. |
  ```

---

### Project 2: Login Form Automation (`02_login_form`)
* **Goal**: Interact with text inputs and buttons, handling both positive (successful) and negative (failed) login paths.
* **Target Webpage**: [SauceDemo (Swag Labs)](https://www.saucedemo.com/)
* **Test Cases**:
  * **Test Case 1 (Success)**:
    1. Navigate to SauceDemo.
    2. Input Username `standard_user` and Password `secret_sauce`.
    3. Click the Login button.
    4. Verify navigation to the inventory page (URL contains `/inventory.html`).
  * **Test Case 2 (Failure)**:
    1. Navigate to SauceDemo.
    2. Input Username `invalid_user` and Password `wrong_password`.
    3. Click the Login button.
    4. Verify that an error message is displayed containing: "Username and password do not match any user in this service".
* **Execution Command**:
  ```bash
  uv run pytest 02_login_form/test_login.py
  ```
* **Required Parameters & Variables**:
  * `login_url`: Target URL (`https://www.saucedemo.com/`).
  * `valid_username` / `valid_password`: Correct login credentials.
  * `invalid_username` / `invalid_password`: Incorrect login credentials.
  * `error_msg_substring`: Substring to assert on authentication failure.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 2: Login Form Automation
  
  ## Description
  Tests standard form filling, submit actions, and positive/negative assertion flows on the SauceDemo login page.
  
  ## Test Cases Solved
  - Successful login redirecting to `/inventory.html`.
  - Failed login with invalid credentials displaying the correct error message.
  
  ## How to Run
  ```bash
  uv run pytest 02_login_form/test_login.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `login_url` | URL of the login form under test. |
  | `valid_username` | Username for the success scenario. |
  | `valid_password` | Password for the success scenario. |
  | `invalid_username` | Incorrect username to trigger validation. |
  | `invalid_password` | Incorrect password to trigger validation. |
  | `error_msg_substring` | Expected error text when authentication fails. |
  ```

---

### Project 3: Search and Filter Products (`03_search_filter`)
* **Goal**: Test interactive dropdowns and dynamic product lists by selecting categories.
* **Target Webpage**: [Demoblaze](https://demoblaze.com/)
* **Test Case Description**:
  1. Navigate to Demoblaze.
  2. Select the "Laptops" category from the side menu.
  3. Verify that the product list updates to show laptop models (e.g., "Sony vaio", "MacBook air").
  4. Verify that non-laptop items (such as "Samsung galaxy s6" or "ASUS Full HD") are not displayed in the results.
* **Execution Command**:
  ```bash
  uv run pytest 03_search_filter/test_search_filter.py
  ```
* **Required Parameters & Variables**:
  * `homepage_url`: Target URL (`https://demoblaze.com/`).
  * `category_name`: The category to click (`Laptops`).
  * `expected_item`: A product name that must appear under this category.
  * `excluded_item`: A product name from another category that must not appear.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 3: Search and Filter Products
  
  ## Description
  Automates interacting with dynamic navigation links and asserting correct product list filtering.
  
  ## Test Cases Solved
  - Filtering by the 'Laptops' category.
  - Verifying laptops are shown and phones/monitors are hidden.
  
  ## How to Run
  ```bash
  uv run pytest 03_search_filter/test_search_filter.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `homepage_url` | URL of Demoblaze homepage. |
  | `category_name` | The filter category string. |
  | `expected_item` | An item name that must appear when filter is active. |
  | `excluded_item` | An item name that must not appear when filter is active. |
  ```

---

### Project 4: Add Product to Cart (`04_add_to_cart`)
* **Goal**: Validate complex multi-page state transitions, browser popup dialogs, and cart calculations.
* **Target Webpage**: [Demoblaze](https://demoblaze.com/)
* **Test Case Description**:
  1. Navigate to Demoblaze and select product A (e.g., "Samsung galaxy s6").
  2. Click "Add to cart" and accept the browser dialog confirmation popup.
  3. Navigate back to the homepage and select product B (e.g., "Nokia lumia 1520").
  4. Click "Add to cart" and accept the browser dialog confirmation popup.
  5. Go to the "Cart" page.
  6. Verify both items exist in the cart list.
  7. Delete product A and verify that the cart total decreases by product A's price.
* **Execution Command**:
  ```bash
  uv run pytest 04_add_to_cart/test_cart.py
  ```
* **Required Parameters & Variables**:
  * `product_a_name` / `product_a_price`: Details of the first item to purchase.
  * `product_b_name` / `product_b_price`: Details of the second item to purchase.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 4: Add Product to Cart
  
  ## Description
  Covers page navigation loops, handling JavaScript alert dialogs, verifying shopping cart lists, and validating price math.
  
  ## Test Cases Solved
  - Adding multiple items to the cart and handling confirmation alerts.
  - Verifying items are correctly listed in the cart.
  - Deleting an item and validating that the price calculation updates dynamically.
  
  ## How to Run
  ```bash
  uv run pytest 04_add_to_cart/test_cart.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `product_a_name` | Name of the first product. |
  | `product_b_name` | Name of the second product. |
  ```

---

### Project 5: Data-Driven Login Tests (`05_data_driven_login`)
* **Goal**: Separate test logic from test data by loading login credentials from an external JSON file.
* **Target Webpage**: [SauceDemo (Swag Labs)](https://www.saucedemo.com/)
* **Test Data File**: `credentials.json`
* **Test Case Description**:
  1. Load multiple credential sets from `credentials.json`.
  2. Parameterize tests using `pytest.mark.parametrize`.
  3. Run the login process for each dataset.
  4. Verify that each credential type redirects to the inventory page or shows the expected validation error message.
* **Execution Command**:
  ```bash
  uv run pytest 05_data_driven_login/test_data_driven.py
  ```
* **Required Parameters & Variables**:
  * `data_file_path`: Path to `credentials.json`.
  * `username` / `password`: Credentials injected per iteration.
  * `expected_outcome`: Expected result type (`success`, `locked_out_error`, `invalid_error`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 5: Data-Driven Login Tests
  
  ## Description
  Reads credentials from an external JSON file and runs a parameterized test suite covering various user profiles.
  
  ## Test Cases Solved
  - Standard user login (Success).
  - Locked out user login (Error validation).
  - Invalid user login (Error validation).
  
  ## How to Run
  ```bash
  uv run pytest 05_data_driven_login/test_data_driven.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `data_file_path` | Path to the credentials source JSON. |
  | `username` | The injected username. |
  | `password` | The injected password. |
  | `expected_outcome` | Key indicating if the test expects success or an error message. |
  ```

---

### Project 6: API + UI Validation (`06_api_ui_validation`)
* **Goal**: Send API requests and assert that the retrieved data maps onto the browser's UI.
* **Target Resources**:
  - API: `POST https://api.demoblaze.com/entries`
  - UI Webpage: `https://demoblaze.com/`
* **Test Case Description**:
  1. Send an HTTP POST request to the Demoblaze catalog API to fetch available products.
  2. Parse the product titles and prices from the JSON response.
  3. Load the frontend URL in the browser.
  4. Match the API-returned product titles/prices with the elements rendered in the product grid.
* **Execution Command**:
  ```bash
  uv run pytest 06_api_ui_validation/test_api_ui.py
  ```
* **Required Parameters & Variables**:
  * `api_endpoint`: Target API URL (`https://api.demoblaze.com/entries`).
  * `ui_url`: Frontend website URL (`https://demoblaze.com/`).
* **Subproject `README.md` Template**:
  ```markdown
  # Project 6: API + UI Validation
  
  ## Description
  Leverages Playwright's `APIRequestContext` to invoke endpoints directly, then performs UI audits to verify matching content.
  
  ## Test Cases Solved
  - Fetching catalog items via API.
  - Navigating the UI and matching products to ensure database integrity.
  
  ## How to Run
  ```bash
  uv run pytest 06_api_ui_validation/test_api_ui.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `api_endpoint` | Endpoint URI used to query products. |
  | `ui_url` | Browser page URL containing the catalog. |
  ```

---

### Project 7: File Upload and Download (`07_upload_download`)
* **Goal**: Manage filesystem interactions, trigger uploads, and intercept downloads.
* **Target Webpages**:
  - [The Internet - File Upload](https://the-internet.herokuapp.com/upload)
  - [The Internet - File Download](https://the-internet.herokuapp.com/download)
* **Test Cases**:
  * **Test Case 1 (Upload)**:
    1. Navigate to the upload page.
    2. Use `page.expect_file_chooser()` or file input locators to select `test_upload.txt`.
    3. Submit the file.
    4. Assert that the confirmation header shows "File Uploaded!".
  * **Test Case 2 (Download)**:
    1. Navigate to the download page.
    2. Click a downloadable file link (e.g., `some-file.txt`) and capture the download payload using `page.expect_download()`.
    3. Save the file to a temporary folder.
    4. Verify that the file exists and is not empty.
* **Execution Command**:
  ```bash
  uv run pytest 07_upload_download/test_files.py
  ```
* **Required Parameters & Variables**:
  * `upload_url` / `download_url`: Target URLs.
  * `upload_file_path`: Path to local file for upload testing.
  * `download_save_dir`: Directory where downloaded assets are stored.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 7: File Upload and Download
  
  ## Description
  Handles file upload forms and intercepts background download streams in Playwright tests.
  
  ## Test Cases Solved
  - Selecting and uploading a local file.
  - Intercepting file download triggers and writing output to disk.
  
  ## How to Run
  ```bash
  uv run pytest 07_upload_download/test_files.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `upload_url` | Upload test form URL. |
  | `download_url` | List of downloadable files page. |
  | `upload_file_path` | Absolute/relative path to the sample file to upload. |
  | `download_save_dir` | Storage location for completed downloads. |
  ```

---

### Project 8: Multi-User Approval Workflow (`08_multi_user_approval`)
* **Goal**: Orchestrate multi-context workflows by simulating interactions between two users simultaneously.
* **Target Webpage**: A simple local FastAPI dashboard service (launched before tests).
* **Test Case Description**:
  1. Open two separate, isolated browser contexts (`UserA` context and `UserB` context).
  2. `UserA` (Requester) logs in, fills out a submission form, and hits submit.
  3. `UserB` (Approver) logs in, loads the approval dashboard, finds User A's submission, and clicks "Approve".
  4. `UserA`'s page refreshes or polls and verifies the status changes from "Pending" to "Approved".
* **Execution Command**:
  ```bash
  uv run pytest 08_multi_user_approval/test_approval.py
  ```
* **Required Parameters & Variables**:
  * `app_url`: Local host URL where the FastAPI test application is running.
  * `requester_creds`: Credentials for `UserA`.
  * `approver_creds`: Credentials for `UserB`.
  * `request_payload_title`: Title of request to trace.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 8: Multi-User Approval Workflow
  
  ## Description
  Tests concurrent roles using isolated browser contexts without cookie/session leakages.
  
  ## Test Cases Solved
  - Request creation by `UserA`.
  - Request approval by `UserB` in a separate session.
  - Real-time status update visibility on `UserA`'s panel.
  
  ## How to Run
  ```bash
  uv run pytest 08_multi_user_approval/test_approval.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `app_url` | Local server port URL. |
  | `requester_creds` | Login info for request author. |
  | `approver_creds` | Login info for approver. |
  | `request_payload_title` | Dynamic title identifier used to map approval rows. |
  ```

---

### Project 9: Build a Mini Test Framework (`09_mini_test_framework`)
* **Goal**: Implement the Page Object Model (POM) and build robust failure logging with screenshots and traces.
* **Target Webpage**: [SauceDemo (Swag Labs)](https://www.saucedemo.com/)
* **Test Case Description**:
  1. Create a Page Object directory structured with `LoginPage`, `InventoryPage`, and `CartPage` classes.
  2. Write high-level test scripts referencing these POM classes.
  3. Configure a custom Pytest fixture in `conftest.py` that checks test outcomes. If a test fails, capture a screenshot and save the Playwright execution trace zip.
* **Execution Command**:
  ```bash
  uv run pytest 09_mini_test_framework/tests/test_pom_flow.py --tracing=retain-on-failure
  ```
* **Required Parameters & Variables**:
  * `pom_locators`: Embedded selectors housed inside page classes.
  * `artifact_output_dir`: Location to drop failure assets.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 9: Mini Test Framework (POM)
  
  ## Description
  Applies enterprise design patterns using Page Objects, centralized configurations, and screenshot/trace logging on failure.
  
  ## Test Cases Solved
  - End-to-end shopping cart checkout written via POM abstractions.
  - Automatic failure capture hooks in `conftest.py`.
  
  ## How to Run
  ```bash
  uv run pytest 09_mini_test_framework/tests/test_pom_flow.py --tracing=retain-on-failure
  ```
  
  ## Parameter Reference
  | Parameter / Selector | Page Class | Purpose |
  |----------------------|------------|---------|
  | `username_input` | `LoginPage` | Locator for username field. |
  | `password_input` | `LoginPage` | Locator for password field. |
  | `inventory_list` | `InventoryPage` | Locator for product cards. |
  | `cart_items` | `CartPage` | Selector for rows in shopping cart. |
  ```

---

### Project 10: Payment Checkout Simulation (`10_payment_checkout`)
* **Goal**: Conduct a full end-to-end multi-step checkout workflow validating validation messages and price sums.
* **Target Webpage**: [SauceDemo (Swag Labs)](https://www.saucedemo.com/)
* **Test Cases**:
  * **Test Case 1 (Success)**:
    1. Log in.
    2. Add two specific items to the cart.
    3. Navigate to checkout, fill in first name, last name, and postal code.
    4. Confirm receipt page lists correct items, taxes, and final mathematical total.
    5. Click Finish and assert final success page heading "Thank you for your order!".
  * **Test Case 2 (Form Validation Error)**:
    1. Fill in checkout form details but leave the postal code blank.
    2. Click Continue.
    3. Assert validation message: "Error: Postal Code is required".
* **Execution Command**:
  ```bash
  uv run pytest 10_payment_checkout/test_checkout.py
  ```
* **Required Parameters & Variables**:
  * `first_name` / `last_name` / `postal_code`: Customer input strings.
  * `expected_tax_rate`: Decimal representing expected taxation factor.
* **Subproject `README.md` Template**:
  ```markdown
  # Project 10: Payment Checkout Simulation
  
  ## Description
  Validates a complete E2E transactional checkout flow, ensuring form constraints and calculations.
  
  ## Test Cases Solved
  - Complete purchase validation including subtotals, tax math, and final order.
  - Checkout form validation (missing postal code handling).
  
  ## How to Run
  ```bash
  uv run pytest 10_payment_checkout/test_checkout.py
  ```
  
  ## Parameter Reference
  | Parameter | Description |
  |-----------|-------------|
  | `first_name` | Checkout form input. |
  | `last_name` | Checkout form input. |
  | `postal_code` | Checkout form input (empty in Case 2). |
  | `expected_tax_rate` | Applied tax percentage used to assert totals. |
  ```

---

## 4. Vibe-Coding Workflow Cycle
When working on these tasks:
1. **Define the requirement** in plain English.
2. **Generate the code** using AI assistance.
3. **Run tests** and diagnose failures line-by-line.
4. **Refactor and optimize** code structure and ensure clear commenting.
5. **Update local README.md** parameter details.
