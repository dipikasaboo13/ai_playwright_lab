"""
FastAPI Server for Project 20: AI-Assisted Test Automation Framework.
Provides interactive UI routes for Login, Dashboard, and Checkout workflows,
along with API endpoints for testing framework interactions.
"""

from typing import Dict, Optional
from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="AI-Assisted Framework Target App")

# Mock User Database
USERS = {
    "admin": "admin123",
    "john_doe": "password123",
    "qa_tester": "playwright2026",
    "test_user": "secret_pass"
}

# Discount Codes
PROMO_CODES = {
    "AI20": 0.20,      # 20% discount
    "HALFPRICE": 0.50, # 50% discount
    "SUPER100": 1.00   # 100% discount
}


@app.get("/health")
def health_check():
    """Health check endpoint for test setup synchronization."""
    return {"status": "ok"}


@app.get("/login", response_class=HTMLResponse)
def login_page(error: Optional[str] = None):
    """Render HTML Login Page with error state handling."""
    error_html = f'<div id="error-message" class="error-banner">{error}</div>' if error else ""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login - AI Framework Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; padding: 40px; }}
            .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h2 {{ color: #333; margin-bottom: 20px; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ display: block; margin-bottom: 5px; color: #666; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }}
            button {{ width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
            button:hover {{ background: #218838; }}
            .error-banner {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; padding: 10px; border-radius: 4px; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Portal Sign In</h2>
            {error_html}
            <form action="/login" method="post" id="login-form">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" placeholder="Enter username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter password" required>
                </div>
                <button type="submit" id="btn-login">Sign In</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/login")
def process_login(username: str = Form(...), password: str = Form(...)):
    """Authenticate login form post and return dashboard or error page."""
    # Check credentials
    if username in USERS and USERS[username] == password:
        html_redirect = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0;url=/dashboard?user={username}">
        </head>
        <body>Redirecting...</body>
        </html>
        """
        return HTMLResponse(content=html_redirect)
    else:
        # Invalid credentials or unknown user
        return login_page(error="Invalid username or password.")


from html import escape

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(user: str = Query("Guest"), query: Optional[str] = None):
    """Render Dashboard Page displaying key metrics and search features."""
    search_result_html = ""
    if query:
        escaped_query = escape(query)
        search_result_html = f'<div id="search-results" class="search-box">Search query results for: <strong>{escaped_query}</strong></div>'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard - AI Framework Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eef2f5; margin: 0; padding: 20px; }}
            .navbar {{ background: #343a40; color: white; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 6px; }}
            .navbar a {{ color: #007bff; text-decoration: none; font-weight: bold; background: white; padding: 6px 12px; border-radius: 4px; }}
            .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center; }}
            .card-val {{ font-size: 28px; font-weight: bold; color: #007bff; }}
            .search-box {{ margin-top: 20px; background: white; padding: 15px; border-radius: 8px; }}
            input[type="text"] {{ padding: 8px; width: 60%; border: 1px solid #ccc; border-radius: 4px; }}
            button {{ padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <span id="welcome-message">Welcome, <strong id="current-user">{user}</strong>!</span>
            <div>
                <a href="/checkout" id="nav-checkout">Go to Checkout</a>
                <a href="/login" id="nav-logout" style="background: #dc3545; color: white; margin-left: 10px;">Logout</a>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="card">
                <h3>Total Sales</h3>
                <div class="card-val" id="metric-sales">$12,450.00</div>
            </div>
            <div class="card">
                <h3>Active Users</h3>
                <div class="card-val" id="metric-users">1,280</div>
            </div>
            <div class="card">
                <h3>Pending Orders</h3>
                <div class="card-val" id="metric-orders">42</div>
            </div>
        </div>

        <div class="search-box">
            <h3>Search Products / Records</h3>
            <form action="/dashboard" method="get" id="search-form">
                <input type="hidden" name="user" value="{user}">
                <input type="text" id="search-input" name="query" placeholder="Type product name..." value="{query or ''}">
                <button type="submit" id="btn-search">Search</button>
            </form>
            {search_result_html}
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/checkout", response_class=HTMLResponse)
def checkout_page(promo: Optional[str] = None, promo_applied: Optional[bool] = False, error: Optional[str] = None):
    """Render Checkout Page with cart items, promo code calculator, and confirmation."""
    item_price = 150.00
    quantity = 2
    subtotal = item_price * quantity
    discount_pct = PROMO_CODES.get(promo.upper(), 0.0) if promo and promo.upper() in PROMO_CODES else 0.0
    
    if promo and promo.upper() not in PROMO_CODES:
        error = f"Invalid promo code: {promo}"

    discount_amount = subtotal * discount_pct
    total = subtotal - discount_amount

    error_html = f'<div id="checkout-error" class="error-banner">{error}</div>' if error else ""
    success_promo_html = f'<div id="promo-success" class="success-banner">Promo code "{promo}" applied! ({int(discount_pct*100)}% Off)</div>' if (promo and discount_pct > 0) else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Checkout - AI Framework Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8f9fa; padding: 30px; }}
            .checkout-container {{ max-width: 600px; margin: 0 auto; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }}
            h2 {{ color: #222; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border-bottom: 1px solid #ddd; padding: 10px; text-align: left; }}
            .total-row {{ font-weight: bold; font-size: 18px; }}
            .promo-section {{ background: #f1f3f5; padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
            input[type="text"] {{ padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 60%; }}
            .btn {{ padding: 10px 18px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
            .btn-success {{ background: #28a745; width: 100%; font-size: 18px; padding: 12px; margin-top: 15px; }}
            .error-banner {{ background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin-bottom: 15px; }}
            .success-banner {{ background: #d4edda; color: #155724; padding: 10px; border-radius: 4px; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="checkout-container">
            <h2>Order Summary & Checkout</h2>
            {error_html}
            {success_promo_html}

            <table id="cart-table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Qty</th>
                        <th>Price</th>
                        <th>Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Enterprise License</td>
                        <td id="cart-qty">{quantity}</td>
                        <td>${item_price:.2f}</td>
                        <td id="cart-subtotal">${subtotal:.2f}</td>
                    </tr>
                </tbody>
            </table>

            <div class="promo-section">
                <form action="/checkout" method="get" id="promo-form">
                    <label for="promo-input">Promo Code:</label>
                    <input type="text" id="promo-input" name="promo" value="{promo or ''}" placeholder="e.g. AI20">
                    <button type="submit" id="btn-apply-promo" class="btn">Apply</button>
                </form>
            </div>

            <div style="text-align: right; font-size: 16px; margin-bottom: 10px;">
                <span>Discount: </span><strong id="discount-val">-${discount_amount:.2f}</strong>
            </div>
            <div style="text-align: right;" class="total-row">
                <span>Total Amount: </span><strong id="total-val">${total:.2f}</strong>
            </div>

            <form action="/confirm-checkout" method="post" id="checkout-form">
                <input type="hidden" name="total_amount" value="{total}">
                <button type="submit" id="btn-submit-order" class="btn btn-success">Complete Purchase</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/confirm-checkout", response_class=HTMLResponse)
def confirm_checkout(total_amount: float = Form(...)):
    """Process checkout order and display order confirmation page."""
    import uuid
    conf_code = f"CONF-{uuid.uuid4().hex[:8].upper()}"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Order Confirmation - AI Framework Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eef2f5; padding: 40px; text-align: center; }}
            .card {{ max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            .icon {{ font-size: 50px; color: #28a745; }}
            h2 {{ color: #333; margin-top: 10px; }}
            .code {{ background: #f8f9fa; border: 1px dashed #007bff; padding: 10px; border-radius: 4px; font-size: 20px; font-weight: bold; color: #007bff; display: inline-block; margin: 15px 0; }}
            a {{ display: inline-block; margin-top: 20px; text-decoration: none; background: #007bff; color: white; padding: 10px 20px; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon">✓</div>
            <h2>Order Confirmed!</h2>
            <p>Thank you for your purchase. Your transaction was processed successfully.</p>
            <p>Confirmation Reference:</p>
            <div class="code" id="confirmation-code">{conf_code}</div>
            <p>Total Charged: <strong id="confirmed-total">${total_amount:.2f}</strong></p>
            <a href="/dashboard" id="link-back-dashboard">Return to Dashboard</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
