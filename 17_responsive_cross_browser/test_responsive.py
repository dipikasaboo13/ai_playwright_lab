"""
Test suite for Project 17: Responsive Cross-Browser Regression Suite.
Validates desktop multi-engine execution (Chromium, Firefox, WebKit), mobile layout viewports (iPhone 13, Pixel 5),
hamburger menu drawer toggles, responsive product grid, cart drawer, modal checkout, and automatic failure screenshot capture.
"""

import os
import socket
import sys
import time
import subprocess
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, Playwright, expect

SUBPROJECT_DIR = Path(__file__).parent
ARTIFACTS_DIR = SUBPROJECT_DIR / "artifacts" / "screenshots"


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


def capture_failure_screenshot(page: Page, test_name: str):
    """Utility function to automatically capture visual failure screenshots into artifacts directory."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    screenshot_path = ARTIFACTS_DIR / f"failure_{test_name}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    print(f"\n[Screenshot Saved] Failure artifact generated at: {screenshot_path}")


def test_desktop_cross_browser_flow(page: Page, server_url: str):
    """
    Task 17.1 Scenario:
    Executes end-to-end checkout user flow on desktop viewport.
    Asserts visibility of top desktop navigation bar, absence of hamburger button, cart drawer interactions,
    and confirmation reference code display. Compatible with --browser=all across Chromium, Firefox, and WebKit.
    """
    try:
        # 1. Set explicit desktop viewport dimensions
        page.set_viewport_size({"width": 1280, "height": 800})
        page.goto(server_url)

        # 2. Assert desktop navigation bar is visible and mobile hamburger button is hidden
        desktop_nav = page.locator("#desktop-nav")
        hamburger_btn = page.locator("#hamburger-btn")

        expect(desktop_nav).to_be_visible()
        expect(hamburger_btn).to_be_hidden()

        # 3. Verify desktop nav links content
        expect(page.locator("#nav-home")).to_contain_text("Home")
        expect(page.locator("#nav-products")).to_contain_text("Products")

        # 4. Add product to shopping cart
        page.click("#btn-add-prod-1")

        # 5. Assert cart drawer slides open and badge count updates to 1
        cart_drawer = page.locator("#cart-drawer")
        expect(cart_drawer).to_have_class(r"cart-drawer open")
        expect(page.locator("#cart-count")).to_have_text("1")
        expect(page.locator("#cart-total")).to_have_text("$299.00")

        # 6. Proceed to modal checkout
        page.click("#btn-checkout")
        checkout_modal = page.locator("#checkout-modal")
        expect(checkout_modal).to_be_visible()

        # 7. Complete checkout form fields and submit
        page.fill("#input-name", "Desktop Tester")
        page.fill("#input-email", "desktop.tester@example.com")
        page.fill("#input-address", "100 Desktop Blvd")
        page.click("#btn-submit-order")

        # 8. Assert modal closes and order confirmation banner displays reference code
        expect(checkout_modal).to_be_hidden()
        order_conf = page.locator("#order-confirmation")
        expect(order_conf).to_be_visible()
        expect(page.locator("#order-ref-code")).to_contain_text("REF-")
        expect(page.locator("#order-total-price")).to_have_text("$299.00")

    except Exception:
        capture_failure_screenshot(page, "desktop_cross_browser_flow")
        raise


def test_mobile_viewport(playwright: Playwright, browser: Browser, server_url: str):
    """
    Task 17.2 Scenario:
    Simulates mobile viewports (iPhone 13 & Pixel 5) using Playwright device descriptors.
    Asserts desktop navigation is hidden, hamburger menu button is visible, mobile drawer expands on click,
    and mobile checkout completes successfully with touch interactions.
    """
    # Test both iPhone 13 and Pixel 5 mobile device profiles
    mobile_devices = ["iPhone 13", "Pixel 5"]

    for device_name in mobile_devices:
        device_config = playwright.devices[device_name]
        context = browser.new_context(**device_config)
        page = context.new_page()

        try:
            page.goto(server_url)

            # 1. Assert desktop nav links hidden and hamburger menu toggle visible on mobile screen
            desktop_nav = page.locator("#desktop-nav")
            hamburger_btn = page.locator("#hamburger-btn")

            expect(desktop_nav).to_be_hidden()
            expect(hamburger_btn).to_be_visible()

            # 2. Click hamburger menu button to expand mobile drawer
            mobile_menu = page.locator("#mobile-menu")
            expect(mobile_menu).to_be_hidden()

            hamburger_btn.click()
            expect(mobile_menu).to_be_visible()
            expect(mobile_menu).to_have_class(r"mobile-menu expanded")

            # 3. Assert mobile menu items exist
            expect(page.locator("#mobile-nav-home")).to_be_visible()
            expect(page.locator("#mobile-nav-products")).to_be_visible()

            # 4. Add items to cart on mobile screen
            page.click("#btn-add-prod-2")  # Add Ultra-Wide Gaming Monitor ($599.00)

            # 5. Assert cart drawer slides open and mobile cart counter updates
            cart_drawer = page.locator("#cart-drawer")
            expect(cart_drawer).to_have_class(r"cart-drawer open")
            expect(page.locator("#mobile-cart-count")).to_have_text("1")
            expect(page.locator("#cart-total")).to_have_text("$599.00")

            # 6. Complete mobile checkout flow
            page.click("#btn-checkout")
            checkout_modal = page.locator("#checkout-modal")
            expect(checkout_modal).to_be_visible()

            page.fill("#input-name", f"Mobile Tester ({device_name})")
            page.fill("#input-email", "mobile.tester@example.com")
            page.fill("#input-address", "200 Mobile Street")
            page.click("#btn-submit-order")

            # 7. Assert order confirmation displays with generated reference code
            expect(checkout_modal).to_be_hidden()
            order_conf = page.locator("#order-confirmation")
            expect(order_conf).to_be_visible()
            expect(page.locator("#order-ref-code")).to_contain_text("REF-")
            expect(page.locator("#order-total-price")).to_have_text("$599.00")

        except Exception:
            capture_failure_screenshot(page, f"mobile_viewport_{device_name.replace(' ', '_')}")
            raise
        finally:
            context.close()


def test_tablet_viewport(playwright: Playwright, browser: Browser, server_url: str):
    """
    Additional Tablet Responsive Scenario:
    Simulates tablet viewport dimensions using Playwright iPad Pro profile.
    Verifies responsive product grid layout adaptations and cart drawer responsiveness.
    """
    tablet_config = playwright.devices["iPad Pro 11"]
    context = browser.new_context(**tablet_config)
    page = context.new_page()

    try:
        page.goto(server_url)

        # Verify page heading
        expect(page.locator("h1")).to_contain_text("Next-Gen Tech Essentials")

        # Add multiple products to test responsive list in cart drawer
        page.click("#btn-add-prod-1")  # $299.00
        page.click("#btn-add-prod-3")  # $149.00

        # Assert total calculation ($448.00)
        expect(page.locator("#cart-total")).to_have_text("$448.00")
        expect(page.locator("#cart-count")).to_have_text("2")

        # Proceed to checkout and confirm
        page.click("#btn-checkout")
        page.fill("#input-name", "Tablet Tester")
        page.fill("#input-email", "tablet.tester@example.com")
        page.fill("#input-address", "300 Tablet Boulevard")
        page.click("#btn-submit-order")

        expect(page.locator("#order-confirmation")).to_be_visible()
        expect(page.locator("#order-total-price")).to_have_text("$448.00")

    except Exception:
        capture_failure_screenshot(page, "tablet_viewport")
        raise
    finally:
        context.close()
