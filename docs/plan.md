# Implementation Plan: Playwright Python Lab

This document defines the step-by-step roadmap to implement and verify the 10 vibe-coding Playwright projects.

---

## Phase 1: Environment Initialization

### Task 1.1: Root Workspace Setup
- Initialize the python project root workspace using `uv`.
- Configure core dependencies in `pyproject.toml` including `pytest` and `pytest-playwright`.
- Download and configure Playwright browser runtimes (Chromium, Firefox, WebKit).

### Task 1.2: Global Configuration
- Create a baseline `.gitignore` file to ignore `.venv/`, `__pycache__/`, download outputs, and test trace/screenshot artifacts.

---

## Phase 2: Sequential Subproject Execution

Each project follows the vibe-coding cycle:
1. Initialize the project directory.
2. Draft the automated test file using AI assistant inputs.
3. Validate and debug locally using `uv run pytest`.
4. Refactor the code with clear comments.
5. Generate the dedicated subproject `README.md`.

---

### Project 1: Open and Verify Webpage (`01_open_verify`)
- **Step 1**: Create directory `01_open_verify/`.
- **Step 2**: Create `test_open_verify.py` verifying `playwright.dev/python` title and main hero heading text.
- **Step 3**: Execute: `uv run pytest 01_open_verify/`
- **Step 4**: Create `01_open_verify/README.md`.

---

### Project 2: Login Form Automation (`02_login_form`)
- **Step 1**: Create directory `02_login_form/`.
- **Step 2**: Implement `test_login.py` covering:
  - Valid login asserting navigation redirect to `/inventory.html`.
  - Invalid login asserting specific error message visibility.
- **Step 3**: Execute: `uv run pytest 02_login_form/`
- **Step 4**: Create `02_login_form/README.md`.

---

### Project 3: Search and Filter Products (`03_search_filter`)
- **Step 1**: Create directory `03_search_filter/`.
- **Step 2**: Implement `test_search_filter.py` clicking the "Laptops" category on Demoblaze and verifying matching models.
- **Step 3**: Execute: `uv run pytest 03_search_filter/`
- **Step 4**: Create `03_search_filter/README.md`.

---

### Project 4: Add Product to Cart (`04_add_to_cart`)
- **Step 1**: Create directory `04_add_to_cart/`.
- **Step 2**: Implement `test_cart.py` handling alert dialog overlays, navigation back-and-forth, item list extraction, and cart item deletion value comparison.
- **Step 3**: Execute: `uv run pytest 04_add_to_cart/`
- **Step 4**: Create `04_add_to_cart/README.md`.

---

### Project 5: Data-Driven Login Tests (`05_data_driven_login`)
- **Step 1**: Create directory `05_data_driven_login/`.
- **Step 2**: Create `credentials.json` with user profiles.
- **Step 3**: Implement `test_data_driven.py` loading JSON and invoking `@pytest.mark.parametrize` for testing credentials.
- **Step 4**: Execute: `uv run pytest 05_data_driven_login/`
- **Step 5**: Create `05_data_driven_login/README.md`.

---

### Project 6: API + UI Validation (`06_api_ui_validation`)
- **Step 1**: Create directory `06_api_ui_validation/`.
- **Step 2**: Implement `test_api_ui.py` querying `https://api.demoblaze.com/entries` via APIRequestContext, and comparing the payload titles against DOM cards.
- **Step 3**: Execute: `uv run pytest 06_api_ui_validation/`
- **Step 4**: Create `06_api_ui_validation/README.md`.

---

### Project 7: File Upload and Download (`07_upload_download`)
- **Step 1**: Create directory `07_upload_download/`.
- **Step 2**: Create a dummy `test_upload.txt` file.
- **Step 3**: Implement `test_files.py` testing the file chooser upload, and file download interception.
- **Step 4**: Execute: `uv run pytest 07_upload_download/`
- **Step 5**: Create `07_upload_download/README.md`.

---

### Project 8: Multi-User Approval Workflow (`08_multi_user_approval`)
- **Step 1**: Create directory `08_multi_user_approval/`.
- **Step 2**: Implement a lightweight local mock server in `server.py` using FastAPI.
- **Step 3**: Implement `test_approval.py` using separate browser contexts for Requester and Approver.
- **Step 4**: Execute: `uv run pytest 08_multi_user_approval/`
- **Step 5**: Create `08_multi_user_approval/README.md`.

---

### Project 9: Build a Mini Test Framework (`09_mini_test_framework`)
- **Step 1**: Create directory `09_mini_test_framework/` and sub-folders `pages/` and `tests/`.
- **Step 2**: Code base page objects and subproject page objects.
- **Step 3**: Setup screenshot and trace hooks in `conftest.py`.
- **Step 4**: Implement POM test flows.
- **Step 5**: Execute: `uv run pytest 09_mini_test_framework/tests/`
- **Step 6**: Create `09_mini_test_framework/README.md`.

---

### Project 10: Payment Checkout Simulation (`10_payment_checkout`)
- **Step 1**: Create directory `10_payment_checkout/`.
- **Step 2**: Write full transactional tests verifying price sums (item price + tax) and form error overlays.
- **Step 3**: Execute: `uv run pytest 10_payment_checkout/`
- **Step 4**: Create `10_payment_checkout/README.md`.

---

## Phase 3: Final Integration & Verification
- Run all test suites in headless and headed mode.
- Verify each folder contains its respective `README.md` and highly commented source code.
