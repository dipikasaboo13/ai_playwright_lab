# Project 16: Mock External Dependency Failures (`16_mock_dependency_failures`)

## Overview & Objectives

Project 16 demonstrates route interception, network mock injection, external service failure simulation, artificial network latency handling, and fallback UI resilience testing using Playwright Python.

### Key Objectives:
1. **Payment Gateway Server Error & Network Abort Interception**: Intercept outbound payment requests (`/api/payment`) using Playwright `page.route()`, fulfilling them with HTTP 500 error payloads or aborting requests to verify error banner rendering.
2. **Artificial Latency & Spinner Verification**: Inject artificial network response delays (1.5s+) to test loading spinner display during pending request states.
3. **Partial Data & Fallback View Resilience**: Return degraded/partial JSON payloads to test client-side resilience and graceful fallback UI activation.

---

## Solved Test Cases & Scenarios

| Test Case Name | Objective / Scenario Covered | Validation Method |
| :--- | :--- | :--- |
| `test_mock_server_error` | Intercept `/api/payment` with HTTP 500 status code and `route.abort("failed")`. | Playwright `page.route()`, `route.fulfill()`, `route.abort()`, and `expect(page.locator("#error-alert")).to_be_visible()`. |
| `test_mock_delay_resilience` | Inject 1.5s network delay and partial JSON data payload into `/api/user-data`. | Playwright `page.route()`, `expect(page.locator("#dashboard-spinner")).to_be_visible()`, and fallback view assertions. |

---

## Technical Stack & Architecture

- **Web Server Framework**: FastAPI + Uvicorn (running on an ephemeral local TCP port).
- **Automation Engine**: Playwright Sync API (`Page`, `Route`, `expect`).
- **Mock Interception API**: `page.route()`, `route.fulfill()`, `route.abort()`.
- **Test Runner**: Pytest with module-scoped server fixtures.

---

## Command-Line Execution Instructions

Run all test execution commands using `uv` environment wrapper:

### 1. Run All Tests in Subproject
```bash
uv run pytest 16_mock_dependency_failures/
```

### 2. Run Payment Gateway HTTP 500 & Abort Error Test
```bash
uv run pytest 16_mock_dependency_failures/test_mock_failures.py -k "test_mock_server_error"
```

### 3. Run Response Delay & Partial Data Fallback Test
```bash
uv run pytest 16_mock_dependency_failures/test_mock_failures.py -k "test_mock_delay_resilience"
```

### 4. Run with HTML Report Generation
```bash
uv run pytest 16_mock_dependency_failures/ --html=report.html --self-contained-html
```

### Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 16_mock_dependency_failures.server:app --reload --port 8000
```
Once started, open your browser and navigate to:
- **Interactive Web Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## Fixture & Parameter References

### Pytest Fixtures
- **`server_url`** (`module` scope):
  - Spawns the FastAPI application on an isolated background thread via Uvicorn on a free TCP port.
  - Polls `/health` endpoint until server responds HTTP 200 before test execution begins.
  - Gracefully shuts down Uvicorn server after all module tests complete.

### Key Element Locators & API Endpoints
- **UI Locators**:
  - Checkout Form: `#checkout-form`
  - Card Input: `#card-number-input`
  - Amount Input: `#amount-input`
  - Pay Button: `#btn-pay-now`
  - Payment Spinner: `#payment-spinner`
  - Error Alert Banner: `#error-alert`
  - Error Message Span: `#error-message`
  - Success Alert Banner: `#success-alert`
  - Fetch Details Button: `#btn-load-data`
  - Dashboard Spinner: `#dashboard-spinner`
  - Fallback View Banner: `#fallback-view`
  - Fallback Message Span: `#fallback-message`
  - Profile Data Display: `#user-profile-data`
- **Backend Endpoints**:
  - Web UI Portal: `GET /`
  - Payment API: `POST /api/payment`
  - User Data API: `GET /api/user-data`
  - Health Check: `GET /health`
