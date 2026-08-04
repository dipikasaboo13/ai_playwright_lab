"""
FastAPI application for Project 14: Webhook and Notification Validation.
Provides a modern Webhook Hub UI for triggering events, receiving webhook dispatches,
logging payloads, and displaying real-time toast notifications.
"""

from datetime import datetime, timezone
import random
from typing import Dict, Any, List
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Webhook & Notification Dispatcher Hub")

# In-memory storage for received webhooks
webhooks_db: List[Dict[str, Any]] = []


class WebhookPayload(BaseModel):
    event_type: str
    timestamp: str
    data: Dict[str, Any]


class EventTriggerRequest(BaseModel):
    event_type: str
    recipient_email: str
    meta: Dict[str, Any] = {}


@app.get("/health")
def health_check():
    """Health check endpoint to verify server is active."""
    return {"status": "ok", "service": "webhook-notification-hub"}


@app.post("/api/v1/webhook")
def receive_webhook(payload: WebhookPayload):
    """
    Webhook receiver endpoint. Accepts JSON webhook payloads containing
    event_type, timestamp, and data dictionary.
    """
    event_entry = {
        "id": f"evt_{len(webhooks_db) + 1001}",
        "event_type": payload.event_type,
        "timestamp": payload.timestamp,
        "data": payload.data,
        "received_at": datetime.now(timezone.utc).isoformat()
    }
    webhooks_db.append(event_entry)
    return JSONResponse(status_code=200, content={"status": "success", "event_id": event_entry["id"]})


@app.get("/api/v1/webhooks")
def get_webhooks():
    """Returns all logged webhook events."""
    return {"count": len(webhooks_db), "webhooks": webhooks_db}


@app.post("/api/v1/trigger-event")
def trigger_event(req: EventTriggerRequest):
    """
    Processes event trigger request, constructs valid webhook payload,
    and returns it to UI for outbound dispatch or internal recording.
    """
    order_id = f"ORD-{random.randint(10000, 99999)}"
    now_iso = datetime.now(timezone.utc).isoformat()

    payload = {
        "event_type": req.event_type,
        "timestamp": now_iso,
        "data": {
            "order_id": order_id,
            "recipient_email": req.recipient_email,
            "status": "PROCESSED",
            "amount": round(random.uniform(25.0, 450.0), 2),
            **req.meta
        }
    }

    # Automatically log to internal webhooks database
    webhooks_db.append({
        "id": f"evt_{len(webhooks_db) + 1001}",
        "event_type": payload["event_type"],
        "timestamp": payload["timestamp"],
        "data": payload["data"],
        "received_at": now_iso
    })

    return {
        "status": "dispatched",
        "message": f"Webhook event '{req.event_type}' generated successfully",
        "payload": payload
    }


@app.delete("/api/v1/webhooks")
def clear_webhooks():
    """Clears internal webhook logs (used for test setup/teardown)."""
    webhooks_db.clear()
    return {"status": "cleared"}


@app.get("/", response_class=HTMLResponse)
def get_dashboard_ui():
    """Renders Webhook & Notification Dashboard web UI."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Webhook & Notification Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --accent-blue: #38bdf8;
            --accent-green: #22c55e;
            --accent-purple: #a855f7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-dark); color: var(--text-main); min-height: 100vh; padding: 2rem; }
        .container { max-width: 1100px; margin: 0 auto; }
        header { margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; }
        h1 { font-size: 1.875rem; font-weight: 700; background: linear-gradient(135deg, #38bdf8, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
        .card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); }
        .card h2 { font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; color: var(--accent-blue); }
        .form-group { margin-bottom: 1.25rem; }
        label { display: block; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; color: var(--text-muted); }
        input, select { width: 100%; padding: 0.75rem; background: #0f172a; border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-main); font-size: 0.95rem; }
        input:focus, select:focus { outline: none; border-color: var(--accent-blue); }
        button { width: 100%; padding: 0.85rem; background: linear-gradient(135deg, #0284c7, #2563eb); border: none; border-radius: 8px; color: #fff; font-weight: 600; cursor: pointer; transition: transform 0.1s ease, opacity 0.2s ease; }
        button:hover { opacity: 0.95; }
        button:active { transform: scale(0.98); }
        .events-list { max-height: 380px; overflow-y: auto; display: flex; flex-direction: column; gap: 0.75rem; }
        .event-item { background: #0f172a; border: 1px solid var(--border-color); padding: 1rem; border-radius: 8px; font-size: 0.875rem; }
        .event-item .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-weight: 600; font-size: 0.75rem; background: #1e3a8a; color: #60a5fa; margin-bottom: 0.5rem; }
        .event-item pre { font-family: monospace; color: #cbd5e1; white-space: pre-wrap; font-size: 0.8rem; }
        
        /* Toast Notification Styling */
        #toast-container { position: fixed; top: 1.5rem; right: 1.5rem; z-index: 9999; display: flex; flex-direction: column; gap: 0.75rem; }
        .toast { background: #1e293b; border-left: 4px solid var(--accent-green); padding: 1rem 1.25rem; border-radius: 8px; color: var(--text-main); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); display: flex; align-items: center; gap: 0.75rem; opacity: 0; transform: translateX(50px); transition: all 0.3s ease; }
        .toast.show { opacity: 1; transform: translateX(0); }
        .toast-icon { color: var(--accent-green); font-weight: 700; font-size: 1.2rem; }
        .toast-message { font-size: 0.9rem; font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Webhook & Notification Control Center</h1>
            <span style="font-size: 0.85rem; color: var(--text-muted);">Real-Time System Dispatcher</span>
        </header>

        <div class="grid">
            <!-- Event Trigger Card -->
            <div class="card">
                <h2>Trigger Webhook Event</h2>
                <form id="webhook-trigger-form">
                    <div class="form-group">
                        <label for="event-type-select">Select Event Type</label>
                        <select id="event-type-select" name="event_type" required>
                            <option value="order_created">order_created</option>
                            <option value="payment_completed">payment_completed</option>
                            <option value="user_registered">user_registered</option>
                            <option value="alert_triggered">alert_triggered</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="recipient-email">Recipient Email</label>
                        <input type="email" id="recipient-email" name="recipient_email" value="alex.dev@example.com" required>
                    </div>

                    <div class="form-group">
                        <label for="custom-note">Custom Note / Payload Metadata</label>
                        <input type="text" id="custom-note" name="custom_note" value="Standard checkout transaction">
                    </div>

                    <button type="submit" id="btn-trigger-webhook">Trigger & Dispatch Webhook</button>
                </form>
            </div>

            <!-- Live Webhook Log Card -->
            <div class="card">
                <h2>Interception & Received Log</h2>
                <div class="events-list" id="events-log">
                    <div class="event-item" id="empty-state">
                        <p style="color: var(--text-muted);">No webhooks dispatched yet. Trigger an event from the form.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Toast Notifications Container -->
    <div id="toast-container"></div>

    <script>
        function showToast(message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.id = 'toast-notification';
            toast.innerHTML = `
                <span class="toast-icon">✓</span>
                <span class="toast-message">${message}</span>
            `;
            container.appendChild(toast);
            
            setTimeout(() => toast.classList.add('show'), 10);
            
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 4000);
        }

        document.getElementById('webhook-trigger-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const eventType = document.getElementById('event-type-select').value;
            const email = document.getElementById('recipient-email').value;
            const note = document.getElementById('custom-note').value;

            const nowIso = new Date().toISOString();
            const payload = {
                event_type: eventType,
                timestamp: nowIso,
                data: {
                    order_id: 'ORD-' + Math.floor(10000 + Math.random() * 90000),
                    recipient_email: email,
                    status: 'PROCESSED',
                    note: note
                }
            };

            // Send outbound HTTP POST request to webhook receiver endpoint
            try {
                const response = await fetch('/api/v1/webhook', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const resData = await response.json();

                // Display Real-Time Toast Notification
                showToast(`Notification: Webhook event '${eventType}' delivered!`);

                // Append to Log UI
                const emptyState = document.getElementById('empty-state');
                if (emptyState) emptyState.remove();

                const logContainer = document.getElementById('events-log');
                const item = document.createElement('div');
                item.className = 'event-item';
                item.innerHTML = `
                    <span class="badge">${eventType}</span>
                    <pre>${JSON.stringify(payload, null, 2)}</pre>
                `;
                logContainer.prepend(item);

            } catch (err) {
                console.error('Webhook dispatch failed:', err);
                showToast('Error dispatching webhook event');
            }
        });
    </script>
</body>
</html>"""
