"""
Root Pytest Configuration for ai_playwright_lab repository.

Ensures complete module cache isolation between subprojects during global test collection and execution.
Prevents namespace collisions for top-level subproject modules like `server`, `pages`, `utils`, and `config`.
"""

import sys
from pathlib import Path
import pytest


def _isolate_subproject_environment(test_path: Path):
    """
    Ensure the subproject root directory is at head of sys.path and evict any
    stale top-level subproject modules from sys.modules cache.
    """
    subproject_dir = test_path.parent
    if subproject_dir.name == "tests":
        subproject_dir = subproject_dir.parent

    dir_str = str(subproject_dir.resolve())

    # Ensure subproject root is at head of sys.path
    if not sys.path or sys.path[0] != dir_str:
        if dir_str in sys.path:
            sys.path.remove(dir_str)
        sys.path.insert(0, dir_str)

    # Evict stale subproject modules from Python import cache
    isolated_modules = ("server", "pages", "utils", "config")
    for mod_name in list(sys.modules.keys()):
        if mod_name in isolated_modules or any(mod_name.startswith(f"{m}.") for m in isolated_modules):
            mod = sys.modules.get(mod_name)
            if mod and hasattr(mod, "__file__") and mod.__file__:
                mod_file = str(Path(mod.__file__).resolve())
                if not mod_file.startswith(dir_str):
                    del sys.modules[mod_name]


@pytest.hookimpl(tryfirst=True)
def pytest_pycollect_makemodule(module_path, parent):
    """Collection hook: isolates module environment before test module import."""
    _isolate_subproject_environment(Path(module_path))


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Execution hook: isolates module environment before running each test item."""
    if hasattr(item, "path"):
        _isolate_subproject_environment(Path(item.path))
