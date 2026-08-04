# Project 7: File Upload and Download (`07_upload_download`)

## Description & Objectives
This subproject demonstrates automated testing of file upload and download operations using Playwright Python and `pytest`. It covers interacting with standard file input selectors (`<input type="file">`) and handling browser download events (`page.expect_download()`) to verify file persistence on disk.

## Solved Test Cases & Scenarios Covered
1. **File Upload (`test_upload`)**:
   - Navigates to `https://the-internet.herokuapp.com/upload`.
   - Attaches `test_upload.txt` to `#file-upload` via `page.set_input_files`.
   - Submits the form via `#file-submit`.
   - Asserts heading `<h3>File Uploaded!</h3>` is visible and `#uploaded-files` contains `test_upload.txt`.
2. **File Download (`test_download`)**:
   - Navigates to `https://the-internet.herokuapp.com/download`.
   - Listens for download event via `with page.expect_download() as download_info:`.
   - Triggers download by clicking a file link (`.example a`).
   - Saves the file using `download.save_as(...)` into Pytest `tmp_path`.
   - Asserts file exists on disk and has a file size greater than 0 bytes.

## Execution Instructions

Run all tests in this subproject:
```bash
uv run pytest 07_upload_download/
```

Run specific test scenarios:
```bash
uv run pytest 07_upload_download/test_files.py -k "test_upload"
uv run pytest 07_upload_download/test_files.py -k "test_download"
```

## Key Parameter References & Test Data Design
- **Upload Target**: `https://the-internet.herokuapp.com/upload`
  - Input Selector: `#file-upload`
  - Submit Button: `#file-submit`
  - Test Asset: `07_upload_download/test_upload.txt`
- **Download Target**: `https://the-internet.herokuapp.com/download`
  - Download Link Selector: `.example a`
  - Storage Location: Pytest fixture `tmp_path` (temporary execution directory)
