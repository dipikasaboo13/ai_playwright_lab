# Project 8: Multi-User Approval Workflow (`08_multi_user_approval`)

## Project Description & Objectives
This project demonstrates orchestrating multi-user web workflows in Playwright Python using isolated browser contexts. 
It includes a local mock backend server built with FastAPI that provides dynamic request creation and approval APIs alongside a real-time web portal UI. The test suite simulates a real-world multi-role business process where one user (Requester) submits a financial/equipment request and another independent user (Approver) reviews and approves it in real time.

## Architecture & Design
- **Mock Backend Server (`server.py`)**: Built with FastAPI and served via `uvicorn`. Exposes REST API endpoints (`/api/requests`, `/api/requests/{id}/approve`, `/health`) and serves an interactive web dashboard with automatic state polling (`setInterval`).
- **Multi-Context Orchestration (`test_approval.py`)**: Uses Playwright's `browser.new_context()` to launch two completely independent, un-shared browser sessions (`user_a_context` and `user_b_context`).
- **Dynamic State Sync**: Verifies that state mutations performed by User B (Approval) instantly reflect on User A's view via real-time frontend updates.

## Solved Test Cases
- `test_multi_user_approval_workflow`:
  1. **User A Request Submission**: User A opens the web portal, submits a request for `"MacBook Pro Purchase"` ($2,499.99), and verifies the request status is initially `"Pending"`.
  2. **User B Queue Inspection**: User B opens the portal in a separate browser context, sees User A's request listed in the queue with status `"Pending"`.
  3. **User B Approval**: User B clicks the `"Approve"` button and confirms the status updates to `"Approved"`.
  4. **User A Real-Time Synchronization**: Asserts User A's page automatically updates to show the status `"Approved"` without requiring a manual page refresh.

## Command-Line Execution Instructions

Run the complete Project 8 test suite:
```bash
uv run pytest 08_multi_user_approval/test_approval.py -v
```

Run with verbose logging or output printing:
```bash
uv run pytest 08_multi_user_approval/test_approval.py -v -s
```

## Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 08_multi_user_approval.server:app --reload --port 8000
```
Once started, open your browser and navigate to:
- **Interactive Web Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Interactive OpenAPI Specs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


## Key Parameter References & Test Data Design

| Field Name | Type | Description | Sample Test Input |
|---|---|---|---|
| `title` | `str` | Title/description of approval request | `"MacBook Pro Purchase"` |
| `amount` | `float` | Amount requested in USD | `2499.99` |
| `status` | `str` | Workflow state (`"Pending"`, `"Approved"`) | `"Pending"` → `"Approved"` |
| `user_a_context` | `BrowserContext` | Isolated browser context for Requester role | N/A |
| `user_b_context` | `BrowserContext` | Isolated browser context for Approver role | N/A |
