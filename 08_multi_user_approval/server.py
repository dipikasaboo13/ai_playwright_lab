from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Multi-User Approval Server")

# In-memory storage for requests
requests_db: List[Dict[str, Any]] = []
request_id_counter = 1

class RequestCreate(BaseModel):
    title: str
    amount: float

class RequestResponse(BaseModel):
    id: int
    title: str
    amount: float
    status: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/requests", response_model=List[RequestResponse])
def get_requests():
    return requests_db

@app.get("/api/requests/{request_id}", response_model=RequestResponse)
def get_request(request_id: int):
    for req in requests_db:
        if req["id"] == request_id:
            return req
    raise HTTPException(status_code=404, detail="Request not found")

@app.post("/api/requests", response_model=RequestResponse)
def create_request(data: RequestCreate):
    global request_id_counter
    new_req = {
        "id": request_id_counter,
        "title": data.title,
        "amount": data.amount,
        "status": "Pending"
    }
    request_id_counter += 1
    requests_db.append(new_req)
    return new_req

@app.post("/api/requests/{request_id}/approve", response_model=RequestResponse)
def approve_request(request_id: int):
    for req in requests_db:
        if req["id"] == request_id:
            req["status"] = "Approved"
            return req
    raise HTTPException(status_code=404, detail="Request not found")

@app.get("/", response_class=HTMLResponse)
def get_ui():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-User Approval System</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --success: #22c55e;
            --warning: #eab308;
            --border: #334155;
        }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        h1 {
            font-size: 1.875rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-main);
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .card h2 {
            font-size: 1.25rem;
            margin-top: 0;
            margin-bottom: 1rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        label {
            font-size: 0.875rem;
            color: var(--text-muted);
        }

        input[type="text"], input[type="number"] {
            background-color: var(--bg-color);
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 0.625rem 0.875rem;
            border-radius: 0.375rem;
            font-size: 1rem;
            outline: none;
        }

        input:focus {
            border-color: var(--primary);
        }

        button {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.625rem 1.25rem;
            border-radius: 0.375rem;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 0.5rem;
        }

        th, td {
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 600;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.625rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
        }

        .badge-pending {
            background-color: rgba(234, 179, 8, 0.15);
            color: var(--warning);
            border: 1px solid rgba(234, 179, 8, 0.3);
        }

        .badge-approved {
            background-color: rgba(34, 197, 94, 0.15);
            color: var(--success);
            border: 1px solid rgba(34, 197, 94, 0.3);
        }

        .btn-approve {
            background-color: var(--success);
            font-size: 0.85rem;
            padding: 0.4rem 0.8rem;
        }

        .btn-approve:hover {
            background-color: #16a34a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Multi-User Approval Portal</h1>
        
        <div class="card">
            <h2>Submit Approval Request</h2>
            <form id="request-form">
                <div class="form-group">
                    <label for="request-title">Request Title</label>
                    <input type="text" id="request-title" required placeholder="e.g. Server Upgrade">
                </div>
                <div class="form-group">
                    <label for="request-amount">Amount ($)</label>
                    <input type="number" id="request-amount" required step="0.01" placeholder="e.g. 1500.00">
                </div>
                <button type="submit" id="submit-request-btn">Submit Request</button>
            </form>
        </div>

        <div class="card">
            <h2>Approval Queue & Requests</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="requests-tbody">
                    <!-- Dynamic Rows -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        async function fetchRequests() {
            try {
                const res = await fetch('/api/requests');
                const data = await res.json();
                const tbody = document.getElementById('requests-tbody');
                tbody.innerHTML = '';

                data.forEach(req => {
                    const tr = document.createElement('tr');
                    tr.setAttribute('data-id', req.id);
                    
                    const statusBadge = req.status === 'Approved'
                        ? `<span class="badge badge-approved" id="status-${req.id}">${req.status}</span>`
                        : `<span class="badge badge-pending" id="status-${req.id}">${req.status}</span>`;

                    const actionBtn = req.status === 'Pending'
                        ? `<button class="btn-approve" id="approve-btn-${req.id}" onclick="approveRequest(${req.id})">Approve</button>`
                        : `<span style="color: var(--text-muted); font-size: 0.875rem;">Completed</span>`;

                    tr.innerHTML = `
                        <td>#${req.id}</td>
                        <td class="req-title">${req.title}</td>
                        <td class="req-amount">$${req.amount.toFixed(2)}</td>
                        <td>${statusBadge}</td>
                        <td>${actionBtn}</td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (err) {
                console.error('Failed to fetch requests', err);
            }
        }

        async function approveRequest(id) {
            try {
                await fetch(`/api/requests/${id}/approve`, { method: 'POST' });
                fetchRequests();
            } catch (err) {
                console.error('Failed to approve request', err);
            }
        }

        document.getElementById('request-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('request-title').value;
            const amount = parseFloat(document.getElementById('request-amount').value);

            await fetch('/api/requests', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, amount })
            });

            document.getElementById('request-title').value = '';
            document.getElementById('request-amount').value = '';
            fetchRequests();
        });

        // Initial fetch and auto-refresh for multi-user status sync
        fetchRequests();
        setInterval(fetchRequests, 1000);
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
