# Project 5: Data-Driven Login Tests (`05_data_driven_login`)

## Description & Objectives
This subproject demonstrates data-driven testing using Playwright with `pytest` parameterization. Test data is decoupled from test logic and loaded dynamically from an external JSON file (`credentials.json`), executing multiple scenarios (valid user, locked-out user, invalid credentials) in a clean, maintainable structure.

## Scenarios Covered
1. **Standard User Login (Positive Path)**:
   - Navigates to SauceDemo login page.
   - Enters valid credentials (`standard_user` / `secret_sauce`).
   - Verifies successful login and redirection to inventory page (`/inventory.html`).
2. **Locked Out User (Negative Path)**:
   - Enters credentials for a locked-out account (`locked_out_user`).
   - Verifies that the login fails and displays the expected error message (`Sorry, this user has been locked out.`).
3. **Invalid User (Negative Path)**:
   - Enters non-existent or incorrect credentials (`invalid_user` / `wrong_password`).
   - Verifies that login fails with an error indicating unmatched credentials.

## Setup & File Structure
- `credentials.json`: Contains the dataset of test user credentials, expected status (`should_succeed`), expected URL patterns, or expected error messages.
- `test_data_driven.py`: Pytest test suite using `@pytest.mark.parametrize` to dynamically generate test runs per dataset record.
- `README.md`: Subproject documentation and execution guide.

## Command-Line Execution

To run all data-driven login tests in this subproject:

```bash
uv run pytest 05_data_driven_login/test_data_driven.py
```

To run verbose test output showing parameterized test IDs:

```bash
uv run pytest -v 05_data_driven_login/test_data_driven.py
```

## Key Parameter References & Test Data Schema
Each record in `credentials.json` follows this JSON structure:

```json
{
  "username": "<string>",
  "password": "<string>",
  "should_succeed": <boolean>,
  "expected_url_substring": "<optional string>",
  "expected_error": "<optional string>"
}
```
