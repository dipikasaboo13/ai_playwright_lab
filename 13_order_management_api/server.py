"""
FastAPI Backend & Interactive UI Dashboard for Project 13: Order Management with API Setup.
Provides RESTful API endpoints for order CRUD operations and serves a dynamic management dashboard.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
import datetime

app = FastAPI(title="Order Management API & Dashboard", version="1.0.0")

# In-memory storage for order records
orders_db = {}
order_counter = 1000


class OrderItem(BaseModel):
    name: str
    qty: int = 1
    price: float


class OrderCreateRequest(BaseModel):
    customer_name: str
    items: List[OrderItem] = []
    total_price: Optional[float] = None
    status: Optional[str] = "Pending"


class OrderUpdateRequest(BaseModel):
    status: str


@app.get("/health")
def health_check():
    """Health check endpoint for fixture initialization polling."""
    return {"status": "ok"}


@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
def create_order(order_req: OrderCreateRequest):
    """
    API Endpoint: Create order record.
    Generates a unique order_id and stores order details.
    """
    global order_counter
    order_counter += 1
    order_id = f"ORD-{order_counter}"
    
    # Calculate total price if not explicitly provided
    computed_total = order_req.total_price
    if computed_total is None:
        computed_total = sum(item.price * item.qty for item in order_req.items)
        
    order_record = {
        "order_id": order_id,
        "customer_name": order_req.customer_name,
        "items": [item.model_dump() for item in order_req.items],
        "total_price": round(computed_total, 2),
        "status": order_req.status or "Pending",
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    orders_db[order_id] = order_record
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=order_record)


@app.get("/api/v1/orders")
def list_orders():
    """API Endpoint: List all orders."""
    return list(orders_db.values())


@app.get("/api/v1/orders/{order_id}")
def get_order(order_id: str):
    """API Endpoint: Retrieve specific order by ID."""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found")
    return orders_db[order_id]


@app.patch("/api/v1/orders/{order_id}")
@app.put("/api/v1/orders/{order_id}")
def update_order_status(order_id: str, update_req: OrderUpdateRequest):
    """API Endpoint: Update status of an existing order."""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found")
    
    orders_db[order_id]["status"] = update_req.status
    return orders_db[order_id]


@app.delete("/api/v1/orders/{order_id}")
def delete_order(order_id: str):
    """API Endpoint: Delete order record (Teardown)."""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order '{order_id}' not found")
    
    deleted_order = orders_db.pop(order_id)
    return {"message": f"Order {order_id} deleted successfully", "order_id": order_id}


@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the Order Management Interactive Dashboard UI."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Management Dashboard</title>
    <style>
        :root {
            --primary: #4f46e5;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
            --success: #10b981;
            --warning: #f59e0b;
            --info: #3b82f6;
            --danger: #ef4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--bg);
            color: var(--text);
            padding: 2rem;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        h1 {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
        }

        .controls {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        input[type="text"], select {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus, select:focus {
            border-color: var(--primary);
        }

        input[type="text"] {
            flex-grow: 1;
        }

        .table-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th, td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border);
        }

        th {
            background-color: #0f172a;
            color: var(--text-muted);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background-color: #24334a;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .badge-Pending { background-color: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-Processing { background-color: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        .badge-Shipped { background-color: rgba(16, 185, 129, 0.2); color: #34d399; }
        .badge-Delivered { background-color: rgba(168, 85, 247, 0.2); color: #c084fc; }
        .badge-Cancelled { background-color: rgba(239, 68, 68, 0.2); color: #f87171; }

        .status-select {
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
        }

        .empty-state {
            padding: 3rem;
            text-align: center;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Order Management Dashboard</h1>
            <span id="order-count-tag" style="color: var(--text-muted);">0 Orders Loaded</span>
        </header>

        <div class="controls">
            <input type="text" id="search-input" placeholder="Search by Order ID or Customer Name..." onkeyup="renderOrders()">
            <select id="status-filter" onchange="renderOrders()">
                <option value="ALL">All Statuses</option>
                <option value="Pending">Pending</option>
                <option value="Processing">Processing</option>
                <option value="Shipped">Shipped</option>
                <option value="Delivered">Delivered</option>
                <option value="Cancelled">Cancelled</option>
            </select>
        </div>

        <div class="table-card">
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Total Price</th>
                        <th>Current Status</th>
                        <th>Update Status</th>
                    </tr>
                </thead>
                <tbody id="orders-list">
                    <!-- Dynamic Order Rows -->
                </tbody>
            </table>
            <div id="empty-msg" class="empty-state" style="display: none;">
                No orders match your search criteria.
            </div>
        </div>
    </div>

    <script>
        let allOrders = [];

        async function fetchOrders() {
            try {
                const res = await fetch('/api/v1/orders');
                if (res.ok) {
                    allOrders = await res.json();
                    renderOrders();
                }
            } catch (err) {
                console.error("Failed to fetch orders:", err);
            }
        }

        function renderOrders() {
            const query = document.getElementById('search-input').value.trim().toLowerCase();
            const filter = document.getElementById('status-filter').value;
            const tbody = document.getElementById('orders-list');
            const emptyMsg = document.getElementById('empty-msg');
            const countTag = document.getElementById('order-count-tag');

            const filtered = allOrders.filter(order => {
                const matchesQuery = order.order_id.toLowerCase().includes(query) || 
                                     order.customer_name.toLowerCase().includes(query);
                const matchesFilter = (filter === 'ALL') || (order.status === filter);
                return matchesQuery && matchesFilter;
            });

            countTag.textContent = `${filtered.length} Order(s) Displayed`;
            tbody.innerHTML = '';

            if (filtered.length === 0) {
                emptyMsg.style.display = 'block';
                return;
            }

            emptyMsg.style.display = 'none';

            filtered.forEach(order => {
                const tr = document.createElement('tr');
                tr.setAttribute('data-order-id', order.order_id);
                
                tr.innerHTML = `
                    <td class="order-id" style="font-weight: 600; color: #a5b4fc;">${order.order_id}</td>
                    <td class="customer-name">${order.customer_name}</td>
                    <td class="total-price">$${order.total_price.toFixed(2)}</td>
                    <td><span class="badge badge-${order.status}" id="status-badge-${order.order_id}">${order.status}</span></td>
                    <td>
                        <select class="status-select" id="status-select-${order.order_id}" onchange="updateStatus('${order.order_id}', this.value)">
                            <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''}>Pending</option>
                            <option value="Processing" ${order.status === 'Processing' ? 'selected' : ''}>Processing</option>
                            <option value="Shipped" ${order.status === 'Shipped' ? 'selected' : ''}>Shipped</option>
                            <option value="Delivered" ${order.status === 'Delivered' ? 'selected' : ''}>Delivered</option>
                            <option value="Cancelled" ${order.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                        </select>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        async function updateStatus(orderId, newStatus) {
            try {
                const res = await fetch(`/api/v1/orders/${orderId}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: newStatus })
                });

                if (res.ok) {
                    const updated = await res.json();
                    const target = allOrders.find(o => o.order_id === orderId);
                    if (target) target.status = updated.status;
                    renderOrders();
                } else {
                    alert('Failed to update status on server');
                }
            } catch (err) {
                console.error("Error updating order status:", err);
            }
        }

        // Poll for updates every 2 seconds
        setInterval(fetchOrders, 2000);
        fetchOrders();
    </script>
</body>
</html>
"""
