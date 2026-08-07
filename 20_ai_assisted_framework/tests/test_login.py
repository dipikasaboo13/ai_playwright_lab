"""
Login Test Suite for Project 20 AI-Assisted Test Framework.
Validates successful authentication, error alerts on invalid credentials, and boundary handling.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.mark.smoke
@pytest.mark.regression
def test_successful_login(page: Page, server_url: str):
    """
    Verify valid credentials authenticate successfully and redirect to dashboard.
    
    Fixtures:
        page: Playwright Page object.
        server_url: Base URL of running FastAPI target app.
    """
    login_page = LoginPage(page, base_url=server_url)
    dashboard_page = DashboardPage(page)

    # 1. Navigate to login page
    login_page.navigate_to_login()

    # 2. Execute login with valid admin credentials
    login_page.login("admin", "admin123")

    # 3. Assert URL redirection and dashboard welcome element
    expect(page).to_have_url(f"{server_url}/dashboard?user=admin")
    assert dashboard_page.get_current_username() == "admin"


@pytest.mark.regression
def test_invalid_login_credentials(page: Page, server_url: str):
    """
    Verify invalid credentials trigger error banner message and remain on login page.
    """
    login_page = LoginPage(page, base_url=server_url)

    # 1. Navigate to login page
    login_page.navigate_to_login()

    # 2. Execute login with invalid password
    login_page.login("admin", "wrongpass999")

    # 3. Assert error banner presence and message text
    assert login_page.is_error_visible()
    assert login_page.get_error_message() == "Invalid username or password."


@pytest.mark.regression
def test_login_boundary_empty_fields(page: Page, server_url: str):
    """
    Verify attempt with non-existent user returns error notification.
    """
    login_page = LoginPage(page, base_url=server_url)

    login_page.navigate_to_login()
    login_page.login("unknown_user_99", "nopassword")

    assert login_page.is_error_visible()
    assert login_page.get_error_message() == "Invalid username or password."
