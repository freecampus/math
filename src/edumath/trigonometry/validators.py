"""Answer validators for trigonometry lessons."""

from __future__ import annotations

from typing import SupportsFloat, cast

from edumath.core import AnswerCheck, NumericTolerance, check_numeric_answer

TRIGONOMETRY_TOLERANCE = NumericTolerance(absolute=1e-9, relative=1e-9)


def validate_angle_answer(
    received: object,
    expected: float,
    *,
    tolerance: NumericTolerance = TRIGONOMETRY_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric angle answer in degrees."""

    try:
        return check_numeric_answer(
            float(cast(SupportsFloat, received)),
            float(expected),
            tolerance=tolerance,
        )
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare angle answer: {error}",
        )


def validate_trig_value_answer(
    received: object,
    expected: float,
    *,
    tolerance: NumericTolerance = TRIGONOMETRY_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric trigonometric value."""

    try:
        return check_numeric_answer(
            float(cast(SupportsFloat, received)),
            float(expected),
            tolerance=tolerance,
        )
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare trigonometric value: {error}",
        )


def validate_keyword(received: object, expected: str) -> AnswerCheck:
    """Validate a short keyword answer."""

    normalized = str(received).strip().lower()
    expected_normalized = expected.strip().lower()
    correct = normalized == expected_normalized
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


__all__ = [
    "TRIGONOMETRY_TOLERANCE",
    "validate_angle_answer",
    "validate_keyword",
    "validate_trig_value_answer",
]
