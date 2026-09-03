import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_catalog_derived_files_are_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/generate_navigation.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_generated_lesson_navigation_stays_within_each_course() -> None:
    catalog = json.loads((ROOT / "docs/courses/_catalog.yml").read_text())
    navigation = json.loads((ROOT / "docs/assets/navigation.json").read_text())
    course_by_item = {
        item["id"]: course["id"]
        for course in catalog["courses"]
        for unit in course["units"]
        for item in [*unit["lessons"], *unit["challenges"]]
    }
    course_by_item.update(
        {
            assessment_id: course["id"]
            for course in catalog["courses"]
            for unit in course["units"]
            for assessment_id in unit.get("assessment_ids", [])
        }
    )

    for item_id, links in navigation["items"].items():
        for neighbor_id in (links["previous_id"], links["next_id"]):
            if neighbor_id is not None:
                assert course_by_item[item_id] == course_by_item[neighbor_id]


def test_generated_notebooks_are_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_notebooks.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_course_readiness_notebook_preserves_source_identity_and_questions() -> None:
    source = (
        ROOT / "docs/courses/advanced-algebra/units/orientation/"
        "readiness-diagnostic-and-repair.qmd"
    )
    notebook_path = (
        ROOT / "notebooks/courses/advanced-algebra/units/orientation/"
        "readiness-diagnostic-and-repair.ipynb"
    )
    notebook = json.loads(notebook_path.read_text())
    markdown = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )

    assert (
        notebook["metadata"]["fcmath"]["source_sha256"]
        == hashlib.sha256(source.read_bytes()).hexdigest()
    )
    assert "Evaluate $7-3(2-5)$." in markdown
    assert "<fc-quiz" not in markdown
    assert all(
        cell.get("execution_count") is None
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )


def test_topic_checkpoint_is_compiled_to_readable_notebook_practice() -> None:
    notebook_path = (
        ROOT / "notebooks/courses/advanced-algebra/units/algebra/"
        "expressions-and-equations.ipynb"
    )
    notebook = json.loads(notebook_path.read_text())
    markdown = "\n".join(
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "markdown"
    )

    metadata = notebook["metadata"]["fcmath"]
    assert metadata["generator_version"] == 4
    assert "source_revision" not in metadata
    assert "Select the expanded form." in markdown
    assert "Answer and explanation" in markdown
    assert "website-only controls are omitted" not in markdown


def test_every_generated_notebook_has_stable_cells_and_clean_python() -> None:
    notebooks = sorted((ROOT / "notebooks").rglob("*.ipynb"))
    catalog = json.loads((ROOT / "docs/courses/_catalog.yml").read_text())
    expected_count = sum(
        len(unit["lessons"]) + len(unit["challenges"])
        for course in catalog["courses"]
        for unit in course["units"]
    ) + len(catalog["assessments"])

    assert len(notebooks) == expected_count
    for path in notebooks:
        notebook = json.loads(path.read_text())
        cell_ids = [cell["id"] for cell in notebook["cells"]]
        assert len(cell_ids) == len(set(cell_ids))
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            assert cell["execution_count"] is None
            assert cell["outputs"] == []
            compile("".join(cell["source"]), f"{path}:cell-{index}", "exec")


def test_progress_script_uses_versioned_local_completion_only() -> None:
    script = (ROOT / "docs/assets/learning-ui.js").read_text()

    assert 'const STORAGE_KEY = "fcmath.progress.v1"' in script
    assert "schemaVersion" in script
    assert "CURRICULUM_MIGRATIONS" in script
    assert "migrateCurriculumState" in script
    assert "unit.assessment_ids" in script
    assert "localStorage" in script
    assert "rawAnswer" not in script
    assert "analytics" not in script.lower()
