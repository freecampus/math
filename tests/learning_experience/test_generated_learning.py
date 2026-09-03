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


def test_generated_notebooks_are_current() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_notebooks.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_diagnostic_notebook_preserves_source_identity_and_questions() -> None:
    source = ROOT / "docs/pathways/quantitative-mathematics/diagnostic.qmd"
    notebook_path = (
        ROOT / "notebooks/pathways/quantitative-mathematics/diagnostic.ipynb"
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
    assert "What does `sum(i*i for i in range(4))` return?" in markdown
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

    assert len(notebooks) == 67
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
    assert "localStorage" in script
    assert "rawAnswer" not in script
    assert "analytics" not in script.lower()
