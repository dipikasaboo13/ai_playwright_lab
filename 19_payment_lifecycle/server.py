import uuid
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Payment Transaction Lifecycle Portal")

# In-memory data store for ledger state and transactions
INITIAL_BALANCE = 1000.00

ledger_store: Dict[str, Any] = {
    "balance": INITIAL_BALANCE,
    "transactions": {}
}


class PaymentInitiateRequest(BaseModel):
    card_number: str
    expiry: str
    amount: float
    description: str


class StateTransitionRequest(BaseModel):
    transaction_id: str


class RefundRequest(BaseModel):
    transaction_id: str
    refund_amount: float


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/ledger")
def get_ledger():
    return {
        "balance": round(ledger_store["balance"], 2),
        "transactions": list(ledger_store["transactions"].values())
    }


@app.post("/api/payment/initiate")
def initiate_payment(req: PaymentInitiateRequest):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    tx_id = f"TX-{uuid.uuid4().hex[:8].upper()}"
    tx_record = {
        "id": tx_id,
        "card_number": req.card_number[-4:],
        "amount": round(req.amount, 2),
        "description": req.description,
        "status": "Initiated",
        "refunded_amount": 0.0,
        "history": ["Initiated"]
    }
    ledger_store["transactions"][tx_id] = tx_record
    return {"success": True, "transaction": tx_record}


@app.post("/api/payment/authorize")
def authorize_payment(req: StateTransitionRequest):
    tx_id = req.transaction_id
    if tx_id not in ledger_store["transactions"]:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    tx = ledger_store["transactions"][tx_id]
    if tx["status"] != "Initiated":
        raise HTTPException(status_code=400, detail=f"Cannot authorize transaction in state '{tx['status']}'")
    
    tx["status"] = "Authorized"
    tx["history"].append("Authorized")
    return {"success": True, "transaction": tx}


@app.post("/api/payment/process")
def process_payment(req: StateTransitionRequest):
    tx_id = req.transaction_id
    if tx_id not in ledger_store["transactions"]:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    tx = ledger_store["transactions"][tx_id]
    if tx["status"] != "Authorized":
        raise HTTPException(status_code=400, detail=f"Cannot set to pending from state '{tx['status']}'")
    
    tx["status"] = "Pending"
    tx["history"].append("Pending")
    return {"success": True, "transaction": tx}


@app.post("/api/payment/complete")
def complete_payment(req: StateTransitionRequest):
    tx_id = req.transaction_id
    if tx_id not in ledger_store["transactions"]:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    tx = ledger_store["transactions"][tx_id]
    if tx["status"] not in ["Authorized", "Pending"]:
        raise HTTPException(status_code=400, detail=f"Cannot complete transaction in state '{tx['status']}'")
    
    # Complete payment and deduct from customer ledger balance
    tx["status"] = "Completed"
    tx["history"].append("Completed")
    ledger_store["balance"] -= tx["amount"]
    
    return {
        "success": True,
        "transaction": tx,
        "new_balance": round(ledger_store["balance"], 2)
    }


@app.post("/api/payment/refund")
def refund_payment(req: RefundRequest):
    tx_id = req.transaction_id
    if tx_id not in ledger_store["transactions"]:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    tx = ledger_store["transactions"][tx_id]
    if tx["status"] != "Completed":
        raise HTTPException(status_code=400, detail="Only completed transactions can be refunded")
    
    if req.refund_amount <= 0 or req.refund_amount > tx["amount"]:
        raise HTTPException(status_code=400, detail="Invalid refund amount")
    
    tx["refunded_amount"] += req.refund_amount
    if tx["refunded_amount"] >= tx["amount"]:
        tx["status"] = "Refunded"
    else:
        tx["status"] = "Partially Refunded"
    
    tx["history"].append(tx["status"])
    # Credit back account balance
    ledger_store["balance"] += req.refund_amount
    
    return {
        "success": True,
        "transaction": tx,
        "new_balance": round(ledger_store["balance"], 2)
    }


@app.post("/api/reset")
def reset_ledger():
    ledger_store["balance"] = INITIAL_BALANCE
    ledger_store["transactions"] = {}
    return {"success": True, "balance": INITIAL_BALANCE}


@app.get("/", response_class=HTMLResponse)
def get_portal():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Lifecycle & Ledger Portal</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: #334155;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            margin: 0;
            padding: 24px;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
        }

        header {
            margin-bottom: 32px;
        }

        h1 {
            font-size: 2rem;
            margin: 0 0 8px 0;
            color: var(--text-primary);
        }

        p.subtitle {
            color: var(--text-secondary);
            margin: 0;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 32px;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 20px;
            color: #60a5fa;
        }

        .ledger-summary {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: linear-gradient(135deg, #1e3a8a 0%, #1e293b 100%);
            border: 1px solid #3b82f6;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
        }

        .ledger-val {
            font-size: 2.5rem;
            font-weight: 700;
            color: #34d399;
        }

        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            margin-bottom: 6px;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }

        input {
            width: 100%;
            padding: 10px 12px;
            background-color: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            color: white;
            box-sizing: border-box;
            font-size: 1rem;
        }

        input:focus {
            outline: none;
            border-color: var(--accent-blue);
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.95rem;
        }

        .btn-primary {
            background-color: var(--accent-blue);
            color: white;
            width: 100%;
        }

        .btn-primary:hover {
            background-color: #2563eb;
        }

        .btn-action {
            padding: 6px 12px;
            font-size: 0.85rem;
            margin-right: 6px;
        }

        .btn-authorize { background-color: #8b5cf6; color: white; }
        .btn-pending { background-color: var(--accent-yellow); color: black; }
        .btn-complete { background-color: var(--accent-green); color: white; }
        .btn-refund { background-color: var(--accent-red); color: white; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }

        th, td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background-color: #0f172a;
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-transform: uppercase;
        }

        .status-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .status-Initiated { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid #3b82f6; }
        .status-Authorized { background-color: rgba(139, 92, 246, 0.2); color: #c084fc; border: 1px solid #8b5cf6; }
        .status-Pending { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
        .status-Completed { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
        .status-Refunded { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
        .status-Partially-Refunded { background-color: rgba(249, 115, 22, 0.2); color: #fb923c; border: 1px solid #f97316; }

        .alert {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        .alert-success { background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }
        .alert-error { background-color: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }

        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 24px;
            border-radius: 12px;
            width: 400px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Payment Lifecycle & Ledger Simulation Portal</h1>
            <p class="subtitle">Simulate real-time authorization, pending settlement, completion state machines, and ledger balance math.</p>
        </header>

        <div id="status-alert" class="alert"></div>

        <div class="ledger-summary">
            <div>
                <div style="color: var(--text-secondary); font-size: 0.9rem;">ACCOUNT LEDGER BALANCE</div>
                <div id="ledger-balance" class="ledger-val">$1,000.00</div>
            </div>
            <button class="btn btn-action" onclick="resetLedger()" style="background:#475569; color:white;">Reset Ledger</button>
        </div>

        <div class="grid">
            <div class="card">
                <h2 class="card-title">Initiate Payment Charge</h2>
                <form id="payment-form" onsubmit="handleInitiate(event)">
                    <div class="form-group">
                        <label for="card-number">Card Number</label>
                        <input type="text" id="card-number" required value="4532 9812 3456 7890">
                    </div>
                    <div class="form-group">
                        <label for="card-expiry">Expiry Date</label>
                        <input type="text" id="card-expiry" required value="12/28">
                    </div>
                    <div class="form-group">
                        <label for="charge-amount">Amount ($)</label>
                        <input type="number" step="0.01" id="charge-amount" required value="150.00">
                    </div>
                    <div class="form-group">
                        <label for="charge-desc">Description</label>
                        <input type="text" id="charge-desc" required value="Cloud Software Subscription">
                    </div>
                    <button type="submit" id="btn-initiate-payment" class="btn btn-primary">Initiate Payment</button>
                </form>
            </div>

            <div class="card">
                <h2 class="card-title">Active Transaction Controls</h2>
                <div id="active-tx-container">
                    <p style="color: var(--text-secondary);">No active transaction selected. Initiate a payment or click a transaction row.</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2 class="card-title">Transaction Ledger History</h2>
            <table>
                <thead>
                    <tr>
                        <th>Transaction ID</th>
                        <th>Card End</th>
                        <th>Description</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="transaction-table-body">
                    <tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No transactions recorded</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Refund Modal -->
    <div id="refund-modal" class="modal">
        <div class="modal-content">
            <h3 style="margin-top:0; color: #60a5fa;">Process Transaction Refund</h3>
            <p id="refund-tx-info" style="color: var(--text-secondary); font-size: 0.9rem;"></p>
            <div class="form-group">
                <label for="refund-amount-input">Refund Amount ($)</label>
                <input type="number" step="0.01" id="refund-amount-input">
            </div>
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                <button class="btn" style="background:#475569; color:white;" onclick="closeRefundModal()">Cancel</button>
                <button id="btn-confirm-refund" class="btn btn-refund" onclick="confirmRefund()">Confirm Refund</button>
            </div>
        </div>
    </div>

    <script>
        let currentTxId = null;
        let refundTxId = null;

        async function fetchLedger() {
            const resp = await fetch('/api/ledger');
            const data = await resp.json();
            
            // Format balance
            document.getElementById('ledger-balance').innerText = '$' + data.balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            
            // Render table
            const tbody = document.getElementById('transaction-table-body');
            if (data.transactions.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No transactions recorded</td></tr>';
                return;
            }

            tbody.innerHTML = data.transactions.map(tx => {
                const statusClass = 'status-' + tx.status.replace(' ', '-');
                let actions = '';

                if (tx.status === 'Initiated') {
                    actions += `<button id="btn-authorize-${tx.id}" class="btn btn-action btn-authorize" onclick="authorizeTx('${tx.id}')">Authorize</button>`;
                }
                if (tx.status === 'Authorized') {
                    actions += `<button id="btn-pending-${tx.id}" class="btn btn-action btn-pending" onclick="processTx('${tx.id}')">Pending</button>`;
                    actions += `<button id="btn-complete-${tx.id}" class="btn btn-action btn-complete" onclick="completeTx('${tx.id}')">Complete</button>`;
                }
                if (tx.status === 'Pending') {
                    actions += `<button id="btn-complete-${tx.id}" class="btn btn-action btn-complete" onclick="completeTx('${tx.id}')">Complete</button>`;
                }
                if (tx.status === 'Completed' || tx.status === 'Partially Refunded') {
                    actions += `<button id="btn-refund-${tx.id}" class="btn btn-action btn-refund" onclick="openRefundModal('${tx.id}', ${tx.amount - tx.refunded_amount})">Refund</button>`;
                }

                return `
                    <tr id="row-${tx.id}">
                        <td><strong>${tx.id}</strong></td>
                        <td>**** ${tx.card_number}</td>
                        <td>${tx.description}</td>
                        <td>$${tx.amount.toFixed(2)}</td>
                        <td><span id="status-${tx.id}" class="status-badge ${statusClass}">${tx.status}</span></td>
                        <td>${actions}</td>
                    </tr>
                `;
            }).join('');

            if (currentTxId) {
                const active = data.transactions.find(t => t.id === currentTxId);
                if (active) renderActiveControls(active);
            }
        }

        function showAlert(msg, type = 'success') {
            const alert = document.getElementById('status-alert');
            alert.className = `alert alert-${type}`;
            alert.innerText = msg;
            alert.style.display = 'block';
            setTimeout(() => { alert.style.display = 'none'; }, 4000);
        }

        async function handleInitiate(e) {
            e.preventDefault();
            const payload = {
                card_number: document.getElementById('card-number').value,
                expiry: document.getElementById('card-expiry').value,
                amount: parseFloat(document.getElementById('charge-amount').value),
                description: document.getElementById('charge-desc').value
            };

            const resp = await fetch('/api/payment/initiate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            if (resp.ok) {
                currentTxId = data.transaction.id;
                showAlert(`Payment ${currentTxId} Initiated successfully.`);
                renderActiveControls(data.transaction);
                fetchLedger();
            } else {
                showAlert(data.detail || 'Failed to initiate payment', 'error');
            }
        }

        function renderActiveControls(tx) {
            const container = document.getElementById('active-tx-container');
            container.innerHTML = `
                <div style="font-size: 1.1rem; font-weight: bold; color: #f8fafc; margin-bottom: 8px;">
                    Active Transaction: <span id="active-tx-id">${tx.id}</span>
                </div>
                <div style="margin-bottom: 12px;">Amount: $${tx.amount.toFixed(2)} | Current Status: <span class="status-badge status-${tx.status.replace(' ', '-')}">${tx.status}</span></div>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    ${tx.status === 'Initiated' ? `<button id="btn-authorize" class="btn btn-action btn-authorize" onclick="authorizeTx('${tx.id}')">Authorize Payment</button>` : ''}
                    ${tx.status === 'Authorized' ? `<button id="btn-pending" class="btn btn-action btn-pending" onclick="processTx('${tx.id}')">Move to Pending</button>` : ''}
                    ${(tx.status === 'Authorized' || tx.status === 'Pending') ? `<button id="btn-complete" class="btn btn-action btn-complete" onclick="completeTx('${tx.id}')">Complete & Settle</button>` : ''}
                    ${(tx.status === 'Completed' || tx.status === 'Partially Refunded') ? `<button id="btn-refund" class="btn btn-action btn-refund" onclick="openRefundModal('${tx.id}', ${tx.amount - tx.refunded_amount})">Initiate Refund</button>` : ''}
                    <button id="btn-auto-lifecycle" class="btn btn-action" style="background:#3b82f6; color:white;" onclick="autoRunLifecycle('${tx.id}')">Auto-Run Lifecycle</button>
                </div>
            `;
        }

        async function authorizeTx(txId) {
            const resp = await fetch('/api/payment/authorize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transaction_id: txId })
            });
            if (resp.ok) {
                showAlert(`Transaction ${txId} Authorized.`);
                fetchLedger();
            }
        }

        async function processTx(txId) {
            const resp = await fetch('/api/payment/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transaction_id: txId })
            });
            if (resp.ok) {
                showAlert(`Transaction ${txId} set to Pending.`);
                fetchLedger();
            }
        }

        async function completeTx(txId) {
            const resp = await fetch('/api/payment/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transaction_id: txId })
            });
            if (resp.ok) {
                const data = await resp.json();
                showAlert(`Transaction ${txId} Completed. Account ledger updated.`);
                fetchLedger();
            }
        }

        async function autoRunLifecycle(txId) {
            await authorizeTx(txId);
            await new Promise(r => setTimeout(r, 200));
            await processTx(txId);
            await new Promise(r => setTimeout(r, 200));
            await completeTx(txId);
        }

        function openRefundModal(txId, maxRefundable) {
            refundTxId = txId;
            document.getElementById('refund-tx-info').innerText = `Refunding ${txId} (Max refundable: $${maxRefundable.toFixed(2)})`;
            document.getElementById('refund-amount-input').value = maxRefundable.toFixed(2);
            document.getElementById('refund-modal').style.display = 'flex';
        }

        function closeRefundModal() {
            document.getElementById('refund-modal').style.display = 'none';
        }

        async function confirmRefund() {
            const amount = parseFloat(document.getElementById('refund-amount-input').value);
            const resp = await fetch('/api/payment/refund', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ transaction_id: refundTxId, refund_amount: amount })
            });
            if (resp.ok) {
                closeRefundModal();
                showAlert(`Refund of $${amount.toFixed(2)} processed for ${refundTxId}. Ledger balance updated.`);
                fetchLedger();
            } else {
                const data = await resp.json();
                showAlert(data.detail || 'Refund failed', 'error');
            }
        }

        async function resetLedger() {
            await fetch('/api/reset', { method: 'POST' });
            currentTxId = null;
            document.getElementById('active-tx-container').innerHTML = '<p style="color: var(--text-secondary);">No active transaction selected.</p>';
            showAlert('Ledger and transactions reset to default.');
            fetchLedger();
        }

        // Initial fetch
        fetchLedger();
    </script>
</body>
</html>
    """
