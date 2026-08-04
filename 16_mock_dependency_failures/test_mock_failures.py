"""
Test suite for Project 16: Mock External Dependency Failures.
Validates route interception for payment gateway HTTP 500 errors, network request aborts/timeouts,
artificial network delay with loading spinner assertions, and partial data fallback UI resilience using Playwright.
"""

import socket
import sys
import time
import threading
import urllib.request
from pathlib import Path

import pytest
import uvicorn
from playwright.sync_api import Page, Route, expect

# Ensure subproject directory is in sys.path to import local server module
sys.path.insert(0, str(Path(__file__).parent))
import server

SUBPROJECT_DIR = Path(__file__).parent


def get_free_port() -> int:
    """Utility function to discover an available local TCP port for the FastAPI web server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def server_url():
    """
    Module-scoped Pytest fixture to spin up the uvicorn FastAPI server on an ephemeral port.
    Polls the server's /health endpoint until active, and gracefully shuts it down after test completion.
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


def test_mock_server_error(page: Page, server_url: str):
    """
    Task 16.1 Scenario:
    Intercepts payment API calls to simulate HTTP 500 Gateway Server Errors and network request aborts.
    Asserts UI error banner display and message string validation.
    """
    # 1. Navigate to main resilience lab portal
    page.goto(server_url)
    expect(page.locator("h1")).to_contain_text("Payment & Resilience Testing Portal")

    # 2. Mock HTTP 500 Internal Server Error for payment endpoint
    def handle_500_error(route: Route):
        route.fulfill(
            status=500,
            content_type="application/json",
            body='{"error": "Internal Payment Gateway Error 500: Server Overloaded"}'
        )

    page.route("**/api/payment", handle_500_error)

    # 3. Trigger payment checkout action
    page.fill("#card-number-input", "4000 1234 5678 9010")
    page.fill("#amount-input", "150.00")
    page.click("#btn-pay-now")

    # 4. Assert error alert is displayed with expected mocked error message
    error_alert = page.locator("#error-alert")
    expect(error_alert).to_be_visible()
    expect(page.locator("#error-message")).to_contain_text("Internal Payment Gateway Error 500: Server Overloaded")

    # 5. Test network abort / connection failure scenario
    def handle_abort(route: Route):
        route.abort("failed")

    page.route("**/api/payment", handle_abort)
    page.click("#btn-pay-now")

    # Assert error banner captures network level connection failure
    expect(error_alert).to_be_visible()
    expect(page.locator("#error-message")).to_be_visible()


def test_mock_delay_resilience(page: Page, server_url: str):
    """
    Task 16.2 Scenario:
    Injects artificial network response delay (1.0s) and partial JSON payload into user-data endpoint.
    Asserts loading spinner visibility while pending and graceful fallback view trigger.
    """
    page.goto(server_url)

    # Handler to introduce artificial server delay and fulfill partial JSON response via route.continue_
    def handle_delayed_partial_response(route: Route):
        route.continue_(url=f"{server_url}/api/user-data?delay=1.0&partial=true")

    page.route("**/api/user-data", handle_delayed_partial_response)

    # Trigger user details fetch
    page.click("#btn-load-data")

    # Assert spinner is visible during pending request state
    spinner = page.locator("#dashboard-spinner")
    expect(spinner).to_be_visible()

    # Wait for response completion and assert spinner hides while fallback view triggers
    expect(spinner).to_be_hidden(timeout=5000)
    
    fallback_view = page.locator("#fallback-view")
    expect(fallback_view).to_be_visible()
    expect(page.locator("#fallback-message")).to_contain_text("Partial account data received")

    # Verify profile display container renders partial data
    profile_data = page.locator("#user-profile-data")
    expect(profile_data).to_be_visible()
    expect(profile_data).to_contain_text("USR-9999")
