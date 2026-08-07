"""
Test suite for Project 13: Order Management with API Setup.
Validates API test data seeding using Playwright APIRequestContext, UI search & status updates,
backend API cross-validation, and API test record cleanup (teardown).
"""

import socket
import time
import subprocess
import sys
from pathlib import Path
import urllib.request
import pytest
from playwright.sync_api import Page, Playwright, expect


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
    host = "127.0.0.1"
    base_url = f"http://{host}:{port}"
    subproject_dir = Path(__file__).parent.resolve()

    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "server:app",
            "--host", host,
            "--port", str(port),
            "--log-level", "error"
        ],
        cwd=str(subproject_dir)
    )

    start_time = time.time()
    server_ready = False
    while time.time() - start_time < 5.0:
        try:
            with urllib.request.urlopen(f"{base_url}/health") as resp:
                if resp.status == 200:
                    server_ready = True
                    break
        except Exception:
            time.sleep(0.1)

    if not server_ready:
        proc.kill()
        pytest.fail(f"FastAPI server failed to start at {base_url}")

    yield base_url

    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()


def test_api_order_seeding(playwright: Playwright, server_url: str):
    """
    Task 13.1: API Test Data Seeding Setup
    - Objective: Use Playwright APIRequestContext to create customer and order records.
    - Steps:
        1. Create an isolated APIRequestContext using playwright.request.new_context().
        2. Send HTTP POST request to /api/v1/orders with customer order payload.
        3. Assert HTTP status is 201 Created and JSON contains valid order_id.
    """
    # 1. Initialize APIRequestContext with base server URL
    api_request_context = playwright.request.new_context(base_url=server_url)

    # 2. Define customer order payload
    order_payload = {
        "customer_name": "Samantha Reed",
        "items": [
            {"name": "Wireless Ergonomic Mouse", "qty": 1, "price": 45.99},
            {"name": "Mechanical Keyboard", "qty": 1, "price": 120.00}
        ],
        "total_price": 165.99,
        "status": "Pending"
    }

    # 3. Send HTTP POST request to create order
    response = api_request_context.post("/api/v1/orders", data=order_payload)

    # 4. Assert response HTTP status code is 201 Created
    assert response.status == 201, f"Expected HTTP 201 Created, got {response.status}"

    # 5. Parse JSON response body and validate fields
    data = response.json()
    assert "order_id" in data, "Response JSON does not contain 'order_id' key"
    assert data["order_id"].startswith("ORD-"), f"Unexpected order_id format: {data['order_id']}"
    assert data["customer_name"] == "Samantha Reed", f"Customer name mismatch: {data['customer_name']}"
    assert data["status"] == "Pending", f"Expected initial status 'Pending', got '{data['status']}'"
    assert data["total_price"] == 165.99, f"Total price mismatch: {data['total_price']}"

    # Teardown API request context
    api_request_context.dispose()


def test_ui_search_status_update_and_api_validation(page: Page, playwright: Playwright, server_url: str):
    """
    Task 13.2: UI Search & Status Update with API Cross-Validation
    - Objective: Locate seeded order in UI, update status to Shipped, verify via GET API request,
                 and teardown via DELETE API request.
    - Steps:
        1. Seed order via API POST request. Save returned order_id.
        2. Navigate to UI dashboard in browser.
        3. Type order_id into search input box.
        4. Assert order row displays initial status 'Pending'.
        5. Change status dropdown to 'Shipped'.
        6. Verify UI status badge updates to 'Shipped'.
        7. Issue GET API request to verify backend status value is 'Shipped'.
        8. Issue DELETE API request to teardown seeded record, and verify 404 on subsequent GET.
    """
    # 1. Seed test data using Playwright APIRequestContext
    api_context = playwright.request.new_context(base_url=server_url)
    seed_payload = {
        "customer_name": "Marcus Vance",
        "items": [{"name": "4K Gaming Monitor", "qty": 1, "price": 349.99}],
        "total_price": 349.99,
        "status": "Pending"
    }

    create_resp = api_context.post("/api/v1/orders", data=seed_payload)
    assert create_resp.status == 201, f"Failed to seed order: HTTP {create_resp.status}"
    order_data = create_resp.json()
    seeded_order_id = order_data["order_id"]

    # 2. Open UI Dashboard in Playwright Page
    page.goto(server_url)
    page.wait_for_load_state("domcontentloaded")

    # 3. Locate search bar and filter for seeded order_id
    search_input = page.locator("#search-input")
    expect(search_input).to_be_visible()
    search_input.fill(seeded_order_id)

    # 4. Locate order table row corresponding to seeded order_id
    order_row = page.locator(f"tr[data-order-id='{seeded_order_id}']")
    expect(order_row).to_be_visible()

    # Assert customer name and initial status badge on UI
    customer_cell = order_row.locator(".customer-name")
    expect(customer_cell).to_have_text("Marcus Vance")

    status_badge = order_row.locator(f"#status-badge-{seeded_order_id}")
    expect(status_badge).to_have_text("Pending")

    # 5. Select 'Shipped' from status dropdown in UI
    status_select = order_row.locator(f"#status-select-{seeded_order_id}")
    status_select.select_option("Shipped")

    # 6. Verify UI status badge updates dynamically to 'Shipped'
    expect(status_badge).to_have_text("Shipped")

    # 7. Issue GET API request to cross-validate status in backend storage
    get_resp = api_context.get(f"/api/v1/orders/{seeded_order_id}")
    assert get_resp.status == 200, f"GET API failed for order {seeded_order_id}: HTTP {get_resp.status}"
    backend_order = get_resp.json()
    assert backend_order["status"] == "Shipped", (
        f"Backend API status mismatch: expected 'Shipped', got '{backend_order['status']}'"
    )

    # 8. Teardown: Issue DELETE API request to clean up seeded test record
    del_resp = api_context.delete(f"/api/v1/orders/{seeded_order_id}")
    assert del_resp.status == 200, f"DELETE API failed: HTTP {del_resp.status}"

    # Verify record no longer exists via GET request (returns 404)
    verify_del_resp = api_context.get(f"/api/v1/orders/{seeded_order_id}")
    assert verify_del_resp.status == 404, (
        f"Expected HTTP 404 after deletion, got HTTP {verify_del_resp.status}"
    )

    # Dispose API context
    api_context.dispose()
