# Project 12: End-to-End Travel Booking Flow (`12_travel_booking`)

## Overview
This subproject automates an end-to-end travel booking workflow on a modern flight/hotel booking application. It covers multi-step search interactions, interactive date selection, budget and rating filter application, passenger details form submission, automated validation error checks, and confirmation details verification.

---

## Solved Test Cases & Scenarios

### 1. Successful Travel Search & Booking (`test_successful_booking`)
- **Objective**: Validate the full journey from origin/destination selection to flight booking confirmation.
- **Workflow**:
  1. Open travel booking portal and select origin (`JFK`) and destination (`CDG`).
  2. Pick departure and return dates via date picker widgets.
  3. Adjust maximum budget slider (`#max-price`) and star rating filter (`#min-rating`).
  4. Search flights and select an available package (`#btn-select-flight-1`).
  5. Enter passenger name, email, and phone number in the checkout form.
  6. Submit form and verify booking confirmation screen appears with reference code (`TB-XXXXXX`) and computed total price (`$605.00`).

### 2. Form Validation & Date Alerts (`test_booking_validations`)
- **Objective**: Ensure robust input validation for invalid travel dates and missing passenger information.
- **Workflow**:
  1. Attempt flight search with return date set prior to departure date.
  2. Assert alert banner (`#date-error-alert`) is displayed with message: *"Return date cannot be earlier than departure date"*.
  3. Reset travel dates to valid inputs, search, and proceed to passenger form.
  4. Submit passenger form without filling required fields.
  5. Assert inline validation error messages for name, email, and phone inputs.

---

## Execution Instructions

Run test scenarios using `uv`:

```bash
# Run successful booking test scenario
uv run pytest 12_travel_booking/test_travel_booking.py -k "test_successful_booking"

# Run form validation & error scenario
uv run pytest 12_travel_booking/test_travel_booking.py -k "test_booking_validations"

# Run all tests in Project 12 subproject
uv run pytest 12_travel_booking/
```

### Standalone Server Execution

To launch the FastAPI application server individually for manual web exploration:

```bash
uv run uvicorn 12_travel_booking.server:app --reload --port 8000
```
Once started, open your browser and navigate to:
- **Interactive Web Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Interactive OpenAPI Specs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)


---

## Parameter & Locator Reference

| Element / Locator | Type | Description |
| :--- | :--- | :--- |
| `#origin` | Select | Dropdown for departure airport/city |
| `#destination` | Select | Dropdown for arrival airport/city |
| `#departure-date` | Input (date) | Travel start date picker |
| `#return-date` | Input (date) | Travel end date picker |
| `#max-price` | Input (range) | Maximum budget price slider |
| `#min-rating` | Select | Minimum star rating filter dropdown |
| `#btn-search` | Button | Triggers flight package search |
| `#date-error-alert` | Div/Alert | Warning banner for invalid date ranges |
| `#btn-select-flight-1` | Button | Selects first available flight package |
| `#passenger-name` | Input (text) | Passenger full name field |
| `#passenger-email` | Input (email) | Passenger email field |
| `#passenger-phone` | Input (tel) | Passenger phone number field |
| `#btn-confirm-booking` | Button | Submits booking details |
| `#passenger-name-error` | Div | Inline validation message for name field |
| `#passenger-email-error` | Div | Inline validation message for email field |
| `#booking-reference` | Element | Generated booking confirmation code (`TB-XXXXXX`) |
| `#total-price` | Element | Calculated total price display including base fare & taxes |

---

## Pytest Fixtures Used
- `server_url`: Module-scoped fixture that launches the uvicorn FastAPI server (`server.py`) on an ephemeral TCP port and waits for `/health` readiness.
- `page`: Playwright isolated browser page fixture for automated user interaction.
