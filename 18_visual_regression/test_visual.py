"""
Test suite for Project 18: Visual Regression Testing for Key Screens.

Validates baseline screenshot comparison, masking of dynamic UI elements (timestamps, session tokens,
live clocks, random metrics), and visual drift detection across key screens using Playwright.
"""

import socket
import sys
import time
import threading
import urllib.request
from pathlib import Path

import pytest
import uvicorn
from playwright.sync_api import Page, expect

# Ensure subproject directory is in sys.path for local server import
sys.path.insert(0, str(Path(__file__).parent))
import server

SUBPROJECT_DIR = Path(__file__).parent


def get_free_port() -> int:
    """Utility function to find an available local TCP port for the FastAPI web server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def server_url():
    """
    Module-scoped Pytest fixture that spins up the FastAPI server on an ephemeral port.
    Polls /health until server is active and shuts down cleanly after test module execution.
    """
    port = get_free_port()
    config = uvicorn.Config(server.app, host="127.0.0.1", port=port, log_level="error")
    uv_server = uvicorn.Server(config)

    thread = threading.Thread(target=uv_server.run, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"

    # Wait for server initialization
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


def test_dashboard_visual_regression(page: Page, server_url: str):
    """
    Task 18.1 & 18.2: Executive Dashboard Visual Regression Test.
    
    Navigates to the Dashboard page, masks dynamic elements (timestamps, session token, live clock,
    and active user counter) using `mask=[...]` locator array, and asserts visual consistency
    against the reference baseline snapshot.
    """
    # 1. Navigate to Executive Dashboard
    page.goto(f"{server_url}/dashboard")
    expect(page.locator("h1")).to_contain_text("Analytics & Operational Dashboard")

    # 2. Define locators for dynamic UI components that change across page reloads
    dynamic_elements = [
        page.locator("#dynamic-timestamp"),
        page.locator("#session-id"),
        page.locator("#live-clock"),
        page.locator("#active-users-count"),
    ]

    # 3. Assert visual snapshot equality with masked dynamic locators
    expect(page).to_have_screenshot(
        name="dashboard_page.png",
        mask=dynamic_elements,
        threshold=0.2,
    )


def test_checkout_visual_regression(page: Page, server_url: str):
    """
    Task 18.1 & 18.2: Payment Checkout Visual Regression Test.
    
    Navigates to the Payment Checkout screen, masks dynamic transaction reference tokens and timestamps,
    and validates layout pixel consistency against baseline image.
    """
    # 1. Navigate to Payment Checkout screen
    page.goto(f"{server_url}/checkout")
    expect(page.locator("h2")).to_contain_text("Complete Your Order")

    # 2. Define dynamic element locators for masking
    checkout_dynamic_elements = [
        page.locator("#checkout-tx-id"),
        page.locator("#checkout-timestamp"),
    ]

    # 3. Assert screenshot matching with element masking
    expect(page).to_have_screenshot(
        name="checkout_page.png",
        mask=checkout_dynamic_elements,
        threshold=0.2,
    )
