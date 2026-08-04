# Project 15: Multi-File Import and Error Report Validation (`15_file_import_reports`)

## Overview & Objectives

Project 15 demonstrates multi-file upload processing, row-level error breakdown table validation, and downloadable error report file parsing using Playwright Python.

### Key Objectives:
1. **Clean File Upload Verification**: Automate upload of valid CSV records, verifying processing success banners and counter metrics.
2. **Row-Level Error Table Validation**: Upload corrupted/malformed CSV dataset files and assert dynamic DOM rendering of row-by-row failure breakdown tables.
3. **File Download & Report Parsing**: Capture file download events via Playwright `page.expect_download()`, save report files to disk, and parse CSV contents to assert error strings per row.

---

## Solved Test Cases & Scenarios

| Test Case Name | Objective / Scenario Covered | Validation Method |
| :--- | :--- | :--- |
| `test_valid_import` | Upload `valid_records.csv` via file input and verify success summary banner and record counter. | Playwright `set_input_files("#file-upload-input", ...)` & `expect(page.locator("#import-success-summary")).to_be_visible()`. |
| `test_invalid_import_report` | Upload `invalid_records.csv`, verify error summary table, trigger file download, and parse error report CSV. | Playwright `page.expect_download()`, file saving, and Python `csv.DictReader` row assertions. |

---

## Technical Stack & Architecture

- **Web Server Framework**: FastAPI + Uvicorn (running on an ephemeral local TCP port).
- **Automation Engine**: Playwright Sync API (`Page`, `expect_download`, `expect`).
- **Test Data Formats**: Clean CSV (`valid_records.csv`) and Malformed CSV (`invalid_records.csv`).
- **Test Runner**: Pytest with module-scoped server fixtures.

---

## Command-Line Execution Instructions

Run all test execution commands using `uv` environment wrapper:

### 1. Run All Tests in Subproject
```bash
uv run pytest 15_file_import_reports/
```

### 2. Run Clean File Import Test
```bash
uv run pytest 15_file_import_reports/test_file_import.py -k "test_valid_import"
```

### 3. Run Corrupted File Import & Download Parsing Test
```bash
uv run pytest 15_file_import_reports/test_file_import.py -k "test_invalid_import_report"
```

### 4. Run with HTML Report Generation
```bash
uv run pytest 15_file_import_reports/ --html=report.html --self-contained-html
```

---

## Fixture & Parameter References

### Pytest Fixtures
- **`server_url`** (`module` scope):
  - Spawns the FastAPI application on an isolated background thread via Uvicorn on a free TCP port.
  - Polls `/health` endpoint until server responds HTTP 200 before test execution begins.
  - Gracefully shuts down Uvicorn server after all module tests complete.

### Key Element Locators & API Endpoints
- **UI Locators**:
  - File Input: `#file-upload-input`
  - Upload Button: `#btn-import-file`
  - Success Summary Banner: `#import-success-summary`
  - Success Counter Text: `#success-counter-text`
  - Error Summary Banner: `#import-error-summary`
  - Error Counter Text: `#error-counter-text`
  - Error Table: `#error-table`
  - Error Table Rows: `#error-table-body tr`
  - Download Report Button: `#btn-download-error-report`
- **Backend Endpoints**:
  - Web UI Portal: `GET /`
  - File Import API: `POST /api/v1/import`
  - Download Error Report API: `GET /api/v1/download-error-report`
  - Health Check: `GET /health`

---

## Test Data Design

### `valid_records.csv`
```csv
id,name,email,role,salary
EMP001,Alice Smith,alice@example.com,Developer,85000
EMP002,Bob Jones,bob@example.com,Designer,75000
EMP003,Charlie Brown,charlie@example.com,Manager,95000
```

### `invalid_records.csv`
```csv
id,name,email,role,salary
EMP001,Alice Smith,alice@example.com,Developer,85000
EMP001,Duplicate User,dup@example.com,Tester,60000
EMP005,Invalid Email,notanemail,Analyst,70000
,Missing ID,missingid@example.com,Developer,80000
EMP007,Negative Salary,salary@example.com,Developer,-50000
```
