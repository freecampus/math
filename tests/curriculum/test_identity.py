import re
from pathlib import Path

import fcmath

ROOT = Path(__file__).resolve().parents[2]


def test_renamed_identity_is_consistent() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text()
    quarto = (ROOT / "docs/_quarto.yml").read_text()

    assert 'name = "freecampus-math"' in pyproject
    assert 'include = "fcmath"' in pyproject
    assert "https://github.com/freecampus/math" in quarto
    version_match = re.search(
        r'(?m)^version = "(?P<version>[^"]+)"\s+# semantic-release$', pyproject
    )
    assert version_match is not None
    assert fcmath.__version__ == version_match.group("version")


def test_old_import_package_is_absent() -> None:
    assert not (ROOT / "src/edumath").exists()


def test_public_material_has_no_institution_or_admission_identity() -> None:
    paths = [ROOT / "README.md", ROOT / "CITATION.cff", ROOT / "pyproject.toml"]
    paths.extend((ROOT / "docs").rglob("*.qmd"))
    public_text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    for forbidden in (
        "Harvard",
        "MIT OpenCourseWare",
        "MScFE",
        "admission test",
        "eligibility for admission",
    ):
        assert forbidden.casefold() not in public_text.casefold()
