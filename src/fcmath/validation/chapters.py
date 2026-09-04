"""Structural validation for book-scale mathematics chapters."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from fcmath.validation.curriculum import ValidationIssue, load_structured_data

_REVIEWABLE_STATUSES = {"review", "active", "complete"}
_REQUIRED_HEADINGS = (
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
_WORD = re.compile(r"\b[\w-]+\b")
_HEADING = re.compile(r"(?m)^## (?:\d+\.\s+)?(.+?)\s*$")
_PROBLEM_ID = re.compile(r'data-problem-id="([a-z0-9-]+)"')
_LEVEL = re.compile(r'data-level="([A-D])"')
_QUIZ = re.compile(r'<fc-quiz\s+data-source="([^"]+)"[^>]*>')
_PYTHON = re.compile(r"```\{python\}(.*?)```", re.DOTALL)
_PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|coming soon|placeholder)\b", re.IGNORECASE)


def validate_chapter_contracts(
    coverage_path: str | Path,
    *,
    docs_root: str | Path,
) -> tuple[ValidationIssue, ...]:
    """Validate every reviewable Advanced Algebra chapter.

    Draft chapters may be incomplete. A chapter marked ``review``, ``active``,
    or ``complete`` must already satisfy the structural contract required for
    independent mathematical and editorial review.
    """

    coverage = load_structured_data(coverage_path)
    root = Path(docs_root).resolve()
    issues: list[ValidationIssue] = []
    global_problem_locations: dict[str, list[str]] = {}

    for raw_unit in coverage.get("units", []):
        if not isinstance(raw_unit, Mapping):
            continue
        for raw_chapter in raw_unit.get("chapters", []):
            if not isinstance(raw_chapter, Mapping):
                continue
            chapter = cast(Mapping[str, Any], raw_chapter)
            if chapter.get("status") not in _REVIEWABLE_STATUSES:
                continue
            chapter_id = str(chapter.get("id", "<missing>"))
            location = f"chapter-contract:{chapter_id}"
            source_value = chapter.get("source_file")
            if not isinstance(source_value, str):
                issues.append(ValidationIssue(location, "source_file is required"))
                continue
            source = (root / source_value).resolve()
            if not source.is_relative_to(root) or not source.is_file():
                issues.append(
                    ValidationIssue(location, "source_file must exist under docs")
                )
                continue
            text = source.read_text(encoding="utf-8")
            headings = _HEADING.findall(text)
            problem_ids = _PROBLEM_ID.findall(text)
            levels = set(_LEVEL.findall(text))

            if len(_WORD.findall(text)) < 3_000:
                issues.append(
                    ValidationIssue(
                        location, "reviewable chapter has fewer than 3000 words"
                    )
                )
            for required in _REQUIRED_HEADINGS:
                if not any(heading.startswith(required) for heading in headings):
                    issues.append(
                        ValidationIssue(
                            location, f"missing required heading {required!r}"
                        )
                    )
            if headings and headings[-1] != "Using this lesson with fcmath and SymPy":
                issues.append(
                    ValidationIssue(location, "fcmath and SymPy appendix must be last")
                )
            if text.count("{.worked-example") < 8:
                issues.append(
                    ValidationIssue(location, "fewer than eight worked examples")
                )
            if len(problem_ids) < 12:
                issues.append(
                    ValidationIssue(location, "fewer than twelve stable problem IDs")
                )
            for problem_id, count in Counter(problem_ids).items():
                if count > 1:
                    issues.append(
                        ValidationIssue(
                            location, f"duplicate problem ID {problem_id!r}"
                        )
                    )
                global_problem_locations.setdefault(problem_id, []).append(location)
            if levels != {"A", "B", "C", "D"}:
                issues.append(
                    ValidationIssue(
                        location, "problems must span levels A, B, C, and D"
                    )
                )
            if _PLACEHOLDER.search(text):
                issues.append(
                    ValidationIssue(
                        location, "reviewable chapter contains a placeholder"
                    )
                )
            if 'target="_blank"' in text or "target='_blank'" in text:
                issues.append(
                    ValidationIssue(
                        location, "chapter must not force links into new tabs"
                    )
                )

            quiz_references = _QUIZ.findall(text)
            if not quiz_references:
                issues.append(ValidationIssue(location, "topic quiz is required"))
            for reference in quiz_references:
                quiz_path = (source.parent / reference).resolve()
                if not quiz_path.is_relative_to(root) or not quiz_path.is_file():
                    issues.append(
                        ValidationIssue(
                            location, f"missing quiz resource {reference!r}"
                        )
                    )

            appendix_start = text.rfind("## Using this lesson with fcmath and SymPy")
            if appendix_start < 0 or "#| echo: true" not in text[appendix_start:]:
                issues.append(
                    ValidationIssue(
                        location, "final appendix needs visible Python code"
                    )
                )
            for chunk in _PYTHON.findall(text):
                if (
                    ".plot(" in chunk or ".render(" in chunk
                ) and "#| fig-alt:" not in chunk:
                    issues.append(
                        ValidationIssue(location, "rendered plots require fig-alt text")
                    )

    for problem_id, locations in global_problem_locations.items():
        if len(locations) > 1:
            issues.append(
                ValidationIssue(
                    "chapter-contracts",
                    f"problem ID {problem_id!r} appears in multiple chapters",
                )
            )

    return tuple(sorted(issues))
