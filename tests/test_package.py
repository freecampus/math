import re
from pathlib import Path

import edumath


def test_package_exposes_version() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    match = re.search(r'^version = "([^"]+)"', pyproject.read_text(), re.MULTILINE)

    assert match is not None
    assert edumath.__version__ == match.group(1)
