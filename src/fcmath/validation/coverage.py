"""Validation for book-scale course coverage matrices."""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from fcmath.validation.curriculum import ValidationIssue, load_structured_data

_CHAPTER_STATUSES = {"planned", "in-development", "active", "complete"}
_PROBLEM_LEVELS = {"A", "B", "C", "D"}


def validate_coverage_matrix(
    coverage_path: str | Path,
    catalog_path: str | Path,
) -> tuple[ValidationIssue, ...]:
    """Validate a course coverage matrix against the curriculum catalog.

    The matrix is intentionally stricter than the public catalog.  It records
    the complete book architecture, including chapters that have not yet been
    published, while requiring every published chapter to agree with its
    catalog identity and source path.
    """

    coverage = load_structured_data(coverage_path)
    catalog = load_structured_data(catalog_path)
    issues: list[ValidationIssue] = []

    if not isinstance(coverage.get("schema_version"), int):
        issues.append(ValidationIssue("coverage", "schema_version must be an integer"))

    course_id = coverage.get("course_id")
    courses = catalog.get("courses", [])
    course = next(
        (
            candidate
            for candidate in courses
            if isinstance(candidate, Mapping) and candidate.get("id") == course_id
        ),
        None,
    )
    if course is None:
        issues.append(
            ValidationIssue("coverage", f"unknown catalog course {course_id!r}")
        )
        return tuple(sorted(issues))

    catalog_outcomes = {
        str(outcome.get("id"))
        for outcome in course.get("outcomes", [])
        if isinstance(outcome, Mapping)
    }
    catalog_items = {
        str(item.get("id")): item
        for unit in course.get("units", [])
        if isinstance(unit, Mapping)
        for group in ("lessons", "challenges")
        for item in unit.get(group, [])
        if isinstance(item, Mapping)
    }

    units = coverage.get("units")
    if not isinstance(units, list) or not units:
        issues.append(ValidationIssue("coverage", "units must be a non-empty list"))
        return tuple(sorted(issues))

    book_units: list[int] = []
    chapters: list[dict[str, Any]] = []
    for unit_index, raw_unit in enumerate(units):
        unit_location = f"coverage/unit[{unit_index}]"
        if not isinstance(raw_unit, dict):
            issues.append(ValidationIssue(unit_location, "unit must be a mapping"))
            continue
        book_unit = raw_unit.get("book_unit")
        if not isinstance(book_unit, int):
            issues.append(
                ValidationIssue(unit_location, "book_unit must be an integer")
            )
        else:
            book_units.append(book_unit)
        raw_chapters = raw_unit.get("chapters")
        if not isinstance(raw_chapters, list) or not raw_chapters:
            issues.append(
                ValidationIssue(unit_location, "chapters must be a non-empty list")
            )
            continue
        for raw_chapter in raw_chapters:
            if isinstance(raw_chapter, dict):
                chapter = cast(dict[str, Any], raw_chapter)
                chapters.append(chapter)
            else:
                issues.append(
                    ValidationIssue(unit_location, "each chapter must be a mapping")
                )

    if sorted(book_units) != list(range(0, 11)):
        issues.append(
            ValidationIssue(
                "coverage", "book_unit values must be contiguous from 0 to 10"
            )
        )

    declared_count = coverage.get("chapter_count")
    if declared_count != len(chapters):
        issues.append(ValidationIssue("coverage", "stale chapter_count"))

    chapter_ids = [str(chapter.get("id", "")) for chapter in chapters]
    chapter_numbers = [str(chapter.get("number", "")) for chapter in chapters]
    for label, values in (
        ("chapter ID", chapter_ids),
        ("chapter number", chapter_numbers),
    ):
        for value, count in Counter(values).items():
            if not value:
                issues.append(ValidationIssue("coverage", f"missing {label}"))
            elif count > 1:
                issues.append(
                    ValidationIssue("coverage", f"duplicate {label} {value!r}")
                )

    known_chapters: set[str] = set()
    outcome_counts: Counter[str] = Counter()
    for chapter in chapters:
        chapter_id = str(chapter.get("id", "<missing>"))
        location = f"coverage/chapter:{chapter_id}"
        status = chapter.get("status")
        if status not in _CHAPTER_STATUSES:
            issues.append(ValidationIssue(location, f"invalid status {status!r}"))

        title = chapter.get("title")
        if not isinstance(title, str) or not title.strip():
            issues.append(ValidationIssue(location, "title is required"))
        scope = chapter.get("scope")
        if not isinstance(scope, str) or len(scope.split()) < 8:
            issues.append(
                ValidationIssue(location, "scope must be a substantive sentence")
            )

        outcome_ids = chapter.get("outcome_ids")
        if not isinstance(outcome_ids, list) or not outcome_ids:
            issues.append(ValidationIssue(location, "outcome_ids must be non-empty"))
        else:
            for outcome_id in outcome_ids:
                if outcome_id not in catalog_outcomes:
                    issues.append(
                        ValidationIssue(location, f"unknown outcome {outcome_id!r}")
                    )
                elif isinstance(outcome_id, str):
                    outcome_counts[outcome_id] += 1

        prerequisites = chapter.get("prerequisite_chapter_ids")
        if not isinstance(prerequisites, list) or not all(
            isinstance(value, str) for value in prerequisites
        ):
            issues.append(
                ValidationIssue(location, "prerequisite_chapter_ids must be a list")
            )
        else:
            for prerequisite in prerequisites:
                if prerequisite not in known_chapters:
                    issues.append(
                        ValidationIssue(
                            location,
                            f"prerequisite {prerequisite!r} must refer to an "
                            "earlier chapter",
                        )
                    )

        levels = chapter.get("problem_levels")
        if not isinstance(levels, list) or set(levels) != _PROBLEM_LEVELS:
            issues.append(
                ValidationIssue(location, "problem_levels must contain A, B, C, and D")
            )
        for key in ("assessment_evidence", "fcmath_support"):
            metadata_values = chapter.get(key)
            if (
                not isinstance(metadata_values, list)
                or not metadata_values
                or not all(
                    isinstance(value, str) and value.strip()
                    for value in metadata_values
                )
            ):
                issues.append(ValidationIssue(location, f"{key} must be non-empty"))

        catalog_item_id = chapter.get("catalog_item_id")
        source_file = chapter.get("source_file")
        if status in {"active", "complete"}:
            item = catalog_items.get(str(catalog_item_id))
            if item is None:
                issues.append(
                    ValidationIssue(
                        location, "published chapter is missing from catalog"
                    )
                )
            else:
                if item.get("file") != source_file:
                    issues.append(
                        ValidationIssue(location, "source_file disagrees with catalog")
                    )
                if item.get("status") != status:
                    issues.append(
                        ValidationIssue(location, "status disagrees with catalog")
                    )
                if item.get("outcome_ids") != outcome_ids:
                    issues.append(
                        ValidationIssue(location, "outcome_ids disagree with catalog")
                    )
        elif catalog_item_id is not None or source_file is not None:
            issues.append(
                ValidationIssue(
                    location,
                    "unpublished chapter must not claim a catalog item or source file",
                )
            )

        known_chapters.add(chapter_id)

    uncovered = sorted(catalog_outcomes - set(outcome_counts))
    if uncovered:
        issues.append(
            ValidationIssue(
                "coverage", f"course outcomes have no planned chapters: {uncovered}"
            )
        )

    return tuple(sorted(issues))
