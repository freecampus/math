import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COVERAGE = ROOT / "docs/courses/advanced-algebra/_coverage.yml"
CHAPTER_ID = "advanced-algebra-chapter-1-4-proof-methods-algebra"
SCRIPT = ROOT / "scripts/scaffold_chapter.py"


def test_scaffold_uses_coverage_metadata_and_contract_sections(tmp_path: Path) -> None:
    output = tmp_path / "proof-methods.qmd"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            CHAPTER_ID,
            str(output),
            "--coverage",
            str(COVERAGE),
            "--lesson-id",
            "advanced-algebra-mathematical-language-proof-methods",
            "--estimated-minutes",
            "600",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    scaffold = output.read_text()

    assert result.returncode == 0, result.stderr
    assert 'title: "Proof methods for algebra"' in scaffold
    assert "unit_id: mathematical-language" in scaffold
    assert "status: draft" in scaffold
    assert 'estimated_time: "600 minutes"' in scaffold
    assert 'data-problem-id="aa-1-4-checkpoint-01"' in scaffold
    assert "## 5. Examination strategy clinic" in scaffold
    assert scaffold.rstrip().endswith("```")
    assert scaffold.rfind(
        "## Using this lesson with fcmath and SymPy"
    ) > scaffold.rfind("## References and further study")


def test_scaffold_writer_refuses_to_overwrite_by_default(tmp_path: Path) -> None:
    output = tmp_path / "proof-methods.qmd"
    command = [
        sys.executable,
        str(SCRIPT),
        CHAPTER_ID,
        str(output),
        "--coverage",
        str(COVERAGE),
        "--lesson-id",
        "advanced-algebra-mathematical-language-proof-methods",
    ]

    first = subprocess.run(command, capture_output=True, text=True, check=False)
    second = subprocess.run(command, capture_output=True, text=True, check=False)

    assert first.returncode == 0, first.stderr
    assert second.returncode != 0
    assert "refusing to overwrite" in second.stderr
