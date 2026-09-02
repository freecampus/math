import json
from pathlib import Path

from fcmath.validation import validate_catalog

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "docs/courses/_catalog.yml"


def test_repository_catalog_is_structurally_valid() -> None:
    assert validate_catalog(CATALOG, docs_root=ROOT / "docs") == ()


def test_validator_reports_duplicate_ids_and_prerequisite_cycles(
    tmp_path: Path,
) -> None:
    catalog = json.loads(CATALOG.read_text())
    advanced = next(
        course for course in catalog["courses"] if course["id"] == "advanced-algebra"
    )
    linear = next(
        course for course in catalog["courses"] if course["id"] == "linear-algebra"
    )
    advanced["prerequisite_ids"] = ["linear-algebra"]
    linear["outcomes"][0]["id"] = advanced["outcomes"][0]["id"]
    path = tmp_path / "catalog.yml"
    path.write_text(json.dumps(catalog))

    issues = validate_catalog(path, docs_root=ROOT / "docs")
    messages = "\n".join(str(issue) for issue in issues)

    assert "cyclic prerequisites" in messages
    assert "duplicate ID" in messages


def test_validator_reports_metadata_disagreement(tmp_path: Path) -> None:
    catalog = json.loads(CATALOG.read_text())
    catalog["courses"][0]["units"][0]["lessons"][0]["status"] = "complete"
    path = tmp_path / "catalog.yml"
    path.write_text(json.dumps(catalog))

    issues = validate_catalog(path, docs_root=ROOT / "docs")

    assert any("QMD status disagrees" in issue.message for issue in issues)

    catalog = json.loads(CATALOG.read_text())
    catalog["courses"][0]["units"][0]["lessons"][0]["outcome_ids"] = [
        "advanced-algebra-outcome-5"
    ]
    path.write_text(json.dumps(catalog))
    issues = validate_catalog(path, docs_root=ROOT / "docs")

    assert any("QMD outcome_ids disagrees" in issue.message for issue in issues)


def test_complete_courses_cannot_hide_incomplete_units(tmp_path: Path) -> None:
    catalog = json.loads(CATALOG.read_text())
    catalog["courses"][0]["status"] = "complete"
    path = tmp_path / "catalog.yml"
    path.write_text(json.dumps(catalog))

    issues = validate_catalog(path, docs_root=ROOT / "docs")

    assert any(
        "complete course has incomplete units" in issue.message for issue in issues
    )
    assert any(
        "complete course has incomplete items" in issue.message for issue in issues
    )
