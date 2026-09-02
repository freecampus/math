#!/usr/bin/env python3
"""Validate curriculum and quiz data from one fast CI entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fcmath.quizzes import load_quiz
from fcmath.validation import ValidationIssue, load_structured_data, validate_catalog


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalog", type=Path, default=ROOT / "docs/courses/_catalog.yml"
    )
    args = parser.parse_args()
    issues = list(validate_catalog(args.catalog, docs_root=ROOT / "docs"))
    catalog = load_structured_data(args.catalog)
    outcome_ids = {
        outcome["id"]
        for course in catalog.get("courses", [])
        for outcome in course.get("outcomes", [])
    }
    question_ids: set[str] = set()
    quiz_ids: set[str] = set()
    quiz_outcomes: dict[str, set[str]] = {}
    for quiz_path in sorted((ROOT / "docs/quizzes").rglob("*.yml")):
        try:
            quiz = load_quiz(quiz_path)
        except (TypeError, ValueError) as error:
            issues.append(ValidationIssue(str(quiz_path.relative_to(ROOT)), str(error)))
            continue
        relative_quiz = quiz_path.relative_to(ROOT / "docs").as_posix()
        if quiz.id in quiz_ids:
            issues.append(
                ValidationIssue(relative_quiz, f"duplicate quiz ID {quiz.id!r}")
            )
        quiz_ids.add(quiz.id)
        quiz_outcomes[relative_quiz] = {
            question.outcome_id for question in quiz.questions
        }
        for question in quiz.questions:
            if question.id in question_ids:
                quiz_name = quiz_path.relative_to(ROOT)
                issues.append(
                    ValidationIssue(
                        str(quiz_name),
                        f"duplicate global question ID {question.id!r}",
                    )
                )
            question_ids.add(question.id)
            if question.outcome_id not in outcome_ids:
                quiz_name = quiz_path.relative_to(ROOT)
                issues.append(
                    ValidationIssue(
                        str(quiz_name),
                        f"unknown outcome {question.outcome_id!r}",
                    )
                )
    for assessment in catalog.get("assessments", []):
        quiz_file = assessment.get("quiz_file")
        if not isinstance(quiz_file, str) or quiz_file not in quiz_outcomes:
            continue
        expected = set(assessment.get("outcome_ids", []))
        if quiz_outcomes[quiz_file] != expected:
            issues.append(
                ValidationIssue(
                    f"assessment:{assessment.get('id', '<missing>')}",
                    "outcome_ids disagree with the linked quiz bank",
                )
            )
    if issues:
        print("\n".join(str(issue) for issue in issues), file=sys.stderr)
        return 1
    print(
        f"Curriculum valid: {len(catalog['courses'])} courses, "
        f"{len(outcome_ids)} outcomes, {len(question_ids)} quiz questions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
