"""Validated, renderer-independent quiz data models."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

from fcmath.core import AnswerCheck, NumericTolerance
from fcmath.validation import (
    DomainName,
    ValidationPolicy,
    check_answer,
    load_structured_data,
)

QuestionType = Literal[
    "single-choice",
    "multiple-select",
    "numeric",
    "symbolic",
    "solution-set",
    "interval",
    "python-output",
]
QuizPurpose = Literal[
    "concept-check",
    "example-checkpoint",
    "computational-checkpoint",
    "lesson-review",
    "unit-challenge",
    "cumulative-review",
    "diagnostic",
    "comprehensive-practice",
    "timed-practice",
]

_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_QUESTION_TYPES = {
    "single-choice",
    "multiple-select",
    "numeric",
    "symbolic",
    "solution-set",
    "interval",
    "python-output",
}
_QUIZ_PURPOSES = {
    "concept-check",
    "example-checkpoint",
    "computational-checkpoint",
    "lesson-review",
    "unit-challenge",
    "cumulative-review",
    "diagnostic",
    "comprehensive-practice",
    "timed-practice",
}
_QUIZ_STATUSES = {
    "planned",
    "draft",
    "review",
    "in-development",
    "active",
    "complete",
    "archived",
}
_SKILL_MODES = {
    "conceptual",
    "manual-calculation",
    "symbolic-reasoning",
    "computational",
    "interpretation",
    "mixed",
}
_COMPATIBLE_VALIDATION = {
    "single-choice": {"exact"},
    "multiple-select": {"set-equality"},
    "numeric": {"numeric"},
    "symbolic": {"symbolic-equivalence"},
    "solution-set": {"solution-set", "set-equality"},
    "interval": {"interval", "solution-set"},
    "python-output": {"normalized-output", "exact"},
}


@dataclass(frozen=True)
class QuizOption:
    """One stable selectable option with optional targeted feedback."""

    id: str
    text: str
    feedback: str = ""


@dataclass(frozen=True)
class QuizQuestion:
    """One question whose validation is independent of its renderer."""

    id: str
    type: QuestionType
    prompt: str
    answer: object
    explanation: str
    outcome_id: str
    skill_mode: str
    validation: ValidationPolicy
    hint: str = ""
    options: tuple[QuizOption, ...] = ()

    def check(self, received: object) -> AnswerCheck:
        """Validate an answer with the question's declared policy."""

        return check_answer(received, self.answer, self.validation)


@dataclass(frozen=True)
class QuizBank:
    """A stable collection of questions shared by web and notebook renderers."""

    schema_version: int
    id: str
    title: str
    purpose: QuizPurpose
    questions: tuple[QuizQuestion, ...]
    status: str = "active"

    def question(self, question_id: str) -> QuizQuestion:
        """Return a question by stable ID."""

        for question in self.questions:
            if question.id == question_id:
                return question
        raise KeyError(question_id)

    def check(self, question_id: str, received: object) -> AnswerCheck:
        """Check an answer by stable question ID."""

        return self.question(question_id).check(received)


def load_quiz(path: str | Path) -> QuizBank:
    """Load and validate a JSON-compatible YAML quiz bank."""

    return quiz_from_mapping(load_structured_data(path))


def quiz_from_mapping(data: dict[str, Any]) -> QuizBank:
    """Build a strict internal quiz model from serialized data."""

    required_bank = ("schema_version", "id", "title", "purpose", "questions")
    for key in required_bank:
        if key not in data:
            raise ValueError(f"quiz is missing {key!r}")
    if data["schema_version"] != 1:
        raise ValueError("unsupported quiz schema_version")
    raw_questions = data["questions"]
    if not isinstance(raw_questions, list) or not raw_questions:
        raise ValueError("quiz questions must be a non-empty list")
    bank_id = str(data["id"])
    if not _ID.fullmatch(bank_id):
        raise ValueError("quiz ID must use stable lowercase kebab-case")
    purpose = str(data["purpose"])
    if purpose not in _QUIZ_PURPOSES:
        raise ValueError(f"unsupported quiz purpose {purpose!r}")
    status = str(data.get("status", "active"))
    if status not in _QUIZ_STATUSES:
        raise ValueError(f"unsupported quiz status {status!r}")

    questions = tuple(_question_from_mapping(item) for item in raw_questions)
    ids = [question.id for question in questions]
    if len(ids) != len(set(ids)):
        raise ValueError("quiz question IDs must be unique")
    return QuizBank(
        schema_version=1,
        id=bank_id,
        title=str(data["title"]),
        purpose=cast(QuizPurpose, purpose),
        questions=questions,
        status=status,
    )


def _question_from_mapping(raw: object) -> QuizQuestion:
    if not isinstance(raw, dict):
        raise ValueError("every question must be a mapping")
    data = cast(dict[str, Any], raw)
    for key in (
        "id",
        "type",
        "prompt",
        "answer",
        "explanation",
        "outcome_id",
        "skill_mode",
        "validation",
    ):
        if key not in data or data[key] in (None, ""):
            raise ValueError(f"question is missing {key!r}")
    question_type = cast(QuestionType, data["type"])
    if question_type not in _QUESTION_TYPES:
        raise ValueError(f"unsupported question type {question_type!r}")
    question_id = str(data["id"])
    if not _ID.fullmatch(question_id):
        raise ValueError("question ID must use stable lowercase kebab-case")
    outcome_id = str(data["outcome_id"])
    if not _ID.fullmatch(outcome_id):
        raise ValueError("outcome ID must use stable lowercase kebab-case")
    skill_mode = str(data["skill_mode"])
    if skill_mode not in _SKILL_MODES:
        raise ValueError(f"unsupported skill mode {skill_mode!r}")

    raw_options = data.get("options", [])
    if not isinstance(raw_options, list):
        raise ValueError("question options must be a list")
    options = tuple(_option_from_mapping(option) for option in raw_options)
    option_ids = [option.id for option in options]
    if len(option_ids) != len(set(option_ids)):
        raise ValueError(f"question {data['id']!r} has duplicate option IDs")
    if question_type in {"single-choice", "multiple-select"} and len(options) < 2:
        raise ValueError(f"question {data['id']!r} needs at least two options")
    answers = data["answer"] if isinstance(data["answer"], list) else [data["answer"]]
    if options and not set(cast(list[str], answers)).issubset(option_ids):
        raise ValueError(f"question {data['id']!r} answer is not a valid option")

    raw_validation = data["validation"]
    if not isinstance(raw_validation, dict):
        raise ValueError("validation must be a mapping")
    validation = _policy_from_mapping(
        cast(dict[str, Any], raw_validation),
        question_type,
        data,
    )
    if validation.mode not in _COMPATIBLE_VALIDATION[question_type]:
        raise ValueError(
            f"question type {question_type!r} is incompatible with "
            f"validation mode {validation.mode!r}"
        )
    return QuizQuestion(
        id=question_id,
        type=question_type,
        prompt=str(data["prompt"]),
        answer=data["answer"],
        explanation=str(data["explanation"]),
        outcome_id=outcome_id,
        skill_mode=skill_mode,
        validation=validation,
        hint=str(data.get("hint", "")),
        options=options,
    )


def _option_from_mapping(raw: object) -> QuizOption:
    if not isinstance(raw, dict) or not raw.get("id") or not raw.get("text"):
        raise ValueError("each option requires id and text")
    option_id = str(raw["id"])
    if not _ID.fullmatch(option_id):
        raise ValueError("option ID must use stable lowercase kebab-case")
    return QuizOption(
        id=option_id,
        text=str(raw["text"]),
        feedback=str(raw.get("feedback", "")),
    )


def _policy_from_mapping(
    raw: dict[str, Any],
    question_type: QuestionType,
    question: dict[str, Any],
) -> ValidationPolicy:
    if not isinstance(raw, dict) or not raw.get("mode"):
        raise ValueError("validation must declare a mode")
    if question_type == "numeric" and (
        "absolute_tolerance" not in raw or "relative_tolerance" not in raw
    ):
        raise ValueError("numeric validation must declare both tolerances")
    variables: tuple[str, ...]
    if "variables" in question:
        value = question["variables"]
        if not isinstance(value, list) or not all(
            isinstance(item, str) for item in value
        ):
            raise ValueError("variables must be a list of names")
        variables = tuple(cast(list[str], value))
    elif "variable" in question:
        variables = (str(question["variable"]),)
    else:
        variables = ()
    if question_type == "symbolic" and not variables:
        raise ValueError("symbolic questions must declare variables")
    shape = raw.get("matrix_shape")
    matrix_shape = tuple(shape) if isinstance(shape, list) and len(shape) == 2 else None
    return ValidationPolicy(
        mode=raw["mode"],
        variables=variables,
        domain=cast(DomainName, question.get("domain", raw.get("domain", "real"))),
        tolerance=NumericTolerance(
            absolute=float(raw.get("absolute_tolerance", 1e-9)),
            relative=float(raw.get("relative_tolerance", 1e-9)),
        ),
        algebraic_form=raw.get("algebraic_form", "any"),
        matrix_shape=cast(tuple[int, int] | None, matrix_shape),
        units=raw.get("units"),
        units_required=bool(raw.get("units_required", False)),
    )
