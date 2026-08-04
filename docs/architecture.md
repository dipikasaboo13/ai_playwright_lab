# Architecture Specification: Playwright Python Lab

This document defines the high-level architecture, design patterns, and repository structure for the Playwright Python Lab.

---

## 1. Directory Structure

The repository is structured as a mono-repo containing 10 decoupled subprojects. Each subproject is self-contained with its own test suite and documentation.

```text
ai_playwright_lab/
├── .gitignore
├── pyproject.toml              # Global dependencies configured via uv
├── uv.lock                    # Dependency lockfile
├── docs/                      # General project documentation
│   ├── start.md               # Guide/overview of the learning track
│   ├── req.md                 # Product requirements document
│   ├── architecture.md        # [This File] Architecture specification
│   └── plan.md                # Implementation roadmap
│
├── 01_open_verify/            # Subproject 1: Open and Verify Webpage
│   ├── README.md
│   └── test_open_verify.py
│
├── 02_login_form/             # Subproject 2: Login Form Automation
│   ├── README.md
│   └── test_login.py
│
├── 03_search_filter/          # Subproject 3: Search and Filter Products
│   ├── README.md
│   └── test_search_filter.py
│
├── 04_add_to_cart/            # Subproject 4: Add Product to Cart
│   ├── README.md
│   └── test_cart.py
│
├── 05_data_driven_login/      # Subproject 5: Data-Driven Login Tests
│   ├── README.md
│   ├── credentials.json       # External test data file
│   └── test_data_driven.py
│
├── 06_api_ui_validation/      # Subproject 6: API + UI Validation
│   ├── README.md
│   └── test_api_ui.py
│
├── 07_upload_download/        # Subproject 7: File Upload and Download
│   ├── README.md
│   ├── test_upload.txt        # Sample file for upload
│   └── test_files.py
│
├── 08_multi_user_approval/    # Subproject 8: Multi-User Approval Workflow
│   ├── README.md
│   ├── server.py              # Local FastAPI application simulating dashboard
│   └── test_approval.py       # Core multi-browser-context test
│
├── 09_mini_test_framework/    # Subproject 9: POM Test Framework
│   ├── README.md
│   ├── conftest.py            # Fixtures and failure hook configurations
│   ├── pages/                 # POM page classes
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   ├── inventory_page.py
│   │   └── cart_page.py
│   └── tests/
│       └── test_pom_flow.py
│
└── 10_payment_checkout/       # Subproject 10: Payment Checkout Simulation
    ├── README.md
    └── test_checkout.py
```

---

## 2. Infrastructure & Execution Architecture

### Package and Dependency Management (`uv`)
- **Single Virtual Environment**: To keep execution fast, a single project-level virtual environment is initialized at the root of the repository.
- **`uv` Toolchain**: All commands leverage `uv run` to ensure tests execute within the configured virtual environment without manually activating scripts.

### Test Runner (`pytest` & `pytest-playwright`)
- Tests are identified and run by `pytest`.
- `pytest-playwright` provides out-of-the-box fixtures (`page`, `browser`, `context`) that manage browser lifecycles efficiently.
- Global defaults (e.g., running in headless mode by default, specifying browser types) are managed via standard command-line arguments or `pytest.ini`.

---

## 3. Design Patterns & Best Practices

### 1. Page Object Model (POM)
*Applied in: Projects 9 & 10.*
- **Abstractions**: UI components and page interactions are abstracted into Python classes. Test scripts invoke method actions (e.g., `login_page.login(user, pass)`) rather than direct locator clicks.
- **Encapsulation**: Selectors are kept private to the Page Object classes. If the UI changes, only the class selectors need updating, keeping tests robust.

### 2. Multi-Context Orchestration
*Applied in: Project 8.*
- **Isolation**: Instead of a single browser session, tests utilize multiple isolated `BrowserContext` instances. 
- **Concurrency**: This simulates distinct users logging in concurrently, ensuring state updates propagate from one browser session to another without cross-contamination.

### 3. API-UI Integration
*Applied in: Project 6.*
- **`APIRequestContext`**: Playwright's native API client is used to trigger HTTP requests. 
- **Synchronization**: Dynamic response bodies are processed in memory and immediately asserted against active DOM nodes in the browser page, bridging backend and frontend validations.

### 4. Data-Driven Parametrization
*Applied in: Project 5.*
- **Decoupled Data**: Login data resides in external static files (e.g., `credentials.json`).
- **Dynamic Parametrization**: Pytest reads data before execution and generates individual test outcomes for each data block, allowing clear feedback on which datasets pass or fail.

### 5. Failure Artifact Capture
*Applied in: Projects 9 & 10.*
- **Pytest Hooks**: Hooks in `conftest.py` intercept failures.
- **Traces & Screenshots**: Screenshot capture and zip-based Playwright execution traces are saved to an outputs folder automatically upon any failure scenario.
