"""
FastAPI web server for Project 16: Mock External Dependency Failures.
Serves an interactive web application with payment checkout and dynamic data dashboard flows,
designed for testing route interception, server error handling, loading spinners, network timeouts,
and partial data fallback views.
"""

import time
from fastapi import FastAPI, Response, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mock Dependency Failures Lab")


class PaymentRequest(BaseModel):
    card_number: str
    amount: float


@app.get("/health")
def health_check():
    """Healthcheck endpoint for pytest fixture readiness verification."""
    return {"status": "ok"}


@app.post("/api/payment")
def process_payment(req: PaymentRequest):
    """
    Standard payment processing endpoint.
    Returns HTTP 200 with transaction payload when called normally.
    In tests, Playwright page.route() will intercept requests to this endpoint.
    """
    return {
        "status": "success",
        "transaction_id": "TX10098234",
        "amount": req.amount,
        "message": "Payment processed successfully."
    }


@app.get("/api/user-data")
def get_user_data(delay: float = 0, partial: bool = False):
    """
    Standard user profile data endpoint.
    Supports delay (seconds) and partial data flags for testing network latency and fallback UI.
    """
    if delay > 0:
        time.sleep(delay)
    if partial:
        return {
            "status": "partial",
            "is_partial": True,
            "user_id": "USR-9999",
            "name": "Alex Mercer (Degraded)"
        }
    return {
        "status": "complete",
        "is_partial": False,
        "user_id": "USR-8821",
        "name": "Alex Mercer",
        "email": "alex.mercer@example.com",
        "account_balance": "$1,450.00",
        "role": "Premium Subscriber"
    }


@app.get("/", response_class=HTMLResponse)
def index():
    """Renders the main web interface for payment processing and dashboard data visualization."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project 16 - Dependency Resilience Lab</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-color: #3b82f6;
            --accent-hover: #2563eb;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --error-bg: #451a03;
            --error-border: #dc2626;
            --error-text: #fca5a5;
            --warning-bg: #422006;
            --warning-border: #d97706;
            --warning-text: #fcd34d;
            --success-bg: #064e3b;
            --success-border: #10b981;
            --success-text: #6ee7b7;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }

        .container {
            width: 100%;
            max-width: 720px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .header {
            text-align: center;
            margin-bottom: 1rem;
        }

        .header h1 {
            margin: 0;
            font-size: 1.8rem;
            color: var(--text-primary);
        }

        .header p {
            margin-top: 0.5rem;
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            border: 1px solid #334155;
        }

        .card h2 {
            margin-top: 0;
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: #60a5fa;
            border-bottom: 1px solid #334155;
            padding-bottom: 0.5rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        input {
            background-color: #0f172a;
            border: 1px solid #475569;
            border-radius: 6px;
            padding: 0.75rem;
            color: var(--text-primary);
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus {
            border-color: var(--accent-color);
        }

        button {
            background-color: var(--accent-color);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.75rem 1.25rem;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }

        button:hover {
            background-color: var(--accent-hover);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        /* Banner alerts */
        .alert {
            padding: 1rem;
            border-radius: 8px;
            font-size: 0.9rem;
            display: none;
            margin-top: 1rem;
        }

        .alert-error {
            background-color: var(--error-bg);
            border: 1px solid var(--error-border);
            color: var(--error-text);
        }

        .alert-warning {
            background-color: var(--warning-bg);
            border: 1px solid var(--warning-border);
            color: var(--warning-text);
        }

        .alert-success {
            background-color: var(--success-bg);
            border: 1px solid var(--success-border);
            color: var(--success-text);
        }

        /* Loading spinner */
        .spinner-container {
            display: none;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            margin-top: 1rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid #334155;
            border-top: 3px solid var(--accent-color);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .data-display {
            background-color: #0f172a;
            border-radius: 6px;
            padding: 1rem;
            margin-top: 1rem;
            font-family: monospace;
            font-size: 0.85rem;
            color: #a7f3d0;
            min-height: 50px;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Payment & Resilience Testing Portal</h1>
        <p>Project 16 - Mock External Dependency Failures Lab</p>
    </div>

    <!-- Payment Checkout Card -->
    <div class="card" id="checkout-section">
        <h2>Payment Checkout Service</h2>
        <form id="checkout-form" onsubmit="handlePaymentSubmit(event)">
            <div class="form-group">
                <label for="card-number-input">Card Number</label>
                <input type="text" id="card-number-input" value="4532 8812 9901 3342" required>
            </div>
            <div class="form-group">
                <label for="amount-input">Amount ($)</label>
                <input type="number" id="amount-input" value="99.99" step="0.01" required>
            </div>
            <button type="submit" id="btn-pay-now">Process Payment</button>
        </form>

        <div class="spinner-container" id="payment-spinner">
            <div class="spinner"></div>
            <span>Connecting to Payment Gateway...</span>
        </div>

        <div class="alert alert-error" id="error-alert">
            <strong>Error:</strong> <span id="error-message"></span>
        </div>

        <div class="alert alert-success" id="success-alert">
            <strong>Success:</strong> <span id="success-message"></span>
        </div>
    </div>

    <!-- Data Dashboard Card -->
    <div class="card" id="dashboard-card">
        <h2>User Account Dashboard</h2>
        <p style="color: var(--text-secondary); font-size: 0.9rem;">
            Fetches profile and account details from external microservice.
        </p>
        <button type="button" id="btn-load-data" onclick="handleLoadUserData()">Fetch User Details</button>

        <div class="spinner-container" id="dashboard-spinner">
            <div class="spinner"></div>
            <span>Loading user account records...</span>
        </div>

        <div class="alert alert-warning" id="fallback-view">
            <strong>Fallback View Active:</strong> <span id="fallback-message"></span>
        </div>

        <div class="data-display" id="user-profile-data" style="display: none;">
            <!-- Output JSON rendered here -->
        </div>
    </div>
</div>

<script>
    async function handlePaymentSubmit(event) {
        event.preventDefault();
        
        const btn = document.getElementById("btn-pay-now");
        const spinner = document.getElementById("payment-spinner");
        const errorAlert = document.getElementById("error-alert");
        const errorMsg = document.getElementById("error-message");
        const successAlert = document.getElementById("success-alert");
        const successMsg = document.getElementById("success-message");

        // Reset UI state
        btn.disabled = true;
        spinner.style.display = "flex";
        errorAlert.style.display = "none";
        successAlert.style.display = "none";

        const cardNumber = document.getElementById("card-number-input").value;
        const amount = parseFloat(document.getElementById("amount-input").value);

        try {
            const response = await fetch("/api/payment", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ card_number: cardNumber, amount: amount })
            });

            if (!response.ok) {
                let errText = "Payment Gateway HTTP " + response.status;
                try {
                    const errData = await response.json();
                    if (errData && errData.error) {
                        errText = errData.error;
                    }
                } catch (e) {
                    const rawText = await response.text();
                    if (rawText) errText = rawText;
                }
                throw new Error(errText);
            }

            const data = await response.json();
            successMsg.textContent = `${data.message} (Transaction ID: ${data.transaction_id})`;
            successAlert.style.display = "block";
        } catch (err) {
            errorMsg.textContent = err.message || "Payment Gateway failed to process request.";
            errorAlert.style.display = "block";
        } finally {
            spinner.style.display = "none";
            btn.disabled = false;
        }
    }

    async function handleLoadUserData() {
        const btn = document.getElementById("btn-load-data");
        const spinner = document.getElementById("dashboard-spinner");
        const fallbackView = document.getElementById("fallback-view");
        const fallbackMsg = document.getElementById("fallback-message");
        const profileData = document.getElementById("user-profile-data");

        btn.disabled = true;
        spinner.style.display = "flex";
        fallbackView.style.display = "none";
        profileData.style.display = "none";

        try {
            const response = await fetch("/api/user-data");
            
            if (!response.ok) {
                throw new Error("Service connection failed with HTTP " + response.status);
            }

            const data = await response.json();

            // Check if backend returned partial data
            if (data.is_partial || data.status === "partial" || !data.email) {
                fallbackMsg.textContent = "Partial account data received. Secondary profile services are currently offline.";
                fallbackView.style.display = "block";
                profileData.textContent = JSON.stringify(data, null, 2);
                profileData.style.display = "block";
            } else {
                profileData.textContent = JSON.stringify(data, null, 2);
                profileData.style.display = "block";
            }
        } catch (err) {
            fallbackMsg.textContent = "Unable to fetch complete profile. Fallback mode engaged: " + err.message;
            fallbackView.style.display = "block";
        } finally {
            spinner.style.display = "none";
            btn.disabled = false;
        }
    }
</script>

</body>
</html>
"""
