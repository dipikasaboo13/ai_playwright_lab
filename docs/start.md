Learn Playwright through small, practical “vibe coding” projects: describe the outcome in plain English, let AI draft the code, then review, run, debug, and improve it yourself.

1. **Open and verify a webpage**

   * Open Google or a sample site, verify title and visible text.
   * Learn: setup, `page.goto`, locators, assertions.

2. **Login form automation**

   * Automate login on a demo application with valid and invalid credentials.
   * Learn: input fields, buttons, positive/negative scenarios.

3. **Search and filter products**

   * Search for an item on a demo e-commerce site and apply a category/price filter.
   * Learn: dropdowns, checkboxes, dynamic results.

4. **Add product to cart**

   * Add an item, update quantity, remove it, and validate cart totals.
   * Learn: reusable steps, numeric assertions, UI state validation.

5. **Data-driven login tests**

   * Read multiple login test cases from a JSON or CSV file.
   * Learn: test data separation, loops/parameterized tests, cleaner test design.

6. **API + UI validation**

   * Call a public/demo API, validate its response, then verify matching information in the UI.
   * Learn: API testing with Playwright, response assertions, end-to-end validation.

7. **File upload and download**

   * Upload a document, validate success, then download a generated file.
   * Learn: file chooser handling, download validation, test fixtures.

8. **Multi-user approval workflow**

   * User A creates a request; User B logs in and approves it.
   * Learn: separate browser contexts, role-based flows, business-process testing.

9. **Build a mini test framework**

   * Organize tests using Page Object Model for login, dashboard, and profile modules.
   * Add screenshots/traces on failure.
   * Learn: maintainable structure, fixtures, reporting, debugging.

10. **Payment checkout simulation**

* Test a demo checkout journey: browse product → add to cart → address → payment form → order confirmation.
* Include invalid card, missing address, and successful order scenarios.
* Learn: realistic end-to-end flow, validations, test coverage, reusable page objects.

For each project, use this vibe-coding cycle:

1. Write the requirement in simple English.
2. Ask AI to generate the first Playwright test.
3. Run it and understand every failing line.
4. Ask AI to fix only the specific failure.
5. Refactor the final version yourself into clean reusable code.

