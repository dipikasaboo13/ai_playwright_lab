# 02_login_form: Login Form Automation

## Description & Objectives
This subproject automates authentication flows on the SauceDemo login page (`https://www.saucedemo.com/`) using Playwright Python and `pytest`. It verifies both positive login redirection and negative error validation scenarios.

## Solved Test Scenarios
- **Success Login Test Scenario (`test_successful_login`)**: 
  - Navigates to `https://www.saucedemo.com/`.
  - Enters valid user credentials (`standard_user` / `secret_sauce`).
  - Clicks the login button and asserts redirection to the inventory landing page (`/inventory.html`).
- **Failure Login Test Scenario (`test_failed_login`)**:
  - Navigates to `https://www.saucedemo.com/`.
  - Enters invalid user credentials (`invalid_user` / `invalid_password`).
  - Clicks the login button and verifies the visibility and dynamic error text of the validation element (`[data-test='error']`).

## Test Execution Commands

Run all tests in this subproject:
```bash
uv run pytest 02_login_form/
```

Run specific test file:
```bash
uv run pytest 02_login_form/test_login.py
```

Run positive login scenario:
```bash
uv run pytest 02_login_form/test_login.py -k "test_successful_login"
```

Run negative login scenario:
```bash
uv run pytest 02_login_form/test_login.py -k "test_failed_login"
```

## Parameter Reference & Test Data
- **Target URL**: `https://www.saucedemo.com/`
- **Expected Success URL**: `https://www.saucedemo.com/inventory.html`
- **Valid Credentials**:
  - Username: `standard_user`
  - Password: `secret_sauce`
- **Invalid Credentials**:
  - Username: `invalid_user`
  - Password: `invalid_password`
- **Key Locators**:
  - Username input: `#user-name`
  - Password input: `#password`
  - Login button: `#login-button`
  - Error banner: `[data-test='error']`
