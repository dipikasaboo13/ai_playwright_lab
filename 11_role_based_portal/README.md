# Project 11: Role-Based Employee Management Portal (`11_role_based_portal`)

## Description & Objectives

This project implements an enterprise Role-Based Employee Management Portal and automated test suite using Playwright Python. The portal provides multi-role functionality (Admin vs. Employee / Sales Specialist) with dynamic permissions, employee creation, and status management.

### Key Objectives
- **Admin Management Workflow**: Test profile creation for new employees and toggle account status between `Active` and `Disabled`.
- **Multi-Context Session Isolation**: Verify role-based UI component visibility and action restriction using isolated Playwright `BrowserContext` instances.
- **REST & UI Integration**: Integrate FastAPI backend routes (`/api/login`, `/api/users`, `/api/users/{user_id}/status`) with an interactive frontend.

---

## Solved Test Cases

1. `test_admin_disable_user`:
   - Authenticates as Administrator.
   - Fills out the employee creation form with full name, email, and role `Sales Specialist`.
   - Submits form and verifies new entry in the employee directory table.
   - Toggles status to `Disabled` and asserts that the status badge updates accordingly.

2. `test_employee_permissions`:
   - Launches an isolated `BrowserContext` simulating an employee session.
   - Authenticates as `Sales Specialist`.
   - Verifies visibility of permitted tabs (`#nav-dashboard`, `#nav-profile`, `#nav-sales`).
   - Asserts strict absence/hiding of admin-restricted tabs (`#nav-admin-settings`, `#nav-system-logs`) and action controls (`#btn-create-employee`, `#btn-delete-user`).

---

## Test Execution Instructions

Run tests within the `uv` environment using the following commands:

```bash
# Run all tests in Project 11
uv run pytest 11_role_based_portal/

# Run specific Admin Disable scenario
uv run pytest 11_role_based_portal/test_role_portal.py -k "test_admin_disable_user"

# Run Multi-Context Employee Permissions scenario
uv run pytest 11_role_based_portal/test_role_portal.py -k "test_employee_permissions"

# Run across all supported browser engines
uv run pytest 11_role_based_portal/ --browser=all
```

---

## Parameter References & Test Data Design

### Default Credentials
| Username | Password | Role | Access Level |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | `Admin` | Full management, user creation, status toggle, admin settings |
| `emp_sales` | `emp123` | `Sales Specialist` | Workspace, sales metrics, restricted admin controls |

### Pytest Fixtures
- `server_url` (`module` scope): Spawns the uvicorn web server on an available local port and waits for `/health`.
- `admin_creds`: Provides dictionary of admin login credentials.
- `employee_creds`: Provides dictionary of standard employee credentials.

### API Endpoints
- `GET /health` - Server health status check.
- `POST /api/login` - Authenticates user credentials.
- `GET /api/users` - Fetches list of all registered employees.
- `POST /api/users` - Creates a new employee record.
- `PATCH /api/users/{user_id}/status` - Updates employee status (`Active` / `Disabled`).
