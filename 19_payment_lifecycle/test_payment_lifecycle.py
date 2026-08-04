"""
Test suite for Project 19: Payment Transaction Lifecycle Simulation.
Validates end-to-end payment authorization, pending settlement, completion state machine,
and transaction reversal / refund ledger math calculation using Playwright.
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


@pytest.fixture(autouse=True)
def reset_server_state(server_url: str):
    """Fixture to reset in-memory ledger and transactions before each test function."""
    req = urllib.request.Request(f"{server_url}/api/reset", data=b"", method="POST")
    try:
        with urllib.request.urlopen(req):
            pass
    except Exception as e:
        print(f"Error resetting ledger: {e}")


def test_payment_completion(page: Page, server_url: str):
    """
    Task 19.1 Scenario:
    Initiates payment charge via UI form and transitions payment status through state machine:
    Initiated -> Authorized -> Pending -> Completed.
    Asserts account ledger balance math updates and transaction table status shows Completed.
    """
    # 1. Navigate to payment lifecycle portal
    page.goto(server_url)
    expect(page.locator("h1")).to_contain_text("Payment Lifecycle & Ledger Simulation Portal")

    # 2. Verify initial ledger starting balance
    ledger_balance = page.locator("#ledger-balance")
    expect(ledger_balance).to_have_text("$1,000.00")

    # 3. Fill and submit payment charge form ($150.00)
    page.fill("#card-number", "4532 9812 3456 7890")
    page.fill("#card-expiry", "12/28")
    page.fill("#charge-amount", "150.00")
    page.fill("#charge-desc", "Cloud Software Subscription")
    page.click("#btn-initiate-payment")

    # 4. Verify transaction status transitions to Initiated
    active_tx = page.locator("#active-tx-id")
    expect(active_tx).to_be_visible()
    
    # 5. Transition state: Initiated -> Authorized
    page.click("#btn-authorize")
    expect(page.locator("#btn-pending")).to_be_visible()

    # 6. Transition state: Authorized -> Pending
    page.click("#btn-pending")
    expect(page.locator("#btn-complete")).to_be_visible()

    # 7. Transition state: Pending -> Completed
    page.click("#btn-complete")

    # 8. Assert ledger balance math: $1000.00 - $150.00 = $850.00
    expect(ledger_balance).to_have_text("$850.00")

    # 9. Verify transaction table reflects Completed status
    table_body = page.locator("#transaction-table-body")
    expect(table_body).to_contain_text("Completed")
    expect(table_body).to_contain_text("Cloud Software Subscription")
    expect(table_body).to_contain_text("$150.00")


def test_payment_refund(page: Page, server_url: str):
    """
    Task 19.2 Scenario:
    Initiates payment completion and subsequently executes transaction reversal / refund.
    Verifies status updates to Refunded and ledger deduction / credit math restoration.
    """
    page.goto(server_url)
    ledger_balance = page.locator("#ledger-balance")
    expect(ledger_balance).to_have_text("$1,000.00")

    # 1. Fill out form for a $200.00 payment charge
    page.fill("#card-number", "4000 1234 5678 9010")
    page.fill("#card-expiry", "08/29")
    page.fill("#charge-amount", "200.00")
    page.fill("#charge-desc", "Annual Hosting Fee")
    page.click("#btn-initiate-payment")

    # 2. Run auto-lifecycle to advance directly to Completed status
    expect(page.locator("#btn-auto-lifecycle")).to_be_visible()
    page.click("#btn-auto-lifecycle")

    # 3. Assert balance after completion: $1000.00 - $200.00 = $800.00
    expect(ledger_balance).to_have_text("$800.00")
    expect(page.locator("#transaction-table-body")).to_contain_text("Completed")

    # 4. Initiate transaction reversal / refund
    page.click("#btn-refund")
    
    # Assert refund modal is displayed
    refund_modal = page.locator("#refund-modal")
    expect(refund_modal).to_be_visible()

    # 5. Confirm full refund of $200.00
    page.fill("#refund-amount-input", "200.00")
    page.click("#btn-confirm-refund")

    # 6. Assert modal closes and transaction status updates to Refunded
    expect(refund_modal).to_be_hidden()
    expect(page.locator("#transaction-table-body")).to_contain_text("Refunded")

    # 7. Assert ledger balance restored back to $1,000.00 ($800.00 + $200.00)
    expect(ledger_balance).to_have_text("$1,000.00")
