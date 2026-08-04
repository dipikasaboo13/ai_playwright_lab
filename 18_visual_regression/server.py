"""
FastAPI Server for Project 18: Visual Regression Testing Portal.

Serves key screens (Executive Dashboard & Payment Checkout) containing dynamic UI components
(live clocks, generated timestamps, session tokens, dynamic transaction IDs) specifically
designed to test Playwright visual comparison masking capabilities.
"""

import random
import time
import uuid
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Project 18 Visual Regression Portal")

COMMON_STYLE = """
<style>
    :root {
        --bg-color: #0f172a;
        --card-bg: #1e293b;
        --accent-color: #38bdf8;
        --accent-green: #34d399;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border-color: #334155;
    }
    body {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        background-color: var(--bg-color);
        color: var(--text-primary);
        margin: 0;
        padding: 24px;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 16px;
        margin-bottom: 24px;
    }
    .nav-links a {
        color: var(--accent-color);
        margin-left: 16px;
        text-decoration: none;
        font-weight: 600;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 24px;
    }
    .card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .card h3 {
        margin-top: 0;
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent-color);
    }
    .dynamic-badge {
        background-color: #475569;
        color: #f1f5f9;
        padding: 4px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 0.85rem;
    }
    .form-group {
        margin-bottom: 16px;
    }
    label {
        display: block;
        margin-bottom: 6px;
        color: var(--text-secondary);
        font-size: 0.9rem;
    }
    input {
        width: 100%;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid var(--border-color);
        background-color: #0f172a;
        color: var(--text-primary);
        box-sizing: border-box;
    }
    button {
        background-color: var(--accent-color);
        color: #0f172a;
        border: none;
        padding: 12px 20px;
        border-radius: 6px;
        font-weight: 700;
        cursor: pointer;
        width: 100%;
    }
</style>
"""

@app.get("/health")
def health_check():
    """Health check endpoint for server initialization verification."""
    return {"status": "ok", "timestamp": time.time()}

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Renders the Executive Analytics Dashboard screen with dynamic elements."""
    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    session_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"
    live_clock = time.strftime("%H:%M:%S")
    active_users = random.randint(1400, 1600)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Executive Dashboard - Visual Regression Lab</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="header">
            <h1>Analytics & Operational Dashboard</h1>
            <div class="nav-links">
                <a href="/dashboard" id="nav-dashboard">Dashboard</a>
                <a href="/checkout" id="nav-checkout">Checkout</a>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>System Status</h3>
                <div class="stat-value" style="color: var(--accent-green);">HEALTHY</div>
                <p style="margin-top: 10px; font-size: 0.85rem; color: var(--text-secondary);">
                    Server Uptime: 99.98%
                </p>
            </div>

            <div class="card">
                <h3>Live Active Users</h3>
                <div class="stat-value" id="active-users-count">{active_users}</div>
                <p style="margin-top: 10px; font-size: 0.85rem; color: var(--text-secondary);">
                    Updated real-time
                </p>
            </div>

            <div class="card">
                <h3>Session Context</h3>
                <p>Session ID: <span id="session-id" class="dynamic-badge">{session_id}</span></p>
                <p>Live Clock: <span id="live-clock" class="dynamic-badge">{live_clock}</span></p>
            </div>

            <div class="card">
                <h3>Timestamp Header</h3>
                <p>Generated At:</p>
                <div id="dynamic-timestamp" class="dynamic-badge" style="display: inline-block; margin-top: 4px;">
                    {current_time_str}
                </div>
            </div>
        </div>

        <div class="card" style="margin-top: 24px;">
            <h2 style="margin-top: 0; font-size: 1.2rem;">Monthly Revenue Trend</h2>
            <div style="background-color: #0f172a; height: 120px; border-radius: 8px; border: 1px dashed var(--border-color); display: flex; align-items: center; justify-content: center; color: var(--text-secondary);">
                [Static Chart Rendering Component Placeholder]
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/checkout", response_class=HTMLResponse)
def get_checkout():
    """Renders Payment Checkout screen with dynamic transaction tokens."""
    tx_id = f"TXN-{random.randint(100000, 999999)}"
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Payment Checkout - Visual Regression Lab</title>
        {COMMON_STYLE}
    </head>
    <body>
        <div class="header">
            <h1>Enterprise Payment Portal</h1>
            <div class="nav-links">
                <a href="/dashboard" id="nav-dashboard">Dashboard</a>
                <a href="/checkout" id="nav-checkout">Checkout</a>
            </div>
        </div>

        <div style="max-width: 600px; margin: 0 auto;">
            <div class="card">
                <h2>Complete Your Order</h2>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">
                    Review transaction breakdown and submit payment details.
                </p>

                <div style="background-color: #0f172a; padding: 12px; border-radius: 6px; margin-bottom: 20px;">
                    <p style="margin: 4px 0;">Transaction Ref: <span id="checkout-tx-id" class="dynamic-badge">{tx_id}</span></p>
                    <p style="margin: 4px 0;">Generated At: <span id="checkout-timestamp" class="dynamic-badge">{timestamp_str}</span></p>
                </div>

                <form onsubmit="event.preventDefault(); alert('Payment Processed!');">
                    <div class="form-group">
                        <label for="card-name">Cardholder Name</label>
                        <input type="text" id="card-name" value="Jane Doe" readonly />
                    </div>

                    <div class="form-group">
                        <label for="card-number">Card Number</label>
                        <input type="text" id="card-number" value="**** **** **** 4242" readonly />
                    </div>

                    <div style="display: flex; gap: 12px;">
                        <div class="form-group" style="flex: 1;">
                            <label for="expiry">Expiry</label>
                            <input type="text" id="expiry" value="12/28" readonly />
                        </div>
                        <div class="form-group" style="flex: 1;">
                            <label for="cvv">CVV</label>
                            <input type="text" id="cvv" value="***" readonly />
                        </div>
                    </div>

                    <div style="margin-top: 10px; margin-bottom: 20px; font-size: 1.2rem; font-weight: 700; color: var(--accent-green);">
                        Total: $499.00 USD
                    </div>

                    <button type="submit" id="btn-submit-payment">Pay Now ($499.00)</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
