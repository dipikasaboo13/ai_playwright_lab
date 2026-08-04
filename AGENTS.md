# Agent Instructions: Playwright Python Lab

This file provides workspace setup details, execution standards, and development workflows that apply across all tasks and subprojects in this repository. Read and adhere to these guidelines before starting any task.

---

## 1. Environment & Core Tooling Setup

This project uses `uv` for dependency management and environment isolation.

- **Python Version**: 3.10+
- **Core Dependencies**:
  - `pytest`
  - `pytest-playwright`
- **Setup Checklist**:
  1. Initialize python setup with `uv init`.
  2. Add dependencies (`pytest`, `pytest-playwright`).
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

Ensure that a `.gitignore` is present at the root, ignoring:
- `.venv/`
- `__pycache__/`
- `artifacts/`
- `.pytest_cache/`

---

## 3. Subproject Structure & Standards

Every subproject task follows a standard pattern:

### Directory & File Naming
- Create a dedicated subdirectory for each project using the two-digit prefixed pattern (e.g., `01_open_verify/`, `02_login_form/`).
- Test files must be prefixed with `test_` (e.g., `test_open_verify.py`, `test_login.py`) to be auto-discovered by `pytest`.

### Subproject Documentation
Every subproject directory must contain a `README.md` that details:
- Project description and objectives.
- Solved test cases / scenarios covered.
- Command-line execution instructions.
- Key parameter references and test data design.

---

## 4. Test Execution & Verification

Tests should always be executed within the `uv` environment. Use the following standard invocation commands:

- **Run all tests in a subproject**:
  ```bash
  uv run pytest <project_folder>/
  ```
- **Run a specific test file**:
  ```bash
  uv run pytest <project_folder>/<test_file>.py
  ```
- **Run specific test cases matching a pattern**:
  ```bash
  uv run pytest <project_folder>/<test_file>.py -k "test_keyword"
  ```
