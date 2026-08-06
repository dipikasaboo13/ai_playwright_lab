"""
FastAPI Server for Project 11: Role-Based Employee Management Portal.
Provides endpoints for authentication, employee CRUD operations, role-based UI rendering,
and a health check endpoint for test setup synchronization.
"""

from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Role-Based Employee Management Portal")

# In-memory user database
users_db: List[Dict[str, str]] = [
    {
        "id": "1",
        "name": "Alice Smith",
        "email": "alice@company.com",
        "role": "Admin",
        "status": "Active"
    },
    {
        "id": "2",
        "name": "Bob Jones",
        "email": "bob@company.com",
        "role": "Sales Specialist",
        "status": "Active"
    }
]

user_id_counter = 3


class UserCreate(BaseModel):
    name: str
    email: str
    role: str


class StatusUpdate(BaseModel):
    status: str


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/health")
def health_check():
    """Health check endpoint for pytest module server wait loop."""
    return {"status": "ok"}


@app.post("/api/login")
def login(creds: LoginRequest):
    """Authenticate user and return role information."""
    if creds.username == "admin" and creds.password == "admin123":
        return {"username": "admin", "role": "Admin", "name": "System Administrator"}
    elif creds.username == "emp_sales" and creds.password == "emp123":
        return {"username": "emp_sales", "role": "Sales Specialist", "name": "Bob Jones"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/api/users")
def get_users():
    """Retrieve all employee user records."""
    return users_db


@app.post("/api/users")
def create_user(user: UserCreate):
    """Create a new employee profile."""
    global user_id_counter
    new_user = {
        "id": str(user_id_counter),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": "Active"
    }
    user_id_counter += 1
    users_db.append(new_user)
    return new_user


@app.patch("/api/users/{user_id}/status")
def update_user_status(user_id: str, payload: StatusUpdate):
    """Update employee account status (e.g. Active vs Disabled)."""
    for user in users_db:
        if user["id"] == user_id:
            user["status"] = payload.status
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/", response_class=HTMLResponse)
def get_portal_ui():
    """Render the Role-Based Employee Management Portal HTML UI."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Management Portal</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #090d16;
            --card-bg: #131b2e;
            --card-border: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-primary: #6366f1;
            --accent-hover: #4f46e5;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Header / Navbar */
        header {
            background-color: var(--card-bg);
            border-bottom: 1px solid var(--card-border);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .logo span {
            color: var(--accent-primary);
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .role-badge {
            background-color: rgba(99, 102, 241, 0.15);
            color: var(--accent-primary);
            border: 1px solid rgba(99, 102, 241, 0.3);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .btn-logout {
            background: transparent;
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 0.4rem 0.8rem;
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.85rem;
        }

        .btn-logout:hover {
            color: var(--text-main);
            border-color: var(--text-muted);
        }

        /* Navigation Bar */
        nav {
            background-color: #0e1424;
            border-bottom: 1px solid var(--card-border);
            padding: 0 2rem;
            display: flex;
            gap: 1rem;
        }

        .nav-item {
            padding: 0.75rem 1rem;
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            border-bottom: 2px solid transparent;
            cursor: pointer;
        }

        .nav-item.active {
            color: var(--accent-primary);
            border-bottom-color: var(--accent-primary);
        }

        /* Container Layout */
        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            width: 100%;
            flex: 1;
        }

        /* Login Card */
        .auth-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 70vh;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        .login-card {
            width: 100%;
            max-width: 400px;
        }

        .card h2 {
            font-size: 1.25rem;
            margin-bottom: 1.5rem;
            color: var(--text-main);
        }

        .form-group {
            margin-bottom: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.875rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        input[type="text"], input[type="password"], input[type="email"], select {
            background-color: var(--bg-dark);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 0.65rem 0.85rem;
            border-radius: 0.375rem;
            font-size: 0.95rem;
            outline: none;
        }

        input:focus, select:focus {
            border-color: var(--accent-primary);
        }

        .btn-primary {
            background-color: var(--accent-primary);
            color: white;
            border: none;
            padding: 0.75rem 1.25rem;
            border-radius: 0.375rem;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.2s;
        }

        .btn-primary:hover {
            background-color: var(--accent-hover);
        }

        /* Grid Layout for Admin Dashboard */
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 1.5rem;
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Table Styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }

        th, td {
            padding: 0.85rem 1rem;
            text-align: left;
            border-bottom: 1px solid var(--card-border);
            font-size: 0.9rem;
        }

        th {
            color: var(--text-muted);
            font-weight: 600;
            background-color: rgba(15, 23, 42, 0.4);
        }

        .status-badge {
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.775rem;
            font-weight: 600;
            display: inline-block;
        }

        .status-active {
            background-color: rgba(16, 185, 129, 0.15);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .status-disabled {
            background-color: rgba(239, 68, 68, 0.15);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .btn-action {
            padding: 0.35rem 0.75rem;
            border-radius: 0.375rem;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            border: none;
        }

        .btn-disable {
            background-color: rgba(239, 68, 68, 0.2);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.4);
        }

        .btn-disable:hover {
            background-color: var(--danger);
            color: white;
        }

        .btn-enable {
            background-color: rgba(16, 185, 129, 0.2);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.4);
        }

        .btn-enable:hover {
            background-color: var(--success);
            color: white;
        }

        .error-message {
            color: var(--danger);
            font-size: 0.85rem;
            margin-top: 0.5rem;
            display: none;
        }

        /* Hidden view helper */
        .hidden {
            display: none !important;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="logo">
            <span>🛡️</span> Enterprise Portal
        </div>
        <div id="header-user-section" class="user-info hidden">
            <span id="user-display-name">User</span>
            <span id="user-role-badge" class="role-badge">Role</span>
            <button class="btn-logout" onclick="logout()">Log Out</button>
        </div>
    </header>

    <!-- Navigation Bar -->
    <nav id="app-nav" class="hidden">
        <a id="nav-dashboard" class="nav-item active">Dashboard</a>
        <a id="nav-profile" class="nav-item">My Profile</a>
        <a id="nav-sales" class="nav-item">Sales Reports</a>
        <a id="nav-admin-settings" class="nav-item">Admin Settings</a>
        <a id="nav-system-logs" class="nav-item">System Logs</a>
    </nav>

    <!-- Main Body Container -->
    <div class="main-container">

        <!-- Login Section -->
        <div id="auth-section" class="auth-wrapper">
            <div class="card login-card">
                <h2>Sign In</h2>
                <form id="login-form">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" required placeholder="admin or emp_sales">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" required placeholder="••••••••">
                    </div>
                    <button type="submit" id="btn-login" class="btn-primary">Log In</button>
                    <div id="login-error" class="error-message">Invalid credentials</div>
                </form>
            </div>
        </div>

        <!-- Portal Dashboard Section -->
        <div id="portal-section" class="hidden">
            
            <!-- Employee / Sales Specialist View -->
            <div id="employee-dashboard" class="hidden">
                <div class="card">
                    <h2>Employee Workspace</h2>
                    <p style="color: var(--text-muted); margin-bottom: 1rem;">Welcome to your role-specific dashboard. You have access to profile parameters and sales reporting tools.</p>
                    <div style="display: flex; gap: 1rem;">
                        <div class="card" style="flex: 1; background: #0f172a;">
                            <h3 style="font-size: 1rem; color: var(--accent-primary);">Sales Targets</h3>
                            <p style="font-size: 1.5rem; font-weight: 700; margin-top: 0.5rem;">$124,500</p>
                        </div>
                        <div class="card" style="flex: 1; background: #0f172a;">
                            <h3 style="font-size: 1rem; color: var(--success);">Active Deals</h3>
                            <p style="font-size: 1.5rem; font-weight: 700; margin-top: 0.5rem;">18 Pending</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Admin Management View -->
            <div id="admin-dashboard" class="dashboard-grid hidden">
                
                <!-- Employee Creation Form -->
                <div class="card">
                    <h2>Create Employee Profile</h2>
                    <form id="create-user-form">
                        <div class="form-group">
                            <label for="employee-name">Full Name</label>
                            <input type="text" id="employee-name" required placeholder="e.g. Jane Doe">
                        </div>
                        <div class="form-group">
                            <label for="employee-email">Email Address</label>
                            <input type="email" id="employee-email" required placeholder="jane@company.com">
                        </div>
                        <div class="form-group">
                            <label for="employee-role">Assigned Role</label>
                            <select id="employee-role" required>
                                <option value="Sales Specialist">Sales Specialist</option>
                                <option value="Support Agent">Support Agent</option>
                                <option value="Accountant">Accountant</option>
                                <option value="Admin">Admin</option>
                            </select>
                        </div>
                        <button type="submit" id="btn-create-employee" class="btn-primary">Add Employee</button>
                    </form>
                </div>

                <!-- Employee Directory Table -->
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h2>Employee Directory</h2>
                        <button id="btn-delete-user" class="btn-action btn-disable" style="font-size: 0.85rem;">Delete Records</button>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Role</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="users-tbody">
                            <!-- Dynamic Employee Rows -->
                        </tbody>
                    </table>
                </div>

            </div>

        </div>

    </div>

    <script>
        let currentUser = null;

        // Login Handler
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');

            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                if (!res.ok) {
                    errorDiv.style.display = 'block';
                    return;
                }

                errorDiv.style.display = 'none';
                currentUser = await res.json();
                renderPortal();
            } catch (err) {
                console.error("Login failed", err);
                errorDiv.style.display = 'block';
            }
        });

        function logout() {
            currentUser = null;
            document.getElementById('auth-section').classList.remove('hidden');
            document.getElementById('portal-section').classList.add('hidden');
            document.getElementById('header-user-section').classList.add('hidden');
            document.getElementById('app-nav').classList.add('hidden');
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        }

        async function renderPortal() {
            if (!currentUser) return;

            document.getElementById('auth-section').classList.add('hidden');
            document.getElementById('portal-section').classList.remove('hidden');
            
            // Render Header User Info
            document.getElementById('header-user-section').classList.remove('hidden');
            document.getElementById('user-display-name').textContent = currentUser.name;
            document.getElementById('user-role-badge').textContent = currentUser.role;

            // Render Nav Bar according to role
            const nav = document.getElementById('app-nav');
            nav.classList.remove('hidden');

            const navAdminSettings = document.getElementById('nav-admin-settings');
            const navSystemLogs = document.getElementById('nav-system-logs');
            const navSales = document.getElementById('nav-sales');

            if (currentUser.role === 'Admin') {
                navAdminSettings.classList.remove('hidden');
                navSystemLogs.classList.remove('hidden');
                navSales.classList.remove('hidden');
                
                document.getElementById('admin-dashboard').classList.remove('hidden');
                document.getElementById('employee-dashboard').classList.add('hidden');
                fetchUsers();
            } else {
                // Role-restricted for Employee/Sales Specialist
                navAdminSettings.classList.add('hidden');
                navSystemLogs.classList.add('hidden');
                navSales.classList.remove('hidden');

                document.getElementById('admin-dashboard').classList.add('hidden');
                document.getElementById('employee-dashboard').classList.remove('hidden');
            }
        }

        async function fetchUsers() {
            try {
                const res = await fetch('/api/users');
                const users = await res.json();
                const tbody = document.getElementById('users-tbody');
                tbody.innerHTML = '';

                users.forEach(u => {
                    const tr = document.createElement('tr');
                    tr.setAttribute('data-id', u.id);

                    const statusClass = u.status === 'Active' ? 'status-active' : 'status-disabled';
                    const actionBtnText = u.status === 'Active' ? 'Disable' : 'Enable';
                    const actionBtnClass = u.status === 'Active' ? 'btn-disable' : 'btn-enable';

                    tr.innerHTML = `
                        <td>#${u.id}</td>
                        <td class="user-name">${u.name}</td>
                        <td class="user-email">${u.email}</td>
                        <td class="user-role">${u.role}</td>
                        <td><span id="status-badge-${u.id}" class="status-badge ${statusClass}">${u.status}</span></td>
                        <td>
                            <button id="btn-toggle-status-${u.id}" class="btn-action ${actionBtnClass}" onclick="toggleStatus('${u.id}', '${u.status}')">
                                ${actionBtnText}
                            </button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (err) {
                console.error("Failed to fetch users", err);
            }
        }

        async function toggleStatus(userId, currentStatus) {
            const newStatus = currentStatus === 'Active' ? 'Disabled' : 'Active';
            try {
                await fetch(`/api/users/${userId}/status`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: newStatus })
                });
                fetchUsers();
            } catch (err) {
                console.error("Failed to update user status", err);
            }
        }

        // Employee Creation Handler
        document.getElementById('create-user-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('employee-name').value;
            const email = document.getElementById('employee-email').value;
            const role = document.getElementById('employee-role').value;

            try {
                await fetch('/api/users', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, role })
                });

                document.getElementById('employee-name').value = '';
                document.getElementById('employee-email').value = '';
                fetchUsers();
            } catch (err) {
                console.error("Failed to create user", err);
            }
        });
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
