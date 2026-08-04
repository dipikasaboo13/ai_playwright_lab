# Project 19: Payment Transaction Lifecycle Simulation (`19_payment_lifecycle`)

## Overview & Objectives

Project 19 automates and validates full-lifecycle payment transaction processing state machines and customer ledger balance accounting math using Playwright Python.

### Key Objectives:
1. **End-to-End State Machine Transition**: Automate payment charge initiation and transition status through `Initiated` -> `Authorized` -> `Pending` -> `Completed` state machine.
2. **Ledger Balance Math Verification**: Validate customer ledger balance calculations upon payment charge completion (e.g. $1000.00 starting balance - $150.00 charge = $850.00 final balance).
3. **Transaction Reversal & Refund Handling**: Process full/partial refunds for completed transactions, verifying status updates to `Refunded` and restoration of ledger balance.

---

## Solved Test Cases & Scenarios

| Test Case Name | Objective / Scenario Covered | Validation Method |
| :--- | :--- | :--- |
| `test_payment_completion` | Initiates charge via UI form, transitions status state machine, and verifies ledger balance reduction ($1000.00 -> $850.00). | Playwright `Page`, `expect(ledger_balance).to_have_text("$850.00")`, and transaction status assertions. |
| `test_payment_refund` | Completes transaction, executes full refund via modal, and verifies ledger balance restoration back to $1,000.00. | Playwright `Page`, modal form interactions, `expect(ledger_balance).to_have_text("$1,000.00")`, and `Refunded` status badge assertions. |

---

## Technical Stack & Architecture

- **Web Server Framework**: FastAPI + Uvicorn (running on an ephemeral local TCP port).
- **Automation Engine**: Playwright Sync API (`Page`, `expect`).
- **State Management**: In-memory ledger balance and transaction state machine store.
- **Test Runner**: Pytest with module-scoped server fixtures and autouse reset fixtures.

---

## Command-Line Execution Instructions

Run all test execution commands using `uv` environment wrapper:

### 1. Run All Tests in Subproject
```bash
uv run pytest 19_payment_lifecycle/
```

### 2. Run Payment Completion Test Scenario
```bash
uv run pytest 19_payment_lifecycle/test_payment_lifecycle.py -k "test_payment_completion"
```

### 3. Run Transaction Refund Test Scenario
```bash
uv run pytest 19_payment_lifecycle/test_payment_lifecycle.py -k "test_payment_refund"
```

### 4. Run with HTML Report Generation
```bash
uv run pytest 19_payment_lifecycle/ --html=report.html --self-contained-html
```

### Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 19_payment_lifecycle.server:app --reload --port 8000
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
- **`reset_server_state`** (`autouse` per test):
  - Sends HTTP POST request to `/api/reset` to restore ledger balance to $1,000.00 and clear active transactions prior to each test run.

### Key Element Locators & API Endpoints
- **UI Locators**:
  - Ledger Balance Container: `#ledger-balance`
  - Card Number Input: `#card-number`
  - Card Expiry Input: `#card-expiry`
  - Amount Input: `#charge-amount`
  - Description Input: `#charge-desc`
  - Initiate Payment Button: `#btn-initiate-payment`
  - Authorize Button: `#btn-authorize`
  - Pending Button: `#btn-pending`
  - Complete Button: `#btn-complete`
  - Auto-Run Lifecycle Button: `#btn-auto-lifecycle`
  - Refund Button: `#btn-refund`
  - Refund Modal: `#refund-modal`
  - Refund Amount Input: `#refund-amount-input`
  - Confirm Refund Button: `#btn-confirm-refund`
  - Transaction Table Body: `#transaction-table-body`
  - Active Transaction ID: `#active-tx-id`
- **Backend Endpoints**:
  - Web UI Portal: `GET /`
  - Health Check: `GET /health`
  - Fetch Ledger: `GET /api/ledger`
  - Initiate Payment: `POST /api/payment/initiate`
  - Authorize Payment: `POST /api/payment/authorize`
  - Process Pending Payment: `POST /api/payment/process`
  - Complete Payment: `POST /api/payment/complete`
  - Refund Payment: `POST /api/payment/refund`
  - Reset Ledger: `POST /api/reset`
