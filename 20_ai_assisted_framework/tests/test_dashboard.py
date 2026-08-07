"""
Dashboard Test Suite for Project 20 AI-Assisted Test Framework.
Validates metric cards, product search, checkout navigation, and logout workflow.
"""

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.mark.regression
def test_dashboard_metrics_display(page: Page, server_url: str):
    """
    Verify dashboard metric cards (Sales, Users, Orders) render accurate starting values.
    """
    login_page = LoginPage(page, base_url=server_url)
    dashboard_page = DashboardPage(page)

    login_page.navigate_to_login()
    login_page.login("john_doe", "password123")

    metrics = dashboard_page.get_metrics()
    assert metrics["sales"] == "$12,450.00"
    assert metrics["users"] == "1,280"
    assert metrics["orders"] == "42"


@pytest.mark.regression
def test_dashboard_product_search(page: Page, server_url: str):
    """
    Verify product search query renders expected query summary box.
    """
    login_page = LoginPage(page, base_url=server_url)
    dashboard_page = DashboardPage(page)

    login_page.navigate_to_login()
    login_page.login("john_doe", "password123")

    search_query = "Playwright License"
    dashboard_page.search_product(search_query)

    search_result = dashboard_page.get_search_results_text()
    assert search_query in search_result


@pytest.mark.regression
def test_dashboard_navigation_and_logout(page: Page, server_url: str):
    """
    Verify clicking logout on dashboard returns user back to sign-in page.
    """
    login_page = LoginPage(page, base_url=server_url)
    dashboard_page = DashboardPage(page)

    login_page.navigate_to_login()
    login_page.login("admin", "admin123")

    dashboard_page.logout()

    expect(page).to_have_url(f"{server_url}/login")
