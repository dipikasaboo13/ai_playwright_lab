"""
Global Pytest Configuration and Fixtures for Project 20.
Includes local FastAPI server lifecycle management, Playwright tracing,
failure screenshot/trace capture into artifacts/, and HTML report integration.
"""

import sys
import time
import socket
import subprocess
import requests
import pytest
from pathlib import Path

# Ensure project directory is in Python path for clean module imports
project_dir = Path(__file__).parent.resolve()
sys.path.insert(0, str(project_dir))

# Clear stale module cache entries (e.g. 'pages', 'utils', 'config') from other subprojects
for mod_name in list(sys.modules.keys()):
    if mod_name in ("pages", "utils", "config") or mod_name.startswith(("pages.", "utils.", "config.")):
        mod = sys.modules.get(mod_name)
        if mod and hasattr(mod, "__file__") and mod.__file__:
            if not str(Path(mod.__file__).resolve()).startswith(str(project_dir)):
                del sys.modules[mod_name]


from config import ARTIFACTS_DIR, SCREENSHOTS_DIR, TRACES_DIR


def get_free_port() -> int:
    """Find an available ephemeral TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def server_url():
    """
    Session fixture that launches the local FastAPI application server via uvicorn
    and yields the base server URL (e.g. http://127.0.0.1:<port>).
    """
    port = get_free_port()
    host = "127.0.0.1"
    base_url = f"http://{host}:{port}"

    # Launch server process
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "server:app",
            "--host", host,
            "--port", str(port),
            "--log-level", "warning"
        ],
        cwd=str(Path(__file__).parent.resolve())
    )

    # Wait for health check
    health_url = f"{base_url}/health"
    timeout = 10
    start_time = time.time()
    server_ready = False

    while time.time() - start_time < timeout:
        try:
            resp = requests.get(health_url)
            if resp.status_code == 200:
                server_ready = True
                break
        except Exception:
            time.sleep(0.2)

    if not server_ready:
        proc.kill()
        pytest.fail(f"FastAPI server failed to start at {base_url} within {timeout} seconds.")

    yield base_url

    # Teardown: terminate server
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()


@pytest.fixture(autouse=True)
def enable_tracing(context):
    """Autouse fixture to record Playwright execution traces for every test."""
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook executed on test completion.
    Captures screenshots and zip traces on failure and saves them in artifacts/.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page = item.funcargs.get("page", None)
        context = item.funcargs.get("context", None)
        ctx = context or (page.context if page else None)

        test_name = item.name.replace("[", "_").replace("]", "_").replace(" ", "_").replace("/", "_")

        if report.failed or hasattr(report, "wasxfail"):
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            TRACES_DIR.mkdir(parents=True, exist_ok=True)

            if page:
                screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
                try:
                    page.screenshot(path=str(screenshot_path))
                except Exception as e:
                    print(f"Failed to capture screenshot for {test_name}: {e}")

            if ctx:
                trace_path = TRACES_DIR / f"{test_name}.zip"
                try:
                    ctx.tracing.stop(path=str(trace_path))
                except Exception as e:
                    print(f"Failed to save trace for {test_name}: {e}")
        else:
            if ctx:
                try:
                    ctx.tracing.stop()
                except Exception:
                    pass
