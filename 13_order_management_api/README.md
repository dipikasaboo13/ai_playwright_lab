# Project 13: Order Management with API Setup (`13_order_management_api`)

## Description & Objectives

This project implements an Order Management system integrating RESTful API endpoints with an interactive web dashboard. It demonstrates Playwright's combined API testing capabilities (`APIRequestContext`) and UI browser automation, verifying end-to-end data consistency across API and UI layers.

### Key Objectives
- **API Test Data Seeding**: Fast, reliable pre-test setup using Playwright's `APIRequestContext` to post customer orders directly to backend REST endpoints (`POST /api/v1/orders`).
- **UI Search & Interactive Status Updates**: Locating seeded orders on the live web dashboard UI via dynamic search filtering, and modifying order status dropdowns.
- **API Cross-Validation**: Validating that UI state mutations are persisted correctly in backend storage by querying `GET /api/v1/orders/{order_id}` via API context.
- **API Teardown**: Cleaning up created test entities post-test via `DELETE /api/v1/orders/{order_id}` endpoints.

---

## Solved Test Cases

1. `test_api_order_seeding`:
   - Creates an isolated `APIRequestContext` tied to the application server.
   - Submits a customer order payload (`POST /api/v1/orders`).
   - Asserts HTTP 201 status code and validates returned `order_id` string, customer name, order total, and default `Pending` status.

2. `test_ui_search_status_update_and_api_validation`:
   - Seeds a unique customer order record via API (`POST /api/v1/orders`).
   - Opens the Order Management Dashboard in the browser.
   - Fills the search input box with the seeded `order_id` to isolate the target order row.
   - Asserts initial status badge displays `Pending`.
   - Changes status dropdown menu to `Shipped`.
   - Asserts UI badge updates dynamically to `Shipped`.
   - Cross-validates backend data persistence by performing a `GET /api/v1/orders/{order_id}` request and asserting backend status is `Shipped`.
   - Performs test teardown by calling `DELETE /api/v1/orders/{order_id}` and verifying subsequent `GET` requests return HTTP 404.

---

## Test Execution Instructions

Execute tests within the `uv` environment using the following commands:

```bash
# Run all tests in Project 13
uv run pytest 13_order_management_api/

# Run API order seeding test scenario
uv run pytest 13_order_management_api/test_order_mgmt.py -k "test_api_order_seeding"

# Run UI search & API cross-validation scenario
uv run pytest 13_order_management_api/test_order_mgmt.py -k "test_ui_search_status_update_and_api_validation"

# Run with verbose output
uv run pytest 13_order_management_api/test_order_mgmt.py -v
```

### Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 13_order_management_api.server:app --reload --port 8000
```
Once started, open your browser and navigate to:
- **Interactive Web Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Interactive OpenAPI Specs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## Parameter References & Test Data Design

### API Endpoints Reference
| HTTP Method | Path | Description | Expected Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Server health check endpoint | `200 OK` |
| `POST` | `/api/v1/orders` | Create new order record | `201 Created` |
| `GET` | `/api/v1/orders` | List all existing order records | `200 OK` |
| `GET` | `/api/v1/orders/{order_id}` | Retrieve specific order record | `200 OK` / `404 Not Found` |
| `PATCH` | `/api/v1/orders/{order_id}` | Update order status | `200 OK` / `404 Not Found` |
| `DELETE` | `/api/v1/orders/{order_id}` | Teardown / Delete order record | `200 OK` / `404 Not Found` |

### Pytest Fixtures
- `server_url` (`module` scope): Spawns the uvicorn FastAPI web server on an ephemeral local TCP port, polls `/health`, and handles post-test server exit.
- `playwright`: Pytest-Playwright fixture for instantiating `APIRequestContext` and browser contexts.
- `page`: Pytest-Playwright fixture providing browser page automation instance.
