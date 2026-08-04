"""
Test suite for Project 11: Role-Based Employee Management Portal.
Validates admin user creation & status disabling workflows as well as multi-context
role and permission isolation between admin and employee user roles.
"""

import socket
import time
import threading
import sys
from pathlib import Path
import urllib.request
import pytest
import uvicorn
from playwright.sync_api import Browser, Page, expect

# Ensure subproject directory is in sys.path to import local server module
sys.path.insert(0, str(Path(__file__).parent))
import server


def get_free_port() -> int:
    """Utility function to discover an available local TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def server_url():
    """
    Module-scoped Pytest fixture to spin up the uvicorn FastAPI server on an ephemeral port.
    Polls the server's /health endpoint until active, and shuts it down after test completion.
    """
    port = get_free_port()
    config = uvicorn.Config(server.app, host="127.0.0.1", port=port, log_level="error")
    uv_server = uvicorn.Server(config)

    thread = threading.Thread(target=uv_server.run, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"

    # Poll /health endpoint to ensure web server is fully initialized before running tests
    start_time = time.time()
    while time.time() - start_time < 5.0:
        try:
            with urllib.request.urlopen(f"{url}/health") as resp:
                if resp.status == 200:
                    break
        except Exception:
            time.sleep(0.1)

    yield url

    uv_server.should_exit = True


@pytest.fixture
def admin_creds():
    """Fixture providing administrator credentials."""
    return {"username": "admin", "password": "admin123"}


@pytest.fixture
def employee_creds():
    """Fixture providing standard employee / sales specialist credentials."""
    return {"username": "emp_sales", "password": "emp123"}


def test_admin_disable_user(page: Page, server_url: str, admin_creds: dict):
    """
    Task 11.1: Admin User Management & Account Disabling Test Scenario.
    Steps:
    1. Navigate to portal URL and log in with admin credentials.
    2. Fill out employee creation form with name, email, and 'Sales Specialist' role.
    3. Submit form and verify user appears in table with 'Active' status.
    4. Click 'Disable' button to toggle account status to 'Disabled'.
    5. Assert table status badge reflects 'Disabled'.
    """
    # 1. Navigate to portal & login as Admin
    page.goto(server_url)
    page.fill("#username", admin_creds["username"])
    page.fill("#password", admin_creds["password"])
    page.click("#btn-login")

    # Assert Admin Dashboard is visible
    expect(page.locator("#admin-dashboard")).to_be_visible()
    expect(page.locator("#user-role-badge")).to_have_text("Admin")

    # 2. Fill employee creation form with role 'Sales Specialist'
    new_emp_name = "Charlie Brown"
    new_emp_email = "charlie@company.com"
    page.fill("#employee-name", new_emp_name)
    page.fill("#employee-email", new_emp_email)
    page.select_option("#employee-role", "Sales Specialist")
    
    # 3. Submit form and verify employee appears in directory table
    page.click("#btn-create-employee")
    created_row = page.locator("tr", has_text=new_emp_name)
    expect(created_row).to_be_visible()
    expect(created_row.locator(".user-email")).to_have_text(new_emp_email)
    expect(created_row.locator(".user-role")).to_have_text("Sales Specialist")

    # Initial status should be Active
    status_badge = created_row.locator(".status-badge")
    expect(status_badge).to_have_text("Active")

    # 4. Toggle status to Disabled
    disable_button = created_row.locator("button.btn-disable")
    disable_button.click()

    # 5. Assert table record reflects Disabled
    expect(status_badge).to_have_text("Disabled")
    expect(status_badge).to_have_class("status-badge status-disabled")


def test_employee_permissions(browser: Browser, server_url: str, employee_creds: dict):
    """
    Task 11.2: Multi-Context Role & Permission Verification Test Scenario.
    Steps:
    1. Create an isolated BrowserContext for the employee session.
    2. Log in with employee credentials.
    3. Assert visibility of role-permitted navigation tabs.
    4. Assert absence/hidden status of admin-restricted tabs and action buttons.
    """
    # 1. Create an isolated BrowserContext
    employee_context = browser.new_context()
    
    try:
        employee_page = employee_context.new_page()
        
        # 2. Navigate and log in with employee credentials
        employee_page.goto(server_url)
        employee_page.fill("#username", employee_creds["username"])
        employee_page.fill("#password", employee_creds["password"])
        employee_page.click("#btn-login")

        # Verify Employee workspace view is loaded
        expect(employee_page.locator("#employee-dashboard")).to_be_visible()
        expect(employee_page.locator("#user-role-badge")).to_have_text("Sales Specialist")

        # 3. Assert visibility of role-permitted navigation tabs
        expect(employee_page.locator("#nav-dashboard")).to_be_visible()
        expect(employee_page.locator("#nav-profile")).to_be_visible()
        expect(employee_page.locator("#nav-sales")).to_be_visible()

        # 4. Assert absence/hidden status of admin-restricted tabs & action elements
        expect(employee_page.locator("#nav-admin-settings")).to_be_hidden()
        expect(employee_page.locator("#nav-system-logs")).to_be_hidden()
        expect(employee_page.locator("#admin-dashboard")).to_be_hidden()
        expect(employee_page.locator("#btn-create-employee")).to_be_hidden()
        expect(employee_page.locator("#btn-delete-user")).to_be_hidden()

    finally:
        # Cleanly dispose of isolated browser context
        employee_context.close()
