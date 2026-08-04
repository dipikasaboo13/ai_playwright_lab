11. **Role-Based Employee Management Portal**

* Admin creates an employee, assigns a role, and disables the account.
* Employee logs in and verifies which menus/actions are available.
* Learn: role-based access, multiple browser contexts, permission assertions.

12. **End-to-End Travel Booking Flow**

* Search flights/hotels, apply filters, select dates, add traveller details, and confirm a mock booking.
* Include validation for unavailable dates, missing traveller details, and price changes.
* Learn: calendars, dynamic pricing, complex forms, stable locators.

13. **Order Management with API Setup**

* Create customer/order data through APIs before the test.
* Log into the UI, search for the order, update status, and verify the update through an API.
* Learn: API-based test-data setup, UI/API cross-validation, cleanup.

14. **Webhook and Notification Validation**

* Trigger an action in the UI, such as placing an order or submitting a request.
* Validate that a webhook/event was sent and the correct notification appears in the application.
* Learn: async events, polling/retries, network interception, event validation.

15. **Multi-File Import and Error Report Validation**

* Upload valid and invalid CSV/Excel files.
* Verify imported records, row-level failures, downloadable error reports, and duplicate-file handling.
* Learn: advanced file handling, data validation, download parsing.

16. **Mock External Dependency Failures**

* Test a checkout, banking, or order flow while mocking payment/API failures:
  timeout, 500 error, partial success, invalid response, and slow response.
* Learn: `page.route()`, API mocking, resilience and error-message testing.

17. **Responsive Cross-Browser Regression Suite**

* Run the same critical user flows across Chromium, Firefox, WebKit, mobile viewport, and tablet viewport.
* Capture screenshots for failed tests.
* Learn: Playwright projects, device emulation, cross-browser issues, visual debugging.

18. **Visual Regression Testing for Key Screens**

* Create screenshot baselines for login, dashboard, product page, cart, and confirmation page.
* Detect unexpected UI changes while masking dynamic data such as timestamps.
* Learn: `toHaveScreenshot()`, masking, baseline management, visual quality checks.

19. **Payment Transaction Lifecycle Simulation**

* Simulate a payment journey: initiate payment → authorization → pending state → success/failure → refund.
* Validate UI status, API response, transaction history, and user notifications at every stage.
* Learn: state-transition testing, API/UI consistency, financial workflow coverage.

20. **AI-Assisted Test Automation Framework**

* Build a medium-advanced Playwright framework for a demo application with:

  * Page Object Model
  * API test-data setup and cleanup
  * environment configuration
  * reusable fixtures
  * test tagging (`smoke`, `regression`, `payments`)
  * screenshots, traces, and HTML reports
  * AI-generated test-data variations for positive, negative, boundary, and exception scenarios
* Learn: framework architecture, scalable test design, CI-ready automation, and AI-enabled testing workflows.
