# Project 6: API + UI Validation (`06_api_ui_validation`)

## Description & Objectives
This subproject demonstrates cross-layer verification by combining Playwright API testing capability (`APIRequestContext`) with UI browser automation (`Page`). It retrieves product data payloads directly from the backend API endpoints and validates that the frontend DOM elements render matching titles and price values.

## Scenarios Covered
1. **API Query Setup (`test_api_query_setup`)**:
   - Sends an HTTP request to `https://api.demoblaze.com/entries`.
   - Validates response code `200 OK`.
   - Parses the returned JSON payload and extracts product titles and prices into an in-memory dictionary data structure.

2. **Frontend Matching Assertions (`test_frontend_matching_assertions`)**:
   - Queries the backend API catalog to obtain the source-of-truth product list and pricing.
   - Launches a browser instance and navigates to the Demoblaze catalog homepage (`https://demoblaze.com/`).
   - Locates product elements (`.card`) in the DOM and extracts visible product titles (`.card-title a`) and prices (`h5`).
   - Asserts that every UI-displayed item exists in the API catalog response and that displayed price amounts match expected API values.

## Setup & File Structure
- `test_api_ui.py`: Pytest test suite performing API request queries and UI cross-layer assertions.
- `README.md`: Subproject documentation and execution guide.

## Command-Line Execution

To run all tests in this subproject:

```bash
uv run pytest 06_api_ui_validation/test_api_ui.py
```

To run a specific test scenario:

```bash
uv run pytest 06_api_ui_validation/test_api_ui.py -k "test_api_query_setup"
uv run pytest 06_api_ui_validation/test_api_ui.py -k "test_frontend_matching_assertions"
```

To run in verbose mode:

```bash
uv run pytest -v 06_api_ui_validation/test_api_ui.py
```

## Key Parameter References & Test Data Design
- **API Endpoint**: `https://api.demoblaze.com/entries`
- **UI Endpoint**: `https://demoblaze.com/`
- **API Payload Keys**: `Items` array containing objects with `title` and `price`.
- **UI DOM Selectors**:
  - Card container: `.card`
  - Title link: `.card-title a`
  - Price label: `h5`
