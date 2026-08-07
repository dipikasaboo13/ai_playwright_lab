"""
Centralized Configuration Module for AI-Assisted Test Automation Framework.
Encapsulates environment variables, timeouts, default credentials, and path references.
"""

from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).parent.resolve()
ARTIFACTS_DIR = BASE_DIR / "artifacts"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
TRACES_DIR = ARTIFACTS_DIR / "traces"
DATA_DIR = BASE_DIR / "data"

# Test Execution Defaults
DEFAULT_TIMEOUT = 10000  # 10 seconds in milliseconds
NAVIGATION_TIMEOUT = 15000  # 15 seconds

# Credentials
VALID_CREDENTIALS = {
    "admin": "admin123",
    "john_doe": "password123",
    "qa_tester": "playwright2026"
}

INVALID_CREDENTIALS = {
    "invalid_user": "wrong_password",
    "admin": "badpass",
    "": ""
}

# Discount Codes
VALID_PROMO_CODES = {
    "AI20": 0.20,
    "HALFPRICE": 0.50,
    "SUPER100": 1.00
}
