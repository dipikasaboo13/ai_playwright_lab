"""
Test suite for Project 12: End-to-End Travel Booking Flow.
Validates multi-step travel searching, date picker selection, price & rating filters,
passenger booking form submission, confirmation details validation, and input validation handling.
"""

import socket
import time
import threading
import sys
from pathlib import Path
import urllib.request
import pytest
import uvicorn
from playwright.sync_api import Page, expect

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


def test_successful_booking(page: Page, server_url: str):
    """
    Task 12.1: Successful Travel Search & Booking Test Scenario.
    Steps:
    1. Navigate to booking portal and select origin/destination locations.
    2. Pick travel dates from interactive date picker.
    3. Apply price slider and minimum rating filters to narrow search results.
    4. Execute flight package search and select preferred flight option.
    5. Fill passenger information form with complete contact details and submit.
    6. Assert confirmation reference code is generated and total price calculation is correct.
    """
    # 1. Navigate to booking portal
    page.goto(server_url)
    expect(page.locator("h1")).to_contain_text("SkyWay Travel Booking Portal")

    # Select origin & destination
    page.select_option("#origin", "JFK")
    page.select_option("#destination", "CDG")

    # 2. Pick travel dates
    page.fill("#departure-date", "2026-09-10")
    page.fill("#return-date", "2026-09-20")

    # 3. Apply price and rating filters
    # Set max price to $600
    page.fill("#max-price", "600")
    page.select_option("#min-rating", "4")

    # 4. Search flights
    page.click("#btn-search")
    expect(page.locator("#search-results-section")).to_be_visible()

    # Select flight package (Flight ID 1: Air France Express @ $550)
    select_btn = page.locator("#btn-select-flight-1")
    expect(select_btn).to_be_visible()
    select_btn.click()

    # 5. Fill passenger information form
    expect(page.locator("#passenger-form-section")).to_be_visible()
    page.fill("#passenger-name", "Alice Johnson")
    page.fill("#passenger-email", "alice.johnson@example.com")
    page.fill("#passenger-phone", "+1-555-0144")

    # Submit booking
    page.click("#btn-confirm-booking")

    # 6. Assert confirmation view details
    expect(page.locator("#booking-confirmation-section")).to_be_visible()
    
    # Assert reference code starts with "TB-"
    booking_ref = page.locator("#booking-reference")
    expect(booking_ref).to_be_visible()
    expect(booking_ref).to_contain_text("TB-")

    # Assert total price calculation ($550 base + 10% tax = $605.00)
    total_price = page.locator("#total-price")
    expect(total_price).to_have_text("$605.00")
    expect(page.locator("#summary-passenger-name")).to_have_text("Alice Johnson")


def test_booking_validations(page: Page, server_url: str):
    """
    Task 12.2: Form Validation & Dynamic Price Change Test Scenario.
    Steps:
    1. Attempt search with invalid date ranges (return date prior to departure date) and verify warning alert banner.
    2. Reset valid dates, perform search, select flight option to open passenger form.
    3. Submit passenger form with missing required fields and assert inline validation error messages.
    """
    # 1. Navigate to booking portal
    page.goto(server_url)

    # Set invalid date range: return date earlier than departure date
    page.fill("#departure-date", "2026-10-15")
    page.fill("#return-date", "2026-10-05")

    # Click search and assert warning alert banner appears
    page.click("#btn-search")
    date_alert = page.locator("#date-error-alert")
    expect(date_alert).to_be_visible()
    expect(date_alert).to_contain_text("Return date cannot be earlier than departure date")
    expect(page.locator("#search-results-section")).to_be_hidden()

    # 2. Fix dates to valid range and proceed
    page.fill("#departure-date", "2026-10-05")
    page.fill("#return-date", "2026-10-15")
    page.click("#btn-search")
    expect(page.locator("#search-results-section")).to_be_visible()

    # Select flight package to display passenger form
    page.click("#btn-select-flight-1")
    expect(page.locator("#passenger-form-section")).to_be_visible()

    # 3. Submit passenger form with empty required fields
    page.fill("#passenger-name", "")
    page.fill("#passenger-email", "")
    page.fill("#passenger-phone", "")
    page.click("#btn-confirm-booking")

    # Assert inline validation messages
    name_err = page.locator("#passenger-name-error")
    email_err = page.locator("#passenger-email-error")
    phone_err = page.locator("#passenger-phone-error")

    expect(name_err).to_have_text("Full name is required.")
    expect(email_err).to_have_text("Email address is required.")
    expect(phone_err).to_have_text("Phone number is required.")
    expect(page.locator("#booking-confirmation-section")).to_be_hidden()
