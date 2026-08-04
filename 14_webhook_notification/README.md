# Project 14: Webhook and Notification Validation (`14_webhook_notification`)

## Overview & Objectives

Project 14 demonstrates end-to-end automation strategies for intercepting outbound asynchronous Webhook HTTP requests and validating real-time in-app DOM Toast Notifications using Playwright Python.

### Key Objectives:
1. **Network Request Interception**: Intercept outbound `POST` network requests to verify webhook dispatches without relying solely on backend logs.
2. **Payload Structure Validation**: Assert that outbound webhook payloads strictly adhere to JSON contract standards containing top-level keys (`event_type`, `timestamp`, `data`).
3. **DOM Toast Notification Assertions**: Locate dynamic, temporary toast UI notification elements and verify real-time status feedback.

---

## Solved Test Cases & Scenarios

| Test Case Name | Objective / Scenario Covered | Validation Method |
| :--- | :--- | :--- |
| `test_webhook_payload` | Trigger UI event, intercept outbound HTTP POST request to `/api/v1/webhook`, and validate JSON body schema. | Playwright `page.expect_request` & JSON key/value assertions (`event_type`, `timestamp`, `data`). |
| `test_ui_notification` | Submit event form and verify real-time toast alert message rendering on DOM. | Playwright `expect(page.locator("#toast-notification")).to_be_visible()` and text content assertion. |

---

## Technical Stack & Architecture

- **Web Server Framework**: FastAPI + Uvicorn (running asynchronously on an ephemeral local TCP port).
- **Automation Engine**: Playwright Sync API (`Page`, `Request`, `expect`).
- **Test Runner**: Pytest with custom module-scoped server fixtures.

---

## Command-Line Execution Instructions

Run all commands using `uv` to ensure proper environment isolation:

### 1. Run All Tests in Subproject
```bash
uv run pytest 14_webhook_notification/
```

### 2. Run Webhook Payload Interception Test
```bash
uv run pytest 14_webhook_notification/test_webhook_notification.py -k "test_webhook_payload"
```

### 3. Run UI Toast Notification Test
```bash
uv run pytest 14_webhook_notification/test_webhook_notification.py -k "test_ui_notification"
```

### 4. Run with HTML Report Generation
```bash
uv run pytest 14_webhook_notification/ --html=report.html --self-contained-html
```

### Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 14_webhook_notification.server:app --reload --port 8000
```
Once started, open your browser and navigate to:
- **Interactive Web Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Interactive OpenAPI Specs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## Fixture & Parameter References

### Pytest Fixtures
- **`server_url`** (`module` scope):
  - Automatically identifies a free TCP port using `get_free_port()`.
  - Spawns the FastAPI application on an isolated background thread via Uvicorn.
  - Polls `/health` endpoint until server responds HTTP 200 before test execution begins.
  - Gracefully shuts down Uvicorn server after all module tests complete.

### Key Element Locators & API Endpoints
- **UI Locators**:
  - Event Selector: `#event-type-select`
  - Recipient Email Input: `#recipient-email`
  - Custom Note Input: `#custom-note`
  - Submit Button: `#btn-trigger-webhook`
  - Toast Notification Container: `#toast-notification`
  - Toast Message Span: `#toast-notification .toast-message`
- **Backend Endpoints**:
  - Web UI Dashboard: `GET /`
  - Webhook Receiver: `POST /api/v1/webhook`
  - Event Trigger API: `POST /api/v1/trigger-event`
  - Webhook History API: `GET /api/v1/webhooks`
  - Server Health Check: `GET /health`

---

## Test Data Design

### Webhook Event Payload Schema
```json
{
  "event_type": "order_created",
  "timestamp": "2026-08-04T19:59:00.000Z",
  "data": {
    "order_id": "ORD-58492",
    "recipient_email": "test.developer@example.com",
    "status": "PROCESSED",
    "note": "Automated Playwright Webhook Payload Verification"
  }
}
```
