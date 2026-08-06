"""
Test suite for Project 14: Webhook and Notification Validation.
Validates outbound HTTP POST webhook network interception, JSON payload validation
(event_type, timestamp, data keys), and DOM real-time toast notification assertion.
"""

import socket
import time
import threading
import sys
from pathlib import Path
import urllib.request
import pytest
import uvicorn
from playwright.sync_api import Page, Playwright, expect

# Ensure subproject directory is in sys.path to import local server module
sys.path.insert(0, str(Path(__file__).parent))
import server


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


def test_webhook_payload(page: Page, server_url: str):
    """
    Task 14.1: UI Trigger & Webhook Event Interception
    - Objective: Trigger UI action and intercept outbound HTTP POST webhook event.
    - Steps:
        1. Open Webhook Notification Dashboard in Playwright Page.
        2. Select event type ('order_created') from dropdown selector.
        3. Fill form parameters (recipient email, custom note).
        4. Set up Playwright request listener (page.expect_request) matching POST to /api/v1/webhook.
        5. Click trigger button to submit form.
        6. Intercept outbound HTTP POST request payload.
        7. Assert event payload contains required keys: 'event_type', 'timestamp', 'data'.
        8. Assert payload data structure values match submitted form input.
    """
    # 1. Navigate to Webhook Control Center UI
    page.goto(server_url)
    page.wait_for_load_state("domcontentloaded")

    # 2. Select event type 'order_created'
    event_select = page.locator("#event-type-select")
    expect(event_select).to_be_visible()
    event_select.select_option("order_created")

    # 3. Fill recipient email and custom note
    email_input = page.locator("#recipient-email")
    email_input.fill("test.developer@example.com")

    note_input = page.locator("#custom-note")
    note_input.fill("Automated Playwright Webhook Payload Verification")

    trigger_btn = page.locator("#btn-trigger-webhook")
    expect(trigger_btn).to_be_enabled()

    # 4 & 5. Expect outbound HTTP POST request to webhook endpoint upon button click
    with page.expect_request(
        lambda req: "/api/v1/webhook" in req.url and req.method == "POST"
    ) as request_info:
        trigger_btn.click()

    # 6. Retrieve intercepted request object
    intercepted_request = request_info.value
    assert intercepted_request is not None, "Failed to intercept outbound POST request to webhook endpoint"

    # 7. Extract JSON payload from intercepted request
    payload = intercepted_request.post_data_json
    assert payload is not None, "Intercepted webhook request post_data_json is empty or invalid"

    # 8. Assert presence of required top-level payload keys: 'event_type', 'timestamp', 'data'
    assert "event_type" in payload, "Webhook payload missing required 'event_type' key"
    assert "timestamp" in payload, "Webhook payload missing required 'timestamp' key"
    assert "data" in payload, "Webhook payload missing required 'data' key"

    # Validate specific payload contents
    assert payload["event_type"] == "order_created", f"Expected event_type 'order_created', got '{payload['event_type']}'"
    assert isinstance(payload["timestamp"], str) and len(payload["timestamp"]) > 0, "Invalid timestamp string format"
    
    data_dict = payload["data"]
    assert isinstance(data_dict, dict), "'data' field in webhook payload must be a JSON object/dict"
    assert "order_id" in data_dict, "Webhook data payload missing 'order_id'"
    assert data_dict["order_id"].startswith("ORD-"), f"Unexpected order_id format: {data_dict['order_id']}"
    assert data_dict["recipient_email"] == "test.developer@example.com", f"Recipient email mismatch: {data_dict['recipient_email']}"
    assert data_dict["note"] == "Automated Playwright Webhook Payload Verification", f"Note mismatch: {data_dict['note']}"


def test_ui_notification(page: Page, server_url: str):
    """
    Task 14.2: Real-Time In-App Toast Notification Assertion
    - Objective: Verify UI toast notification message.
    - Steps:
        1. Navigate to Webhook Notification Dashboard in Playwright Page.
        2. Select event type ('payment_completed') from dropdown selector.
        3. Click 'Trigger & Dispatch Webhook' button.
        4. Locate real-time toast notification element (#toast-notification).
        5. Assert toast notification element becomes visible on DOM.
        6. Assert toast notification message contains expected notification text.
    """
    # 1. Open Web UI
    page.goto(server_url)
    page.wait_for_load_state("domcontentloaded")

    # 2. Select event type 'payment_completed'
    event_select = page.locator("#event-type-select")
    expect(event_select).to_be_visible()
    event_select.select_option("payment_completed")

    # 3. Trigger webhook dispatch
    trigger_btn = page.locator("#btn-trigger-webhook")
    trigger_btn.click()

    # 4 & 5. Locate toast notification and assert visibility on DOM
    toast_element = page.locator("#toast-notification")
    expect(toast_element).to_be_visible(timeout=5000)

    # 6. Assert exact/expected notification text content
    toast_message = page.locator("#toast-notification .toast-message")
    expect(toast_message).to_be_visible()
    expect(toast_message).to_have_text("Notification: Webhook event 'payment_completed' delivered!")
