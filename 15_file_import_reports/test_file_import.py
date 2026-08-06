"""
Test suite for Project 15: Multi-File Import and Error Report Validation.
Validates clean file upload processing, row-level error breakdown table rendering,
and downloadable CSV error report parsing using Playwright.
"""

import csv
import socket
import time
import threading
import sys
from pathlib import Path
import urllib.request
import pytest
import uvicorn
from playwright.sync_api import Page, expect

# Ensure subproject directory is in sys.path to import local server module
sys.path.insert(0, str(Path(__file__).parent))
import server

SUBPROJECT_DIR = Path(__file__).parent


def get_free_port() -> int:
    """Utility function to discover an available local TCP port for the FastAPI web server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="module")
def server_url():
    """
    Module-scoped Pytest fixture to spin up the uvicorn FastAPI server on an ephemeral port.
    Polls the server's /health endpoint until active, and gracefully shuts it down after test completion.
    """
    port = get_free_port()
    config = uvicorn.Config(server.app, host="127.0.0.1", port=port, log_level="error")
    uv_server = uvicorn.Server(config)

    thread = threading.Thread(target=uv_server.run, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"

    # Poll /health endpoint to ensure web server is fully initialized before running tests
    start_time = time.time()
    while time.time() - start_time < 5.0:
        try:
            with urllib.request.urlopen(f"{url}/health") as resp:
                if resp.status == 200:
                    break
        except Exception:
            time.sleep(0.1)

    yield url

    uv_server.should_exit = True


def test_valid_import(page: Page, server_url: str):
    """
    Task 15.2: Clean File Import Verification Test Scenario
    - Objective: Upload valid file and assert successful processing banner.
    - Steps:
        1. Open file import portal page.
        2. Attach valid_records.csv to file input element (#file-upload-input).
        3. Click upload & process button (#btn-import-file).
        4. Assert success summary banner (#import-success-summary) is visible.
        5. Assert success counter text reflects total processed valid records ("3 records").
        6. Assert error summary banner (#import-error-summary) remains hidden.
    """
    # 1. Open web page
    page.goto(server_url)
    page.wait_for_load_state("domcontentloaded")

    # 2. Attach valid CSV file
    valid_csv_path = SUBPROJECT_DIR / "valid_records.csv"
    file_input = page.locator("#file-upload-input")
    expect(file_input).to_be_visible()
    file_input.set_input_files(str(valid_csv_path))

    # 3. Click upload & process button
    import_btn = page.locator("#btn-import-file")
    expect(import_btn).to_be_enabled()
    import_btn.click()

    # 4. Assert success summary banner is visible
    success_banner = page.locator("#import-success-summary")
    expect(success_banner).to_be_visible(timeout=5000)

    # 5. Assert success counter text
    counter_text = page.locator("#success-counter-text")
    expect(counter_text).to_contain_text("3 records")

    # 6. Assert error summary banner is hidden
    error_banner = page.locator("#import-error-summary")
    expect(error_banner).not_to_be_visible()


def test_invalid_import_report(page: Page, server_url: str, tmp_path: Path):
    """
    Task 15.3: Corrupted File Import & Downloadable Error Report Parsing
    - Objective: Upload invalid CSV, verify failure count, trigger report download, and parse downloaded error file.
    - Steps:
        1. Open file import portal page.
        2. Attach invalid_records.csv containing malformed rows and duplicate keys.
        3. Click upload & process button.
        4. Assert error summary banner (#import-error-summary) is visible.
        5. Assert error counter text indicates 4 failed records.
        6. Assert error breakdown table (#error-table) populates row-level error entries.
        7. Trigger report download via page.expect_download() on download button click.
        8. Save downloaded CSV file to disk.
        9. Parse saved file content to verify error message strings per row.
    """
    # 1. Open web page
    page.goto(server_url)
    page.wait_for_load_state("domcontentloaded")

    # 2. Attach invalid CSV file
    invalid_csv_path = SUBPROJECT_DIR / "invalid_records.csv"
    file_input = page.locator("#file-upload-input")
    expect(file_input).to_be_visible()
    file_input.set_input_files(str(invalid_csv_path))

    # 3. Click upload & process button
    import_btn = page.locator("#btn-import-file")
    import_btn.click()

    # 4. Assert error summary banner is visible
    error_banner = page.locator("#import-error-summary")
    expect(error_banner).to_be_visible(timeout=5000)

    # 5. Assert failure count (4 failed records out of 5)
    error_counter_text = page.locator("#error-counter-text")
    expect(error_counter_text).to_contain_text("Failed records: 4")

    # 6. Assert error breakdown table rows
    error_rows = page.locator("#error-table-body tr")
    expect(error_rows).to_have_count(4)

    # 7. Expect download event on clicking download button
    download_btn = page.locator("#btn-download-error-report")
    expect(download_btn).to_be_visible()

    with page.expect_download() as download_info:
        download_btn.click()

    download = download_info.value

    # 8. Save downloaded file to temporary path
    save_path = tmp_path / "downloaded_error_report.csv"
    download.save_as(str(save_path))
    assert save_path.exists(), "Downloaded error report file was not saved to disk"

    # 9. Parse saved file content to verify row-by-row error details
    with open(save_path, mode="r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == 4, f"Expected 4 error rows in downloaded report, got {len(reader)}"

    # Row 3 (Duplicate ID)
    assert reader[0]["row"] == "3"
    assert reader[0]["employee_id"] == "EMP001"
    assert "Duplicate employee ID 'EMP001'" in reader[0]["error_message"]

    # Row 4 (Invalid Email)
    assert reader[1]["row"] == "4"
    assert reader[1]["employee_id"] == "EMP005"
    assert "Invalid email address format 'notanemail'" in reader[1]["error_message"]

    # Row 5 (Missing ID)
    assert reader[2]["row"] == "5"
    assert reader[2]["employee_id"] == ""
    assert "Missing required employee ID" in reader[2]["error_message"]

    # Row 6 (Negative Salary)
    assert reader[3]["row"] == "6"
    assert reader[3]["employee_id"] == "EMP007"
    assert "Salary must be a positive integer" in reader[3]["error_message"]
