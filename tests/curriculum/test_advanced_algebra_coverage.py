import json
import re
from pathlib import Path

from fcmath.quizzes import load_quiz
from fcmath.validation import (
    load_structured_data,
    validate_coverage_matrix,
    validate_external_resources,
)

ROOT = Path(__file__).resolve().parents[2]
COVERAGE = ROOT / "docs/courses/advanced-algebra/_coverage.yml"
CATALOG = ROOT / "docs/courses/_catalog.yml"
EXTERNAL_RESOURCES = ROOT / "docs/courses/advanced-algebra/_external-resources.yml"


def test_advanced_algebra_coverage_matrix_is_complete_and_valid() -> None:
    matrix = load_structured_data(COVERAGE)

    assert validate_coverage_matrix(COVERAGE, CATALOG) == ()
    assert matrix["chapter_count"] == 49
    assert [unit["book_unit"] for unit in matrix["units"]] == list(range(11))
    assert set(matrix["problem_level_policy"]) == {"A", "B", "C", "D"}
    assert set(matrix["chapter_status_policy"]) == {
        "planned",
        "draft",
        "review",
        "active",
        "complete",
    }
    assert "route_compatibility" not in matrix


def test_coverage_validator_detects_published_and_prerequisite_drift(
    tmp_path: Path,
) -> None:
    matrix = load_structured_data(COVERAGE)
    first = matrix["units"][0]["chapters"][0]
    first["source_file"] = "courses/advanced-algebra/missing.qmd"
    second = matrix["units"][0]["chapters"][1]
    second["prerequisite_chapter_ids"] = [matrix["units"][1]["chapters"][0]["id"]]
    path = tmp_path / "coverage.yml"
    path.write_text(json.dumps(matrix))

    messages = "\n".join(
        str(issue) for issue in validate_coverage_matrix(path, CATALOG)
    )

    assert "source_file disagrees with catalog" in messages
    assert "must refer to an earlier chapter" in messages


def test_reference_chapters_meet_book_scale_structure() -> None:
    matrix = load_structured_data(COVERAGE)
    exemplars = [
        chapter
        for unit in matrix["units"]
        for chapter in unit["chapters"]
        if chapter["reference_exemplar"]
    ]
    required_headings = (
        "Why this matters",
        "Five-minute retrieval warm-up",
        "Common mistakes",
        "Examination strategy clinic",
        "Exercises by purpose and difficulty",
        "Cumulative retrieval",
        "Topic checkpoint",
        "Summary and next step",
        "References and further study",
        "Using this lesson with fcmath and SymPy",
    )
    all_problem_ids: list[str] = []

    assert len(exemplars) == 4
    for chapter in exemplars:
        source = ROOT / "docs" / chapter["source_file"]
        text = source.read_text()
        words = re.findall(r"\b[\w-]+\b", text)
        headings = re.findall(r"(?m)^## (?:\d+\.\s+)?(.+?)\s*$", text)
        problem_ids = re.findall(r'data-problem-id="([a-z0-9-]+)"', text)

        assert len(words) >= 3_000, source
        assert all(
            any(heading.startswith(required) for heading in headings)
            for required in required_headings
        ), source
        assert headings[-1] == "Using this lesson with fcmath and SymPy", source
        assert text.count("{.worked-example") >= 8, source
        assert set(re.findall(r'data-level="([A-D])"', text)) == {"A", "B", "C", "D"}
        assert "<fc-quiz" in text
        assert problem_ids
        assert len(problem_ids) == len(set(problem_ids))
        all_problem_ids.extend(problem_ids)

        for chunk in re.findall(r"```\{python\}(.*?)```", text, re.DOTALL):
            if ".plot(" in chunk or ".render(" in chunk:
                assert "#| fig-alt:" in chunk, source

    assert len(all_problem_ids) == len(set(all_problem_ids))


def test_reference_chapter_quizzes_are_valid() -> None:
    quiz_root = ROOT / "docs/quizzes/advanced-algebra"
    expected = {
        "argument-language.yml": (8, "active"),
        "readiness-diagnostic.yml": (24, "active"),
        "sets-logic.yml": (10, "active"),
        "number-systems.yml": (10, "review"),
    }

    for name, (expected_count, expected_status) in expected.items():
        bank = load_quiz(quiz_root / name)
        assert bank.status == expected_status
        assert len(bank.questions) == expected_count


def test_problem_metadata_schema_and_template_cover_all_levels() -> None:
    schema = json.loads(
        (
            ROOT / "docs/courses/advanced-algebra/problem-metadata.schema.json"
        ).read_text()
    )
    template = load_structured_data(ROOT / "docs/_templates/problem-bank.yml")

    level_property = schema["properties"]["level"]
    assert set(level_property["enum"]) == {"A", "B", "C", "D"}
    assert schema["additionalProperties"] is False
    assert template["problems"][0]["level"] == "A"
    assert template["problems"][0]["verification"]["method"]
    assert {
        "source_kind",
        "source_note",
        "calculator_policy",
        "hint_policy",
        "solution_location",
        "review_status",
    }.issubset(schema["required"])
    assert template["problems"][0]["source_kind"] == "original"
    assert template["problems"][0]["calculator_policy"] == "no-calculator"


def test_external_resource_registry_is_valid_and_rights_aware() -> None:
    assert validate_external_resources(EXTERNAL_RESOURCES, COVERAGE) == ()

    registry = load_structured_data(EXTERNAL_RESOURCES)
    assert registry["resources"]
    for resource in registry["resources"]:
        if resource["license"]["status"] == "not-confirmed":
            assert resource["use_policy"] == "link-only"


def test_external_resource_validator_detects_unsafe_reuse_and_unknown_chapter(
    tmp_path: Path,
) -> None:
    registry = load_structured_data(EXTERNAL_RESOURCES)
    resource = registry["resources"][0]
    resource["use_policy"] = "adapt-with-attribution"
    resource["chapter_ids"] = ["advanced-algebra-chapter-does-not-exist"]
    path = tmp_path / "resources.yml"
    path.write_text(json.dumps(registry))

    messages = "\n".join(
        str(issue) for issue in validate_external_resources(path, COVERAGE)
    )

    assert "must be link-only" in messages
    assert "unknown chapter placement" in messages
