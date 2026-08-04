from pathlib import Path
from playwright.sync_api import Page, expect


def test_upload(page: Page) -> None:
    file_path = Path(__file__).parent / "test_upload.txt"
    assert file_path.exists(), f"Upload source file does not exist at {file_path}"

    page.goto("https://the-internet.herokuapp.com/upload")

    # Set the input file
    page.set_input_files("#file-upload", str(file_path))

    # Click the submit button
    page.click("#file-submit")

    # Verify upload confirmation elements
    expect(page.locator("h3")).to_have_text("File Uploaded!")
    expect(page.locator("#uploaded-files")).to_contain_text("test_upload.txt")


def test_download(page: Page, tmp_path: Path) -> None:
    page.goto("https://the-internet.herokuapp.com/download")

    # Expect download event when clicking a downloadable link
    with page.expect_download() as download_info:
        page.locator(".example a").first.click()

    download = download_info.value

    # Save the downloaded file to temporary path
    download_path = tmp_path / download.suggested_filename
    download.save_as(download_path)

    # Assert that file exists and is non-empty
    assert download_path.exists(), f"Downloaded file was not found at {download_path}"
    assert download_path.stat().st_size > 0, "Downloaded file size is 0 bytes"
