# Agent Instructions: Playwright Python Lab

This file provides workspace setup details, execution standards, and development workflows that apply across all tasks and subprojects (Phase 1 & Phase 2) in this repository. Read and adhere to these guidelines before starting any task.

---

## 1. Environment & Core Tooling Setup

This project uses `uv` for dependency management and environment isolation.

- **Python Version**: 3.10+
- **Core Dependencies**:
  - `pytest` - Test runner framework
  - `pytest-playwright` - Playwright browser automation plugin
  - `pytest-html` - HTML test execution report generator
- **Setup Checklist**:
  1. Initialize python setup with `uv init`.
  2. Add dependencies (`pytest`, `pytest-playwright`, `pytest-html`).
  3. Install Playwright browser runtimes:
     ```bash
     uv run playwright install
     ```
- **Verification Commands**:
  Verify the environment is correctly set up using:
  ```bash
  uv run pytest --version
  uv run playwright --version
  ```

---

## 2. Global Workspace Exclusions

Ensure that `.gitignore` is present at the root, ignoring:
- `.venv/`
- `__pycache__/`
- `artifacts/`
- `.pytest_cache/`
- `report.html`

---

## 3. Subproject Structure & Standards

Every subproject task (Projects 01 to 20) follows a standard pattern:

### Directory & File Naming
- Create a dedicated subdirectory for each project using the two-digit prefixed pattern (e.g., `01_open_verify/`, `11_role_based_portal/`, `20_ai_assisted_framework/`).
- Test files must be prefixed with `test_` (e.g., `test_open_verify.py`, `test_role_portal.py`) to be auto-discovered by `pytest`.

### Subproject Documentation
Every subproject directory must contain a dedicated `README.md` detailing:
- Project description and objectives.
- Solved test cases / scenarios covered.
- Command-line execution instructions.
- Key parameter references, fixtures, credentials, and test data design.

### Comprehensive Code Commenting
All Python code files must be thoroughly commented to explain:
- Purpose of fixtures (`page`, `browser`, `browser_context`, custom fixtures).
- Intent behind complex locators, route mocks, network calls, and page actions.
- Validation and assertion logic.

---

## 4. Test Execution & Verification

Tests should always be executed within the `uv` environment. Use the following standard invocation commands:

- **Run all tests in a subproject**:
  ```bash
  uv run pytest <project_folder>/
  ```
- **Run a specific test file or keyword pattern**:
  ```bash
  uv run pytest <project_folder>/<test_file>.py -k "test_keyword"
  ```
- **Run cross-browser test matrix**:
  ```bash
  uv run pytest <project_folder>/ --browser=all
  ```
- **Run visual regression tests (updating baseline snapshots)**:
  ```bash
  uv run pytest <project_folder>/ --update-snapshots
  ```
- **Run tagged tests with HTML report generation**:
  ```bash
  uv run pytest <project_folder>/ --html=report.html --self-contained-html -m <tag_name>
  ```

---

## 5. Troubleshooting & Known Environment Issues

### Terminal Sandbox Python Encodings Error (`ModuleNotFoundError: No module named 'encodings'`)
- **Issue**: Running `uv run pytest` inside the strict sandboxed terminal environment may cause Python execution to fail with `Fatal Python error: Failed to import encodings module / ModuleNotFoundError: No module named 'encodings'` due to restricted access to virtualenv standard library paths outside the workspace sandbox.
- **Resolution**: Execute commands with `BypassSandbox: true` (or unsandboxed mode) when invoking `uv run pytest` to grant the process proper filesystem permissions to locate standard Python library dependencies in `.venv`.
