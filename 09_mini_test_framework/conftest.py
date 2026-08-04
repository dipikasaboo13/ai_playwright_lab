import sys
import pytest
from pathlib import Path

# Ensure 09_mini_test_framework folder is in python path
sys.path.insert(0, str(Path(__file__).parent))

@pytest.fixture(autouse=True)
def enable_tracing(context):
    """Autouse fixture to start Playwright tracing for every test."""
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture screenshot and trace zip on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = item.funcargs.get("page", None)
        context = item.funcargs.get("context", None)
        ctx = context or (page.context if page else None)

        artifacts_dir = Path(__file__).parent / "artifacts"
        screenshots_dir = artifacts_dir / "screenshots"
        traces_dir = artifacts_dir / "traces"

        test_name = item.name.replace("[", "_").replace("]", "_").replace(" ", "_")

        if report.failed or hasattr(report, "wasxfail"):
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            traces_dir.mkdir(parents=True, exist_ok=True)

            if page:
                screenshot_path = screenshots_dir / f"{test_name}.png"
                try:
                    page.screenshot(path=str(screenshot_path))
                except Exception as e:
                    print(f"Failed to capture screenshot: {e}")

            if ctx:
                trace_path = traces_dir / f"{test_name}.zip"
                try:
                    ctx.tracing.stop(path=str(trace_path))
                except Exception as e:
                    print(f"Failed to save trace: {e}")
        else:
            if ctx:
                try:
                    ctx.tracing.stop()
                except Exception:
                    pass
