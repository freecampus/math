"""Answer validators for probability lessons."""

from __future__ import annotations

import math
from collections.abc import Hashable, Iterable, Sequence
from typing import TypeVar

from edumath.core import AnswerCheck, NumericTolerance, check_numeric_answer

T = TypeVar("T", bound=Hashable)
PROBABILITY_TOLERANCE = NumericTolerance(absolute=1e-9, relative=1e-9)


def validate_probability_answer(
    received: object,
    expected: float,
    *,
    tolerance: NumericTolerance = PROBABILITY_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric probability answer."""

    try:
        numeric = _parse_probability(received)
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not read probability answer: {error}",
        )
    return check_numeric_answer(numeric, float(expected), tolerance=tolerance)


def validate_probabilities(probabilities: Sequence[float]) -> AnswerCheck:
    """Validate that probabilities are non-negative and sum to one."""

    try:
        total = sum(float(probability) for probability in probabilities)
        non_negative = all(float(probability) >= 0 for probability in probabilities)
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=probabilities,
            expected="probabilities that sum to 1",
            message=f"Could not read probabilities: {error}",
        )

    correct = (
        bool(probabilities)
        and non_negative
        and math.isclose(
            total,
            1.0,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )
    )
    return AnswerCheck(
        correct=correct,
        received=probabilities,
        expected="non-negative probabilities summing to 1",
        message="Correct."
        if correct
        else f"Probabilities must sum to 1; total was {total}.",
    )


def validate_pmf(
    values: Sequence[object], probabilities: Sequence[float]
) -> AnswerCheck:
    """Validate a finite probability mass function table."""

    if len(values) != len(probabilities):
        return AnswerCheck(
            correct=False,
            received=(values, probabilities),
            expected="same number of values and probabilities",
            message="A PMF must pair each value with exactly one probability.",
        )
    return validate_probabilities(probabilities)


def validate_event_subset(event: Iterable[T], sample_space: Iterable[T]) -> AnswerCheck:
    """Validate that an event is a subset of the sample space."""

    event_set = set(event)
    sample = set(sample_space)
    correct = event_set <= sample
    return AnswerCheck(
        correct=correct,
        received=event_set,
        expected=f"subset of {sample}",
        message=(
            "Correct."
            if correct
            else (
                "The event contains outcomes outside the sample space: "
                f"{event_set - sample}."
            )
        ),
    )


def is_independent(
    prob_a: float,
    prob_b: float,
    prob_a_and_b: float,
    *,
    tolerance: float = 1e-9,
) -> bool:
    """Return whether ``P(A and B)`` equals ``P(A) P(B)`` within tolerance."""

    return math.isclose(
        float(prob_a_and_b),
        float(prob_a) * float(prob_b),
        rel_tol=tolerance,
        abs_tol=tolerance,
    )


def _parse_probability(value: object) -> float:
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            msg = "empty answer"
            raise ValueError(msg)
        if "/" in stripped:
            numerator, denominator = stripped.split("/", maxsplit=1)
            return float(numerator) / float(denominator)
        if stripped.endswith("%"):
            return float(stripped[:-1]) / 100
        return float(stripped)
    return float(value)  # type: ignore[arg-type]


__all__ = [
    "PROBABILITY_TOLERANCE",
    "is_independent",
    "validate_event_subset",
    "validate_pmf",
    "validate_probabilities",
    "validate_probability_answer",
]
