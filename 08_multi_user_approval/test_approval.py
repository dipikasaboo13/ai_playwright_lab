import socket
import time
import threading
import sys
from pathlib import Path
import urllib.request
import pytest
import uvicorn
from playwright.sync_api import Browser, expect

# Add current directory to sys.path to import server module
sys.path.insert(0, str(Path(__file__).parent))
import server


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def server_url():
    port = get_free_port()
    config = uvicorn.Config(server.app, host="127.0.0.1", port=port, log_level="error")
    uv_server = uvicorn.Server(config)

    thread = threading.Thread(target=uv_server.run, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"

    # Wait for server to start up
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


def test_multi_user_approval_workflow(browser: Browser, server_url: str):
    """
    Test multi-user approval workflow:
    1. User A (Requester) submits a request via context A.
    2. User A sees status 'Pending'.
    3. User B (Approver) accesses context B, sees the request, and approves it.
    4. User B sees status updated to 'Approved'.
    5. User A's view automatically updates to 'Approved'.
    """
    user_a_context = browser.new_context()
    user_b_context = browser.new_context()

    try:
        user_a_page = user_a_context.new_page()
        user_b_page = user_b_context.new_page()

        # Step 1: User A navigates to portal and submits a request
        user_a_page.goto(server_url)
        user_a_page.fill("#request-title", "MacBook Pro Purchase")
        user_a_page.fill("#request-amount", "2499.99")
        user_a_page.click("#submit-request-btn")

        # Step 2: Verify request appears on User A's screen as Pending
        expect(user_a_page.locator("text=MacBook Pro Purchase")).to_be_visible()
        pending_badge_a = user_a_page.locator(".badge-pending")
        expect(pending_badge_a).to_be_visible()
        expect(pending_badge_a).to_have_text("Pending")

        # Step 3: User B navigates to portal and sees pending request
        user_b_page.goto(server_url)
        expect(user_b_page.locator("text=MacBook Pro Purchase")).to_be_visible()
        expect(user_b_page.locator(".badge-pending")).to_have_text("Pending")

        # Step 4: User B approves the request
        user_b_page.click(".btn-approve")

        # Step 5: Verify User B sees status updated to 'Approved'
        approved_badge_b = user_b_page.locator(".badge-approved")
        expect(approved_badge_b).to_be_visible()
        expect(approved_badge_b).to_have_text("Approved")

        # Step 6: Verify User A's screen updates to 'Approved' via dynamic status sync
        approved_badge_a = user_a_page.locator(".badge-approved")
        expect(approved_badge_a).to_be_visible(timeout=5000)
        expect(approved_badge_a).to_have_text("Approved")

    finally:
        user_a_context.close()
        user_b_context.close()
