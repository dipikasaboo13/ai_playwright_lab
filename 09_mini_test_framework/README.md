# Project 9: Build a Mini Test Framework (`09_mini_test_framework`)

## Objectives
Construct a scalable, modular Page Object Model (POM) end-to-end test framework in Python using Playwright and Pytest. The framework features automated test failure hooks that capture screenshots and Playwright execution trace zip archives whenever a test fails.

---

## Directory Architecture
```text
09_mini_test_framework/
├── conftest.py             # Pytest configuration, Playwright tracing autouse fixture & failure hook
├── pages/                  # Page Object Model encapsulation layer
│   ├── __init__.py         # Package exporter
│   ├── base_page.py        # Abstract/base Page class with common Playwright operations
│   ├── login_page.py       # LoginPage locators and user actions
│   ├── inventory_page.py   # InventoryPage locators and catalog actions
│   └── cart_page.py        # CartPage locators and shopping cart actions
├── tests/                  # Test suites utilizing Page Objects
│   └── test_pom_flow.py    # E2E tests for login, product addition, cart validation, and failure tracking
├── artifacts/              # Automatically generated on test failure
│   ├── screenshots/        # PNG screenshots captured on test failure
│   └── traces/             # Zip archives containing Playwright execution traces for debugging
└── README.md               # Subproject documentation
```

---

## Solved Scenarios & Test Cases
1. **`test_pom_successful_login_and_cart_flow`**:
   - Navigates to SauceDemo login page via `LoginPage`.
   - Performs user authentication with valid credentials.
   - Asserts page title and URL via `InventoryPage`.
   - Adds product ("Sauce Labs Backpack") to cart and validates badge counter update.
   - Navigates to `CartPage` and asserts item presence.

2. **`test_pom_invalid_login_error`**:
   - Navigates to SauceDemo login page.
   - Attempts login with locked out user credentials.
   - Validates error message container visibility and text via `LoginPage`.

3. **`test_pom_cart_item_removal`**:
   - Logs in as standard user and adds multiple items to cart ("Sauce Labs Backpack" and "Sauce Labs Bike Light").
   - Navigates to cart page and removes one item.
   - Asserts removed item is no longer present while remaining item persists.

4. **`test_forced_failure_for_artifact_capture`**:
   - Intentional failure test case designed to verify `conftest.py` post-test hooks.
   - Automatically generates PNG screenshots under `artifacts/screenshots/` and `.zip` trace files under `artifacts/traces/`.

---

## Command-Line Execution Instructions

### 1. Run all passing POM tests:
```bash
uv run pytest 09_mini_test_framework/tests/test_pom_flow.py -k "not test_forced_failure"
```

### 2. Run the intentional failure test to verify failure artifact capture:
```bash
uv run pytest 09_mini_test_framework/tests/test_pom_flow.py -k "test_forced_failure"
```

### 3. Run all tests in subproject:
```bash
uv run pytest 09_mini_test_framework/
```

---

## Key Parameters & Architecture Design

### Page Object Model (POM) Design
- **`BasePage`**: Encapsulates common Playwright page interactions (`navigate_to`, `get_url`, `get_title`).
- **`LoginPage`**: Encapsulates `#user-name`, `#password`, `#login-button`, and `[data-test='error']`.
- **`InventoryPage`**: Encapsulates `.title`, `.inventory_item`, `.shopping_cart_link`, `.shopping_cart_badge`, and dynamic item addition by name.
- **`CartPage`**: Encapsulates `.cart_item`, `.inventory_item_name`, `#checkout`, and item removal actions.

### Automated Failure Artifact Hook (`conftest.py`)
- **Tracing Fixture**: An `autouse=True` fixture starts Playwright tracing (`context.tracing.start(screenshots=True, snapshots=True, sources=True)`) before every test run.
- **`pytest_runtest_makereport` Hook**: Evaluates test outcome after execution. On test failure (`report.failed`), it automatically:
  1. Captures a screenshot to `09_mini_test_framework/artifacts/screenshots/<test_name>.png`.
  2. Saves the Playwright execution trace to `09_mini_test_framework/artifacts/traces/<test_name>.zip`.
