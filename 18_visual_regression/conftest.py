"""
Pytest configuration for Project 18: Visual Regression Testing.
Registers custom command-line option `--update-snapshots` and patches Playwright's PageAssertions
with `to_have_screenshot()` method supporting dynamic element locators masking and baseline comparison.
"""

import io
from pathlib import Path
import pytest
from PIL import Image, ImageChops
from playwright.sync_api import Page, PageAssertions

SUBPROJECT_DIR = Path(__file__).parent
SNAPSHOTS_DIR = SUBPROJECT_DIR / "snapshots"

# Flag tracking --update-snapshots command-line option state
UPDATE_SNAPSHOTS = False


def pytest_addoption(parser):
    """Register custom CLI options for visual regression snapshot management."""
    parser.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Update visual regression reference baseline snapshots in snapshots/ directory.",
    )


def pytest_configure(config):
    """Capture pytest configuration state upon initialization."""
    global UPDATE_SNAPSHOTS
    UPDATE_SNAPSHOTS = config.getoption("--update-snapshots", default=False)


def custom_to_have_screenshot(self, name: str, mask=None, threshold: float = 0.2, timeout: float = 5000):
    """
    Custom PageAssertions implementation for to_have_screenshot().
    
    Captures page screenshot applying locator element masks, creates reference baseline
    snapshots when `--update-snapshots` is supplied (or when baseline file is absent),
    and performs PIL image diff comparison against saved PNG files in `snapshots/`.
    """
    impl_page = getattr(self._impl_obj, "_actual_page", None)
    if not impl_page:
        raise RuntimeError("Unable to extract Playwright Page instance from PageAssertions.")
    
    # Wrap implementation Page object into sync Page interface
    page = Page(impl_page)

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_path = SNAPSHOTS_DIR / name

    # Capture page screenshot with Playwright element masking
    current_png = page.screenshot(mask=mask if mask else None)

    # 1. Update snapshot baseline if flag enabled or reference file missing
    if UPDATE_SNAPSHOTS or not snapshot_path.exists():
        snapshot_path.write_bytes(current_png)
        return

    # 2. Read existing reference baseline PNG
    baseline_png = snapshot_path.read_bytes()
    img_baseline = Image.open(io.BytesIO(baseline_png)).convert("RGB")
    img_current = Image.open(io.BytesIO(current_png)).convert("RGB")

    # 3. Assert image dimensions match
    if img_baseline.size != img_current.size:
        raise AssertionError(
            f"Visual regression failed for '{name}': Image dimensions mismatch. "
            f"Baseline size: {img_baseline.size}, Current size: {img_current.size}."
        )

    # 4. Perform pixel-by-pixel comparison with color noise tolerance
    diff_img = ImageChops.difference(img_baseline, img_current)
    total_pixels = img_baseline.width * img_baseline.height
    diff_pixels = 0

    bytes_b = list(img_baseline.tobytes())
    bytes_c = list(img_current.tobytes())
    for i in range(0, len(bytes_b), 3):
        if abs(bytes_b[i] - bytes_c[i]) > 5 or abs(bytes_b[i+1] - bytes_c[i+1]) > 5 or abs(bytes_b[i+2] - bytes_c[i+2]) > 5:
            diff_pixels += 1

    diff_ratio = diff_pixels / total_pixels

    # 5. Assert difference ratio remains within configured threshold tolerance
    if diff_ratio > threshold:
        diff_path = SNAPSHOTS_DIR / f"diff_{name}"
        diff_img.save(diff_path)
        raise AssertionError(
            f"Visual regression drift detected for '{name}'! "
            f"Pixel diff ratio {diff_ratio:.2%} exceeds threshold ({threshold:.2%}). "
            f"Diff visual artifact saved to {diff_path}."
        )


# Inject to_have_screenshot method into Playwright PageAssertions class
PageAssertions.to_have_screenshot = custom_to_have_screenshot
