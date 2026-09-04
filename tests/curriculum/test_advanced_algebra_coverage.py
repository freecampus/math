import json
from pathlib import Path

from fcmath.quizzes import load_quiz
from fcmath.validation import (
    load_structured_data,
    validate_chapter_contracts,
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
    assert len(exemplars) == 6
    assert validate_chapter_contracts(COVERAGE, docs_root=ROOT / "docs") == ()


def test_chapter_contract_validator_rejects_incomplete_review_chapter(
    tmp_path: Path,
) -> None:
    coverage = {
        "units": [
            {
                "chapters": [
                    {
                        "id": "incomplete-review-chapter",
                        "status": "review",
                        "source_file": "bad.qmd",
                    }
                ]
            }
        ]
    }
    (tmp_path / "coverage.yml").write_text(json.dumps(coverage))
    (tmp_path / "bad.qmd").write_text(
        '## Why this matters\n\nTODO: expand.\n\n<a target="_blank">link</a>\n'
    )

    messages = "\n".join(
        str(issue)
        for issue in validate_chapter_contracts(
            tmp_path / "coverage.yml", docs_root=tmp_path
        )
    )

    assert "fewer than 3000 words" in messages
    assert "missing required heading 'Common mistakes'" in messages
    assert "fewer than eight worked examples" in messages
    assert "contains a placeholder" in messages
    assert "must not force links into new tabs" in messages
    assert "topic quiz is required" in messages


def test_reference_chapter_quizzes_are_valid() -> None:
    quiz_root = ROOT / "docs/quizzes/advanced-algebra"
    expected = {
        "argument-language.yml": (8, "active"),
        "readiness-diagnostic.yml": (24, "active"),
        "sets-logic.yml": (10, "active"),
        "number-systems.yml": (10, "review"),
        "algebraic-laws.yml": (10, "review"),
        "proof-methods.yml": (10, "review"),
    }

    for name, (expected_count, expected_status) in expected.items():
        bank = load_quiz(quiz_root / name)
        assert bank.status == expected_status
        assert len(bank.questions) == expected_count


def test_unit_one_proof_assessments_are_registered() -> None:
    catalog = load_structured_data(CATALOG)
    course = next(
        course for course in catalog["courses"] if course["id"] == "advanced-algebra"
    )
    unit = next(
        unit for unit in course["units"] if unit["id"] == "mathematical-language"
    )
    portfolio = next(
        challenge
        for challenge in unit["challenges"]
        if challenge["id"]
        == "advanced-algebra-mathematical-language-unit-1-proof-portfolio"
    )
    examination = next(
        assessment
        for assessment in catalog["assessments"]
        if assessment["id"] == "advanced-algebra-unit-1-proof-examination"
    )

    assert unit["assessment_ids"] == ["advanced-algebra-unit-1-proof-examination"]
    assert portfolio["status"] == "review"
    assert portfolio["estimated_minutes"] == 360
    assert examination["status"] == "review"
    assert examination["estimated_minutes"] == 75
    assert set(examination["outcome_ids"]) == {
        "advanced-algebra-outcome-1",
        "advanced-algebra-outcome-3",
        "advanced-algebra-outcome-6",
        "advanced-algebra-outcome-7",
        "advanced-algebra-outcome-8",
        "advanced-algebra-outcome-14",
    }


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
