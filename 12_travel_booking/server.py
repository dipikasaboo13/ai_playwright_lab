"""
FastAPI application for Project 12: End-to-End Travel Booking Flow.
Provides UI views and API endpoints for searching flights/hotels, applying filters,
handling form validations, and generating booking confirmations.
"""

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

app = FastAPI(title="Travel Booking Portal")

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkyWay Travel Booking Portal</title>
    <style>
        :root {
            --primary: #0284c7;
            --primary-hover: #0369a1;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --border: #334155;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #ef4444;
            --success: #22c55e;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, sans-serif;
        }

        body {
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 900px;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
        }

        header h1 {
            font-size: 2.2rem;
            color: #38bdf8;
            margin-bottom: 0.5rem;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 0.5rem;
            color: #e2e8f0;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        label {
            font-size: 0.875rem;
            color: var(--text-muted);
            font-weight: 500;
        }

        input, select {
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 0.6rem 0.8rem;
            color: var(--text);
            font-size: 0.95rem;
            outline: none;
        }

        input:focus, select:focus {
            border-color: var(--primary);
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.75rem 1.25rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .btn:hover {
            background: var(--primary-hover);
        }

        .btn-success {
            background: var(--success);
        }

        .btn-success:hover {
            background: #16a34a;
        }

        .alert {
            padding: 0.8rem 1rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            display: none;
        }

        .alert-warning {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--danger);
            color: #fca5a5;
        }

        .alert-active {
            display: block;
        }

        .validation-error {
            color: var(--danger);
            font-size: 0.8rem;
            min-height: 1.1rem;
        }

        .flight-card {
            background: #0f172a;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }

        .flight-details h3 {
            font-size: 1rem;
            color: #38bdf8;
        }

        .flight-details p {
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }

        .flight-price {
            text-align: right;
        }

        .price-tag {
            font-size: 1.4rem;
            font-weight: 700;
            color: #4ade80;
        }

        .rating-tag {
            font-size: 0.8rem;
            color: #fde047;
            margin-bottom: 0.4rem;
        }

        .hidden {
            display: none !important;
        }

        .confirmation-badge {
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid var(--success);
            color: #86efac;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }

        .confirmation-badge h2 {
            margin-bottom: 0.5rem;
        }

        .summary-row {
            display: flex;
            justify-content: space-between;
            padding: 0.4rem 0;
            border-bottom: 1px dashed var(--border);
            font-size: 0.95rem;
        }

        .summary-row.total {
            border-bottom: none;
            font-weight: 700;
            font-size: 1.1rem;
            color: #38bdf8;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>✈️ SkyWay Travel Booking Portal</h1>
            <p style="color: var(--text-muted);">Find and book flights, hotels, and travel packages worldwide</p>
        </header>

        <!-- Search & Filter Section -->
        <div id="search-section" class="card">
            <div class="card-title">1. Search Flights & Accommodation</div>
            
            <div id="date-error-alert" class="alert alert-warning">
                ⚠️ Return date cannot be earlier than departure date. Please select valid travel dates.
            </div>

            <form id="search-form" onsubmit="handleSearch(event)">
                <div class="grid" style="margin-bottom: 1rem;">
                    <div class="form-group">
                        <label for="origin">Origin Location</label>
                        <select id="origin" required>
                            <option value="">Select origin...</option>
                            <option value="JFK" selected>New York (JFK)</option>
                            <option value="LHR">London (LHR)</option>
                            <option value="SFO">San Francisco (SFO)</option>
                            <option value="HND">Tokyo (HND)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="destination">Destination Location</label>
                        <select id="destination" required>
                            <option value="">Select destination...</option>
                            <option value="CDG" selected>Paris (CDG)</option>
                            <option value="DXB">Dubai (DXB)</option>
                            <option value="SYD">Sydney (SYD)</option>
                            <option value="FCO">Rome (FCO)</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="departure-date">Departure Date</label>
                        <input type="date" id="departure-date" value="2026-09-10" required>
                    </div>

                    <div class="form-group">
                        <label for="return-date">Return Date</label>
                        <input type="date" id="return-date" value="2026-09-20" required>
                    </div>
                </div>

                <div class="grid" style="margin-bottom: 1.5rem;">
                    <div class="form-group">
                        <label for="max-price">Max Budget ($): <span id="max-price-val">800</span></label>
                        <input type="range" id="max-price" min="200" max="1500" step="50" value="800" oninput="document.getElementById('max-price-val').innerText = this.value">
                    </div>

                    <div class="form-group">
                        <label for="min-rating">Minimum Star Rating</label>
                        <select id="min-rating">
                            <option value="1">1+ Stars</option>
                            <option value="2">2+ Stars</option>
                            <option value="3">3+ Stars</option>
                            <option value="4" selected>4+ Stars</option>
                            <option value="5">5 Stars Only</option>
                        </select>
                    </div>
                </div>

                <button type="submit" id="btn-search" class="btn" style="width: 100%;">Search Flight Packages</button>
            </form>
        </div>

        <!-- Search Results Section -->
        <div id="search-results-section" class="card hidden">
            <div class="card-title">2. Select Flight Package</div>
            <div id="results-container">
                <!-- Flight Options populated dynamically -->
            </div>
        </div>

        <!-- Passenger Form Section -->
        <div id="passenger-form-section" class="card hidden">
            <div class="card-title">3. Passenger & Contact Information</div>
            <form id="passenger-form" onsubmit="handleBookingSubmit(event)" novalidate>
                <div class="grid" style="margin-bottom: 1rem;">
                    <div class="form-group">
                        <label for="passenger-name">Full Name *</label>
                        <input type="text" id="passenger-name" placeholder="e.g. Alice Smith">
                        <div id="passenger-name-error" class="validation-error"></div>
                    </div>

                    <div class="form-group">
                        <label for="passenger-email">Email Address *</label>
                        <input type="email" id="passenger-email" placeholder="e.g. alice@example.com">
                        <div id="passenger-email-error" class="validation-error"></div>
                    </div>

                    <div class="form-group">
                        <label for="passenger-phone">Phone Number *</label>
                        <input type="tel" id="passenger-phone" placeholder="e.g. +1-555-0199">
                        <div id="passenger-phone-error" class="validation-error"></div>
                    </div>
                </div>

                <button type="submit" id="btn-confirm-booking" class="btn btn-success" style="width: 100%;">Confirm & Complete Booking</button>
            </form>
        </div>

        <!-- Booking Confirmation Section -->
        <div id="booking-confirmation-section" class="card hidden">
            <div class="card-title">4. Booking Confirmation</div>
            <div class="confirmation-badge">
                <h2>🎉 Travel Booking Confirmed!</h2>
                <p>Your reservation reference: <strong id="booking-reference" style="color: #38bdf8; font-size: 1.2rem;">TB-982415</strong></p>
            </div>

            <div style="margin-top: 1.5rem; background: #0f172a; padding: 1.25rem; border-radius: 8px; border: 1px solid var(--border);">
                <div class="summary-row">
                    <span>Passenger Name:</span>
                    <span id="summary-passenger-name">-</span>
                </div>
                <div class="summary-row">
                    <span>Route:</span>
                    <span id="summary-route">-</span>
                </div>
                <div class="summary-row">
                    <span>Travel Dates:</span>
                    <span id="summary-dates">-</span>
                </div>
                <div class="summary-row">
                    <span>Base Flight Fare:</span>
                    <span id="summary-base-fare">$0.00</span>
                </div>
                <div class="summary-row">
                    <span>Taxes & Service Fees (10%):</span>
                    <span id="summary-taxes">$0.00</span>
                </div>
                <div class="summary-row total">
                    <span>Total Price Paid:</span>
                    <span id="total-price">$0.00</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const flightDatabase = [
            { id: 1, airline: "Air France Express", route: "New York (JFK) -> Paris (CDG)", price: 550, rating: 4.5, dept: "08:30 AM", arr: "10:15 PM" },
            { id: 2, airline: "SkyWings Luxury", route: "New York (JFK) -> Paris (CDG)", price: 720, rating: 4.8, dept: "01:00 PM", arr: "03:30 AM" },
            { id: 3, airline: "Global Budget Air", route: "New York (JFK) -> Paris (CDG)", price: 950, rating: 3.9, dept: "06:00 PM", arr: "08:00 AM" }
        ];

        let selectedFlight = null;

        function handleSearch(event) {
            event.preventDefault();
            const depDate = document.getElementById("departure-date").value;
            const retDate = document.getElementById("return-date").value;
            const alertBox = document.getElementById("date-error-alert");

            // Clear alert
            alertBox.classList.remove("alert-active");

            // Validate dates
            if (depDate && retDate && retDate < depDate) {
                alertBox.classList.add("alert-active");
                document.getElementById("search-results-section").classList.add("hidden");
                return;
            }

            const maxPrice = parseFloat(document.getElementById("max-price").value);
            const minRating = parseFloat(document.getElementById("min-rating").value);

            const filtered = flightDatabase.filter(f => f.price <= maxPrice && f.rating >= minRating);

            const container = document.getElementById("results-container");
            container.innerHTML = "";

            if (filtered.length === 0) {
                container.innerHTML = `<p style="color: var(--text-muted); padding: 1rem 0;">No flights match your filter criteria. Try adjusting budget or rating.</p>`;
            } else {
                filtered.forEach(flight => {
                    const el = document.createElement("div");
                    el.className = "flight-card";
                    el.innerHTML = `
                        <div class="flight-details">
                            <h3>${flight.airline}</h3>
                            <p>${flight.route} | Dept: ${flight.dept} - Arr: ${flight.arr}</p>
                            <div class="rating-tag">★ ${flight.rating} / 5.0 Rating</div>
                        </div>
                        <div class="flight-price">
                            <div class="price-tag">$${flight.price}</div>
                            <button id="btn-select-flight-${flight.id}" class="btn" style="margin-top: 0.5rem;" onclick="selectFlight(${flight.id})">Select Flight</button>
                        </div>
                    `;
                    container.appendChild(el);
                });
            }

            document.getElementById("search-results-section").classList.remove("hidden");
        }

        function selectFlight(id) {
            selectedFlight = flightDatabase.find(f => f.id === id);
            document.getElementById("passenger-form-section").classList.remove("hidden");
            document.getElementById("passenger-form-section").scrollIntoView({ behavior: 'smooth' });
        }

        function handleBookingSubmit(event) {
            event.preventDefault();
            
            const nameInput = document.getElementById("passenger-name");
            const emailInput = document.getElementById("passenger-email");
            const phoneInput = document.getElementById("passenger-phone");

            const nameErr = document.getElementById("passenger-name-error");
            const emailErr = document.getElementById("passenger-email-error");
            const phoneErr = document.getElementById("passenger-phone-error");

            nameErr.innerText = "";
            emailErr.innerText = "";
            phoneErr.innerText = "";

            let isValid = true;

            if (!nameInput.value.trim()) {
                nameErr.innerText = "Full name is required.";
                isValid = false;
            }

            if (!emailInput.value.trim()) {
                emailErr.innerText = "Email address is required.";
                isValid = false;
            } else if (!emailInput.value.includes("@")) {
                emailErr.innerText = "Please enter a valid email address.";
                isValid = false;
            }

            if (!phoneInput.value.trim()) {
                phoneErr.innerText = "Phone number is required.";
                isValid = false;
            }

            if (!isValid) return;

            // Compute prices
            const baseFare = selectedFlight ? selectedFlight.price : 550;
            const taxes = baseFare * 0.10;
            const totalPrice = baseFare + taxes;

            // Generate Ref Code
            const refCode = "TB-" + Math.floor(100000 + Math.random() * 900000);

            // Populate confirmation view
            document.getElementById("booking-reference").innerText = refCode;
            document.getElementById("summary-passenger-name").innerText = nameInput.value.trim();
            document.getElementById("summary-route").innerText = document.getElementById("origin").value + " → " + document.getElementById("destination").value;
            document.getElementById("summary-dates").innerText = document.getElementById("departure-date").value + " to " + document.getElementById("return-date").value;
            document.getElementById("summary-base-fare").innerText = "$" + baseFare.toFixed(2);
            document.getElementById("summary-taxes").innerText = "$" + taxes.toFixed(2);
            document.getElementById("total-price").innerText = "$" + totalPrice.toFixed(2);

            // Toggle sections
            document.getElementById("search-section").classList.add("hidden");
            document.getElementById("search-results-section").classList.add("hidden");
            document.getElementById("passenger-form-section").classList.add("hidden");
            document.getElementById("booking-confirmation-section").classList.remove("hidden");
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def get_portal():
    """Serve the main travel booking web application page."""
    return HTML_CONTENT


@app.get("/health")
def health_check():
    """Health check endpoint for Pytest fixture initialization."""
    return {"status": "ok", "app": "travel_booking"}
