"""
FastAPI application for Project 17: Responsive Cross-Browser Regression Suite.
Provides a responsive E-Commerce application with desktop and mobile layouts,
collapsible hamburger menu drawer, responsive product grid, cart drawer,
and modal checkout flow.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Responsive E-Commerce Application")


@app.get("/health")
def health_check():
    """Health check endpoint to verify server readiness during test fixture initialization."""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    """Renders the main responsive web portal page with media query breakpoints and interactive JS."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechMart Responsive E-Commerce Portal</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --text-light: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #10b981;
            --border: #334155;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Top Header & Navigation */
        header {
            background-color: #1e293b;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.5rem;
        }

        .brand {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Desktop Navigation Links */
        .desktop-nav {
            display: flex;
            align-items: center;
            gap: 2rem;
        }

        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
            cursor: pointer;
        }

        .nav-link:hover, .nav-link.active {
            color: var(--text-light);
        }

        .cart-badge {
            background-color: var(--primary);
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        /* Hamburger Toggle Button (Mobile/Tablet) */
        .hamburger-btn {
            display: none;
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-light);
            font-size: 1.5rem;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
        }

        /* Mobile Drawer Navigation */
        .mobile-menu {
            display: none;
            background-color: #1e293b;
            border-bottom: 1px solid var(--border);
            padding: 1rem 1.5rem;
            flex-direction: column;
            gap: 1rem;
        }

        .mobile-menu.expanded {
            display: flex !important;
        }

        .mobile-menu .nav-link {
            padding: 0.5rem 0;
            border-bottom: 1px solid #334155;
        }

        /* Media Queries for Viewport Breakpoints */
        @media (max-width: 768px) {
            .desktop-nav {
                display: none !important;
            }
            .hamburger-btn {
                display: flex !important;
                align-items: center;
                justify-content: center;
            }
        }

        /* Page Layout & Container */
        main {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1.5rem;
            flex: 1;
            width: 100%;
        }

        .hero-banner {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
        }

        .hero-banner h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        /* Responsive Product Grid */
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .product-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }

        .product-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .product-desc {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }

        .product-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 1rem;
        }

        .product-price {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--accent);
        }

        .btn-add-cart {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .btn-add-cart:hover {
            background-color: var(--primary-dark);
        }

        /* Cart Side Drawer */
        .cart-drawer {
            position: fixed;
            top: 0;
            right: -400px;
            width: 380px;
            max-width: 100%;
            height: 100%;
            background-color: #1e293b;
            box-shadow: -5px 0 25px rgba(0,0,0,0.5);
            z-index: 200;
            transition: right 0.3s ease-in-out;
            padding: 2rem 1.5rem;
            display: flex;
            flex-direction: column;
        }

        .cart-drawer.open {
            right: 0;
        }

        .cart-drawer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
        }

        .btn-close-drawer {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
        }

        .cart-items-list {
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .cart-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #0f172a;
            padding: 0.75rem 1rem;
            border-radius: 6px;
        }

        .cart-footer {
            border-top: 1px solid var(--border);
            padding-top: 1rem;
            margin-top: 1rem;
        }

        .cart-total-row {
            display: flex;
            justify-content: space-between;
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .btn-checkout {
            width: 100%;
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 0.8rem;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
        }

        /* Modal Overlay & Dialog */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            z-index: 300;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }

        .modal-overlay.active {
            display: flex;
        }

        .modal-card {
            background-color: #1e293b;
            border: 1px solid var(--border);
            border-radius: 12px;
            width: 100%;
            max-width: 480px;
            padding: 2rem;
        }

        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .form-input {
            width: 100%;
            padding: 0.75rem;
            background-color: #0f172a;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: white;
            font-size: 1rem;
        }

        /* Order Confirmation Box */
        .order-confirmation {
            display: none;
            background-color: #064e3b;
            border: 1px solid #10b981;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            text-align: center;
        }

        .order-confirmation.active {
            display: block;
        }

        footer {
            text-align: center;
            padding: 1.5rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border);
            margin-top: auto;
        }
    </style>
</head>
<body>

    <!-- Header Section -->
    <header>
        <div class="nav-container">
            <div class="brand">
                <span>⚡ TechMart</span>
            </div>

            <!-- Desktop Navigation -->
            <nav class="desktop-nav" id="desktop-nav">
                <a class="nav-link active" id="nav-home">Home</a>
                <a class="nav-link" id="nav-products">Products</a>
                <a class="nav-link" id="nav-account">Account</a>
                <a class="nav-link" id="nav-cart-btn" onclick="toggleCartDrawer(true)">
                    🛒 Cart <span class="cart-badge" id="cart-count">0</span>
                </a>
            </nav>

            <!-- Hamburger Button for Mobile / Tablet -->
            <button class="hamburger-btn" id="hamburger-btn" aria-label="Toggle navigation" onclick="toggleMobileMenu()">
                ☰
            </button>
        </div>

        <!-- Collapsible Mobile Menu Drawer -->
        <div class="mobile-menu" id="mobile-menu">
            <a class="nav-link" id="mobile-nav-home" onclick="toggleMobileMenu()">Home</a>
            <a class="nav-link" id="mobile-nav-products" onclick="toggleMobileMenu()">Products</a>
            <a class="nav-link" id="mobile-nav-account" onclick="toggleMobileMenu()">Account</a>
            <a class="nav-link" id="mobile-nav-cart" onclick="toggleMobileMenu(); toggleCartDrawer(true);">
                🛒 View Cart (<span id="mobile-cart-count">0</span> items)
            </a>
        </div>
    </header>

    <!-- Main Content Body -->
    <main>
        <section class="hero-banner">
            <h1>Next-Gen Tech Essentials</h1>
            <p>Tested for Desktop, Tablet, and Mobile Viewports</p>
        </section>

        <!-- Product Grid -->
        <section class="products-grid" id="product-grid">
            <div class="product-card" id="card-prod-1">
                <div>
                    <h3 class="product-title">Noise-Canceling Headphones</h3>
                    <p class="product-desc">Wireless over-ear headphones with premium acoustics.</p>
                </div>
                <div class="product-footer">
                    <span class="product-price">$299.00</span>
                    <button class="btn-add-cart" id="btn-add-prod-1" onclick="addToCart('Noise-Canceling Headphones', 299.00)">Add to Cart</button>
                </div>
            </div>

            <div class="product-card" id="card-prod-2">
                <div>
                    <h3 class="product-title">Ultra-Wide Gaming Monitor</h3>
                    <p class="product-desc">34-inch curved display with 144Hz refresh rate.</p>
                </div>
                <div class="product-footer">
                    <span class="product-price">$599.00</span>
                    <button class="btn-add-cart" id="btn-add-prod-2" onclick="addToCart('Ultra-Wide Gaming Monitor', 599.00)">Add to Cart</button>
                </div>
            </div>

            <div class="product-card" id="card-prod-3">
                <div>
                    <h3 class="product-title">Mechanical RGB Keyboard</h3>
                    <p class="product-desc">Tactile switches with customizable backlighting.</p>
                </div>
                <div class="product-footer">
                    <span class="product-price">$149.00</span>
                    <button class="btn-add-cart" id="btn-add-prod-3" onclick="addToCart('Mechanical RGB Keyboard', 149.00)">Add to Cart</button>
                </div>
            </div>
        </section>

        <!-- Order Confirmation Container -->
        <div class="order-confirmation" id="order-confirmation">
            <h2>🎉 Order Confirmed!</h2>
            <p style="margin-top: 0.5rem;">Reference Code: <strong id="order-ref-code">REF-00000</strong></p>
            <p style="margin-top: 0.25rem;">Total Charged: <strong id="order-total-price">$0.00</strong></p>
        </div>
    </main>

    <!-- Cart Drawer -->
    <div class="cart-drawer" id="cart-drawer">
        <div class="cart-drawer-header">
            <h2>Your Shopping Cart</h2>
            <button class="btn-close-drawer" id="btn-close-cart" onclick="toggleCartDrawer(false)">✕</button>
        </div>

        <div class="cart-items-list" id="cart-items-list">
            <p id="cart-empty-msg" style="color: var(--text-muted);">Your cart is currently empty.</p>
        </div>

        <div class="cart-footer">
            <div class="cart-total-row">
                <span>Total:</span>
                <span id="cart-total">$0.00</span>
            </div>
            <button class="btn-checkout" id="btn-checkout" onclick="openCheckoutModal()">Proceed to Checkout</button>
        </div>
    </div>

    <!-- Checkout Modal -->
    <div class="modal-overlay" id="checkout-modal">
        <div class="modal-card">
            <h2 style="margin-bottom: 1.5rem;">Complete Your Order</h2>
            <form id="checkout-form" onsubmit="handleCheckoutSubmit(event)">
                <div class="form-group">
                    <label for="input-name">Full Name</label>
                    <input type="text" id="input-name" class="form-input" required value="Alex Mercer">
                </div>

                <div class="form-group">
                    <label for="input-email">Email Address</label>
                    <input type="email" id="input-email" class="form-input" required value="alex.mercer@example.com">
                </div>

                <div class="form-group">
                    <label for="input-address">Shipping Address</label>
                    <input type="text" id="input-address" class="form-input" required value="100 Tech Parkway, Suite 400">
                </div>

                <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                    <button type="button" class="btn-add-cart" style="background-color: var(--border);" onclick="closeCheckoutModal()">Cancel</button>
                    <button type="submit" class="btn-checkout" id="btn-submit-order">Confirm & Pay</button>
                </div>
            </form>
        </div>
    </div>

    <footer>
        <p>&copy; 2026 TechMart Lab Portal. Responsive & Cross-Browser Validated.</p>
    </footer>

    <!-- Client-side Logic -->
    <script>
        let cart = [];

        function toggleMobileMenu() {
            const menu = document.getElementById('mobile-menu');
            menu.classList.toggle('expanded');
        }

        function toggleCartDrawer(open) {
            const drawer = document.getElementById('cart-drawer');
            if (open) {
                drawer.classList.add('open');
            } else {
                drawer.classList.remove('open');
            }
        }

        function addToCart(title, price) {
            cart.push({ title, price });
            updateCartUI();
            toggleCartDrawer(true);
        }

        function updateCartUI() {
            const countElem = document.getElementById('cart-count');
            const mobileCountElem = document.getElementById('mobile-cart-count');
            const itemsList = document.getElementById('cart-items-list');
            const totalElem = document.getElementById('cart-total');

            countElem.innerText = cart.length;
            mobileCountElem.innerText = cart.length;

            if (cart.length === 0) {
                itemsList.innerHTML = '<p id="cart-empty-msg" style="color: var(--text-muted);">Your cart is currently empty.</p>';
                totalElem.innerText = '$0.00';
                return;
            }

            let html = '';
            let total = 0;

            cart.forEach((item, index) => {
                total += item.price;
                html += `
                    <div class="cart-item">
                        <span>${item.title}</span>
                        <strong>$${item.price.toFixed(2)}</strong>
                    </div>
                `;
            });

            itemsList.innerHTML = html;
            totalElem.innerText = `$${total.toFixed(2)}`;
        }

        function openCheckoutModal() {
            if (cart.length === 0) {
                alert('Please add items to cart before checking out.');
                return;
            }
            toggleCartDrawer(false);
            document.getElementById('checkout-modal').classList.add('active');
        }

        function closeCheckoutModal() {
            document.getElementById('checkout-modal').classList.remove('active');
        }

        function handleCheckoutSubmit(event) {
            event.preventDefault();
            closeCheckoutModal();

            const refCode = 'REF-' + Math.floor(10000 + Math.random() * 90000);
            let total = cart.reduce((sum, item) => sum + item.price, 0);

            document.getElementById('order-ref-code').innerText = refCode;
            document.getElementById('order-total-price').innerText = `$${total.toFixed(2)}`;
            
            const confirmBox = document.getElementById('order-confirmation');
            confirmBox.classList.add('active');
            confirmBox.scrollIntoView({ behavior: 'smooth' });

            // Reset cart
            cart = [];
            updateCartUI();
        }
    </script>
</body>
</html>
"""
