# Project 20: AI-Assisted Test Automation Framework (`20_ai_assisted_framework`)

## Overview & Objectives

Project 20 demonstrates an **AI-Assisted Test Automation Framework** built with Playwright Python, Pytest, and Page Object Model (POM) design patterns. The subproject includes a self-contained local web application (`server.py`) with authentication, interactive dashboard metrics, product search, cart summary, promo code calculation, and order confirmation flows.

The framework features:
1. **Modular Page Object Models**: `BasePage`, `LoginPage`, `DashboardPage`, and `CheckoutPage` encapsulating page locators and interaction logic.
2. **Structured AI-Generated Dataset Integration**: Static JSON matrix (`data/ai_generated_dataset.json`) containing `positive`, `negative`, `boundary`, and `exception` test scenarios loaded dynamically via `utils/data_loader.py`.
3. **Automated Tracing & Failure Artifact Capture**: Pytest hooks in `conftest.py` that automatically launch Playwright context tracing for every test and capture PNG screenshots (`artifacts/screenshots/`) and ZIP trace archives (`artifacts/traces/`) on test failures.
4. **HTML Test Reporting**: Native integration with `pytest-html` generating standalone HTML execution reports (`report.html`).

---

## Project Structure

```
20_ai_assisted_framework/
├── README.md                          # Project documentation and guide
├── server.py                          # Local FastAPI target web application
├── config.py                          # Centralized framework configuration & path references
├── conftest.py                        # Pytest server lifecycle, tracing, & failure hooks
├── data/
│   └── ai_generated_dataset.json     # Static AI-generated test data matrix
├── pages/
│   ├── __init__.py
│   ├── base_page.py                  # Base Page Object with Playwright wrappers
│   ├── login_page.py                 # Login Page Object
│   ├── dashboard_page.py             # Dashboard Page Object
│   └── checkout_page.py              # Checkout Page Object
├── utils/
│   ├── __init__.py
│   └── data_loader.py                # AI dataset parser and filtering utility
└── tests/
    ├── __init__.py
    ├── test_login.py                 # Smoke & regression tests for authentication
    ├── test_dashboard.py             # Regression tests for metrics and search
    ├── test_checkout.py              # Smoke & regression tests for cart & promo codes
    └── test_ai_dataset_runner.py     # Parameterized runner iterating through AI dataset
```

---

## Solved Test Scenarios

| Test File | Test Case Name | Category / Tag | Objective / Description |
|---|---|---|---|
| `test_login.py` | `test_successful_login` | `smoke`, `regression` | Verifies valid admin credentials authenticate and redirect to dashboard. |
| `test_login.py` | `test_invalid_login_credentials` | `regression` | Asserts error banner on incorrect password attempt. |
| `test_login.py` | `test_login_boundary_empty_fields` | `regression` | Asserts error banner when logging in with non-existent user. |
| `test_dashboard.py` | `test_dashboard_metrics_display` | `regression` | Validates dashboard metric cards render correct starting amounts. |
| `test_dashboard.py` | `test_dashboard_product_search` | `regression` | Validates product search input and result container rendering. |
| `test_dashboard.py` | `test_dashboard_navigation_and_logout` | `regression` | Verifies logout button returns user back to login page. |
| `test_checkout.py` | `test_checkout_valid_promo_discount` | `smoke`, `regression` | Tests applying valid promo code `AI20` (20% off) and total calculation. |
| `test_checkout.py` | `test_checkout_invalid_promo_code` | `regression` | Tests applying invalid promo code triggers error banner. |
| `test_checkout.py` | `test_checkout_order_completion` | `smoke`, `regression` | Verifies order completion generates reference confirmation code. |
| `test_ai_dataset_runner.py` | `test_ai_generated_scenario` | `regression`, `ai_generated` | Parameterized test runner executing 10 AI dataset cases (`POS-001` to `EXC-002`). |

---

## Command-Line Execution Instructions

Always run tests within the `uv` environment.

### 1. Execute Tagged Smoke Suite with HTML Report
```bash
uv run pytest 20_ai_assisted_framework/tests/ --html=report.html --self-contained-html -m smoke
```

### 2. Execute Full Regression Test Suite
```bash
uv run pytest 20_ai_assisted_framework/tests/ --html=report.html --self-contained-html
```

### 3. Execute Only AI-Generated Dataset Scenarios
```bash
uv run pytest 20_ai_assisted_framework/tests/test_ai_dataset_runner.py -m ai_generated
```

### 4. Execute Specific Test Keyword Pattern
```bash
uv run pytest 20_ai_assisted_framework/tests/ -k "promo"
```

### Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 20_ai_assisted_framework.server:app --reload --port 8000
```
Once started, open your browser and navigate to:
- **Interactive Web Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Interactive OpenAPI Specs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## Key Parameter Reference & Credentials

### Default User Credentials
- `admin` / `admin123` (Admin User)
- `john_doe` / `password123` (Standard User)
- `qa_tester` / `playwright2026` (QA Tester)

### Valid Promo Codes
- `AI20`: 20% discount
- `HALFPRICE`: 50% discount
- `SUPER100`: 100% discount (Boundary test)

### AI Dataset Categories
- **`positive`**: Standard user interactions expected to succeed.
- **`negative`**: Invalid credentials or non-existent discount codes.
- **`boundary`**: Edge cases such as whitespace padding or 100% discount boundaries.
- **`exception`**: Injection attack vectors (SQLi, XSS) and malformed payloads.
