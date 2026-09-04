"""Catalog loading and structural curriculum validation."""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

VALID_STATUSES = {
    "planned",
    "draft",
    "review",
    "in-development",
    "active",
    "complete",
    "archived",
}
VALID_SKILL_MODES = {
    "conceptual",
    "manual-calculation",
    "symbolic-reasoning",
    "computational",
    "interpretation",
    "mixed",
}
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|coming soon|placeholder)\b", re.IGNORECASE)


@dataclass(frozen=True, order=True)
class ValidationIssue:
    """One actionable catalog validation failure."""

    location: str
    message: str

    def __str__(self) -> str:
        return f"{self.location}: {self.message}"


class CurriculumValidationError(ValueError):
    """Raised when a catalog fails one or more structural checks."""

    def __init__(self, issues: Iterable[ValidationIssue]) -> None:
        self.issues = tuple(sorted(issues))
        super().__init__("\n".join(str(issue) for issue in self.issues))


def load_structured_data(path: str | Path) -> dict[str, Any]:
    """Load JSON-compatible YAML, with optional PyYAML support for contributors."""

    source = Path(path)
    text = source.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as json_error:
        try:
            import yaml
        except ImportError as import_error:
            raise ValueError(
                f"{source} is not JSON-compatible YAML; install PyYAML to read it"
            ) from import_error
        value = yaml.safe_load(text)
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise ValueError(f"{source} must contain a mapping") from json_error
    if not isinstance(value, dict):
        raise ValueError(f"{source} must contain a mapping")
    return cast(dict[str, Any], value)


def validate_catalog(
    catalog_path: str | Path,
    *,
    docs_root: str | Path | None = None,
    raise_on_error: bool = False,
) -> tuple[ValidationIssue, ...]:
    """Return every catalog error instead of stopping at the first failure."""

    path = Path(catalog_path)
    root = Path(docs_root) if docs_root is not None else path.parents[1]
    catalog = load_structured_data(path)
    issues: list[ValidationIssue] = []

    for version_name in ("schema_version", "curriculum_version"):
        if not isinstance(catalog.get(version_name), int) or catalog[version_name] < 1:
            issues.append(ValidationIssue(version_name, "must be a positive integer"))

    courses = _mapping_list(catalog, "courses", issues)
    assessments = _mapping_list(catalog, "assessments", issues)
    course_ids = [str(course.get("id", "")) for course in courses]
    assessment_ids = {str(assessment.get("id", "")) for assessment in assessments}
    _duplicates(course_ids, "courses", issues)
    course_id_set = set(course_ids)
    all_ids: list[str] = []
    owned_files: dict[str, str] = {}
    outcome_ids: set[str] = set()

    for course in courses:
        course_id = str(course.get("id", ""))
        location = f"course:{course_id or '<missing>'}"
        _require_id(course_id, location, issues)
        all_ids.append(course_id)
        _status(course, location, issues)
        _owned_file(course.get("file"), location, root, owned_files, issues)
        prerequisites = _string_list(course.get("prerequisite_ids"), location, issues)
        for prerequisite in prerequisites:
            if prerequisite not in course_id_set:
                issues.append(
                    ValidationIssue(location, f"unknown prerequisite {prerequisite!r}")
                )
            if prerequisite == course_id:
                issues.append(ValidationIssue(location, "course cannot require itself"))

        outcomes = _mapping_list(course, "outcomes", issues, location)
        for outcome in outcomes:
            outcome_id = str(outcome.get("id", ""))
            _require_id(outcome_id, f"{location}/outcome", issues)
            description = str(outcome.get("description", "")).strip()
            if not description:
                issues.append(
                    ValidationIssue(f"{location}/{outcome_id}", "missing description")
                )
            outcome_ids.add(outcome_id)
            all_ids.append(outcome_id)

        units = _mapping_list(course, "units", issues, location)
        numbers: list[int] = []
        course_item_count = 0
        incomplete_units: list[str] = []
        incomplete_items: list[str] = []
        for unit in units:
            unit_id = str(unit.get("id", ""))
            unit_location = f"{location}/unit:{unit_id or '<missing>'}"
            _require_id(unit_id, unit_location, issues)
            all_ids.append(f"{course_id}/{unit_id}")
            _status(unit, unit_location, issues)
            if unit.get("status") != "complete":
                incomplete_units.append(unit_id)
            number = unit.get("number")
            if isinstance(number, int):
                numbers.append(number)
            else:
                issues.append(
                    ValidationIssue(unit_location, "number must be an integer")
                )
            _owned_file(unit.get("overview"), unit_location, root, owned_files, issues)
            directory = unit.get("directory")
            if not isinstance(directory, str) or not (root / directory).is_dir():
                issues.append(
                    ValidationIssue(unit_location, "directory does not exist")
                )
            assessment_references = _string_list(
                unit.get("assessment_ids", []), unit_location, issues
            )
            for assessment_id in assessment_references:
                if assessment_id not in assessment_ids:
                    issues.append(
                        ValidationIssue(
                            unit_location,
                            f"unknown assessment {assessment_id!r}",
                        )
                    )

            items = [
                *_mapping_list(unit, "lessons", issues, unit_location),
                *_mapping_list(unit, "challenges", issues, unit_location),
            ]
            course_item_count += len(items)
            orders = [item.get("order") for item in items]
            if any(not isinstance(order, int) or order < 1 for order in orders):
                issues.append(
                    ValidationIssue(
                        unit_location, "item order values must be positive integers"
                    )
                )
            elif len(set(cast(list[int], orders))) != len(orders):
                issues.append(
                    ValidationIssue(unit_location, "item order values must be unique")
                )
            elif sorted(cast(list[int], orders)) != list(range(1, len(orders) + 1)):
                issues.append(
                    ValidationIssue(
                        unit_location, "item order values must be contiguous from 1"
                    )
                )

            declared_count = unit.get("item_count")
            if declared_count is not None and declared_count != len(items):
                issues.append(ValidationIssue(unit_location, "stale item_count"))

            for item in items:
                item_id = str(item.get("id", ""))
                item_location = f"{unit_location}/item:{item_id or '<missing>'}"
                _require_id(item_id, item_location, issues)
                all_ids.append(item_id)
                _status(item, item_location, issues)
                if item.get("status") != "complete":
                    incomplete_items.append(item_id)
                _owned_file(item.get("file"), item_location, root, owned_files, issues)
                item_outcomes = _string_list(
                    item.get("outcome_ids"), item_location, issues
                )
                if not item_outcomes:
                    issues.append(
                        ValidationIssue(
                            item_location, "at least one outcome_id is required"
                        )
                    )
                for outcome_id in item_outcomes:
                    if outcome_id not in outcome_ids and not any(
                        outcome_id == str(candidate.get("id", ""))
                        for candidate_course in courses
                        for candidate in candidate_course.get("outcomes", [])
                        if isinstance(candidate, Mapping)
                    ):
                        issues.append(
                            ValidationIssue(
                                item_location, f"unknown outcome {outcome_id!r}"
                            )
                        )
                modes = _string_list(item.get("skill_modes"), item_location, issues)
                invalid_modes = set(modes) - VALID_SKILL_MODES
                if invalid_modes:
                    issues.append(
                        ValidationIssue(
                            item_location,
                            f"invalid skill modes {sorted(invalid_modes)}",
                        )
                    )
                if not isinstance(item.get("estimated_minutes"), int):
                    issues.append(
                        ValidationIssue(
                            item_location, "estimated_minutes must be an integer"
                        )
                    )
                coverage = item.get("coverage")
                if not isinstance(coverage, Mapping):
                    issues.append(
                        ValidationIssue(item_location, "coverage mapping is required")
                    )
                if item.get("status") == "complete":
                    if isinstance(coverage, Mapping) and not all(coverage.values()):
                        issues.append(
                            ValidationIssue(
                                item_location, "complete item has coverage gaps"
                            )
                        )
                    file_value = item.get("file")
                    if isinstance(file_value, str) and (root / file_value).is_file():
                        if PLACEHOLDER.search(
                            (root / file_value).read_text(encoding="utf-8")
                        ):
                            issues.append(
                                ValidationIssue(
                                    item_location,
                                    "complete item contains a placeholder",
                                )
                            )
                _check_front_matter(
                    item, course_id, unit_id, root, issues, item_location
                )

            if unit.get("status") == "complete":
                if not items:
                    issues.append(
                        ValidationIssue(unit_location, "complete unit has no items")
                    )
                unit_incomplete = [
                    str(item.get("id", ""))
                    for item in items
                    if item.get("status") != "complete"
                ]
                if unit_incomplete:
                    issues.append(
                        ValidationIssue(
                            unit_location,
                            f"complete unit has incomplete items: {unit_incomplete}",
                        )
                    )

        expected_numbers = list(range(1, len(units) + 1))
        if sorted(numbers) != expected_numbers:
            issues.append(
                ValidationIssue(location, "unit numbers must be contiguous from 1")
            )
        if (
            course.get("item_count") is not None
            and course.get("item_count") != course_item_count
        ):
            issues.append(ValidationIssue(location, "stale item_count"))
        if course.get("status") == "complete":
            if not units or not course_item_count:
                issues.append(
                    ValidationIssue(location, "complete course has no curriculum items")
                )
            if incomplete_units:
                issues.append(
                    ValidationIssue(
                        location,
                        f"complete course has incomplete units: {incomplete_units}",
                    )
                )
            if incomplete_items:
                issues.append(
                    ValidationIssue(
                        location,
                        f"complete course has incomplete items: {incomplete_items}",
                    )
                )

    _cycles(courses, issues)

    for assessment in assessments:
        assessment_id = str(assessment.get("id", ""))
        location = f"assessment:{assessment_id or '<missing>'}"
        _require_id(assessment_id, location, issues)
        all_ids.append(assessment_id)
        _status(assessment, location, issues)
        _owned_file(assessment.get("file"), location, root, owned_files, issues)
        quiz_file = assessment.get("quiz_file")
        if quiz_file is not None and (
            not isinstance(quiz_file, str) or not (root / quiz_file).is_file()
        ):
            issues.append(ValidationIssue(location, "quiz_file does not exist"))
        assessment_outcomes = _string_list(
            assessment.get("outcome_ids"), location, issues
        )
        if not assessment_outcomes:
            issues.append(
                ValidationIssue(location, "at least one outcome_id is required")
            )
        for outcome_id in assessment_outcomes:
            if outcome_id not in outcome_ids:
                issues.append(
                    ValidationIssue(location, f"unknown outcome {outcome_id!r}")
                )
        modes = _string_list(assessment.get("skill_modes"), location, issues)
        if not modes or set(modes) - VALID_SKILL_MODES:
            issues.append(
                ValidationIssue(location, "assessment skill_modes are invalid")
            )
        if not isinstance(assessment.get("estimated_minutes"), int):
            issues.append(
                ValidationIssue(location, "estimated_minutes must be an integer")
            )
        _check_assessment_front_matter(assessment, root, issues, location)

    _duplicates(all_ids, "catalog", issues)

    lesson_files = {
        path.relative_to(root).as_posix()
        for path in (root / "courses").glob("*/units/*/*.qmd")
        if path.name != "index.qmd"
    }
    catalog_lesson_files = {
        file
        for file in owned_files
        if "/units/" in file and not file.endswith("/index.qmd")
    }
    for orphan in sorted(lesson_files - catalog_lesson_files):
        issues.append(
            ValidationIssue(orphan, "orphan lesson page is not owned by the catalog")
        )

    result = tuple(sorted(issues))
    if result and raise_on_error:
        raise CurriculumValidationError(result)
    return result


def _mapping_list(
    source: Mapping[str, Any],
    key: str,
    issues: list[ValidationIssue],
    location: str = "catalog",
) -> list[dict[str, Any]]:
    value = source.get(key)
    if not isinstance(value, list):
        issues.append(ValidationIssue(location, f"{key} must be a list"))
        return []
    result: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if isinstance(item, dict):
            result.append(cast(dict[str, Any], item))
        else:
            issues.append(
                ValidationIssue(f"{location}/{key}[{index}]", "must be a mapping")
            )
    return result


def _string_list(
    value: object, location: str, issues: list[ValidationIssue]
) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        issues.append(ValidationIssue(location, "expected a list of strings"))
        return []
    return cast(list[str], value)


def _require_id(value: str, location: str, issues: list[ValidationIssue]) -> None:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        issues.append(
            ValidationIssue(location, "ID must use stable lowercase kebab-case")
        )


def _status(
    source: Mapping[str, Any], location: str, issues: list[ValidationIssue]
) -> None:
    if source.get("status") not in VALID_STATUSES:
        issues.append(
            ValidationIssue(location, f"invalid status {source.get('status')!r}")
        )


def _duplicates(
    values: Iterable[str], location: str, issues: list[ValidationIssue]
) -> None:
    for value, count in Counter(values).items():
        if value and count > 1:
            issues.append(ValidationIssue(location, f"duplicate ID {value!r}"))


def _owned_file(
    value: object,
    owner: str,
    root: Path,
    owned: dict[str, str],
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(value, str):
        issues.append(ValidationIssue(owner, "file path is required"))
        return
    if value in owned:
        issues.append(ValidationIssue(owner, f"file already owned by {owned[value]}"))
    owned[value] = owner
    if not (root / value).is_file():
        issues.append(ValidationIssue(owner, f"missing file {value!r}"))


def _cycles(courses: list[dict[str, Any]], issues: list[ValidationIssue]) -> None:
    graph = {
        str(course.get("id")): [
            str(item) for item in course.get("prerequisite_ids", [])
        ]
        for course in courses
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(course_id: str, trail: tuple[str, ...]) -> None:
        if course_id in visiting:
            start = trail.index(course_id) if course_id in trail else 0
            cycle = " -> ".join((*trail[start:], course_id))
            issues.append(ValidationIssue("courses", f"cyclic prerequisites: {cycle}"))
            return
        if course_id in visited:
            return
        visiting.add(course_id)
        for prerequisite in graph.get(course_id, []):
            visit(prerequisite, (*trail, course_id))
        visiting.remove(course_id)
        visited.add(course_id)

    for course_id in graph:
        visit(course_id, ())


def _check_front_matter(
    item: Mapping[str, Any],
    course_id: str,
    unit_id: str,
    root: Path,
    issues: list[ValidationIssue],
    location: str,
) -> None:
    file_value = item.get("file")
    if not isinstance(file_value, str) or not (root / file_value).is_file():
        return
    text = (root / file_value).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        issues.append(ValidationIssue(location, "QMD front matter is missing"))
        return
    end = text.find("\n---\n", 4)
    if end < 0:
        issues.append(ValidationIssue(location, "QMD front matter is not closed"))
        return
    front_matter = text[4:end]
    expected = {
        "id": item.get("id"),
        "course_id": course_id,
        "unit_id": unit_id,
        "page_type": item.get("type"),
        "status": item.get("status"),
    }
    for key, value in expected.items():
        match = re.search(
            rf"(?m)^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", front_matter
        )
        if match is None or match.group(1).strip() != str(value):
            issues.append(
                ValidationIssue(location, f"QMD {key} disagrees with catalog")
            )
    for key in ("outcome_ids", "skill_modes"):
        expected_values = item.get(key)
        match = re.search(rf"(?m)^{re.escape(key)}:\s*\[(.*?)\]\s*$", front_matter)
        actual_values = (
            [
                value.strip().strip("\"'")
                for value in match.group(1).split(",")
                if value.strip()
            ]
            if match
            else None
        )
        if actual_values != expected_values:
            issues.append(
                ValidationIssue(location, f"QMD {key} disagrees with catalog")
            )
    time_match = re.search(
        r'(?m)^estimated_time:\s*["\']?(.*?)["\']?\s*$', front_matter
    )
    expected_time = f"{item.get('estimated_minutes')} minutes"
    if time_match is None or time_match.group(1).strip() != expected_time:
        issues.append(
            ValidationIssue(location, "QMD estimated_time disagrees with catalog")
        )


def _check_assessment_front_matter(
    assessment: Mapping[str, Any],
    root: Path,
    issues: list[ValidationIssue],
    location: str,
) -> None:
    file_value = assessment.get("file")
    if not isinstance(file_value, str) or not (root / file_value).is_file():
        return
    text = (root / file_value).read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        issues.append(ValidationIssue(location, "QMD front matter is missing"))
        return
    end = text.find("\n---\n", 4)
    if end < 0:
        issues.append(ValidationIssue(location, "QMD front matter is not closed"))
        return
    front_matter = text[4:end]
    scalar_expectations = {
        "id": assessment.get("id"),
        "page_type": "assessment",
        "status": assessment.get("status"),
        "estimated_time": f"{assessment.get('estimated_minutes')} minutes",
    }
    for key, expected in scalar_expectations.items():
        match = re.search(
            rf"(?m)^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", front_matter
        )
        if match is None or match.group(1).strip() != str(expected):
            issues.append(
                ValidationIssue(location, f"QMD {key} disagrees with catalog")
            )
    for key in ("outcome_ids", "skill_modes"):
        match = re.search(rf"(?m)^{re.escape(key)}:\s*\[(.*?)\]\s*$", front_matter)
        actual = (
            [
                value.strip().strip("\"'")
                for value in match.group(1).split(",")
                if value.strip()
            ]
            if match
            else None
        )
        if actual != assessment.get(key):
            issues.append(
                ValidationIssue(location, f"QMD {key} disagrees with catalog")
            )
