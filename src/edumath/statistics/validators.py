"""Answer validators for statistics lessons."""

from __future__ import annotations

from collections.abc import Sequence

from edumath.core import AnswerCheck, NumericTolerance, check_numeric_answer

STATISTICS_TOLERANCE = NumericTolerance(absolute=1e-6, relative=1e-6)


def validate_numeric_answer(
    received: object,
    expected: float,
    *,
    tolerance: NumericTolerance = STATISTICS_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric statistics answer."""

    try:
        numeric = _parse_float(received)
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not read numeric answer: {error}",
        )
    return check_numeric_answer(numeric, float(expected), tolerance=tolerance)


def validate_interval_answer(
    received: object,
    expected: tuple[float, float],
    *,
    tolerance: NumericTolerance = STATISTICS_TOLERANCE,
) -> AnswerCheck:
    """Validate a two-number interval answer."""

    try:
        lower, upper = _parse_interval(received)
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not read interval answer: {error}",
        )

    lower_check = check_numeric_answer(lower, expected[0], tolerance=tolerance)
    upper_check = check_numeric_answer(upper, expected[1], tolerance=tolerance)
    correct = lower_check.correct and upper_check.correct
    return AnswerCheck(
        correct=correct,
        received=(lower, upper),
        expected=expected,
        message="Correct." if correct else f"Expected interval {expected}.",
    )


def validate_keyword_answer(received: object, expected: str) -> AnswerCheck:
    """Validate a short text answer by normalized keyword."""

    normalized = str(received).strip().lower().replace("_", "-")
    expected_normalized = expected.strip().lower().replace("_", "-")
    correct = normalized == expected_normalized
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


def _parse_float(value: object) -> float:
    if isinstance(value, str):
        text = value.strip()
        if not text:
            msg = "empty answer"
            raise ValueError(msg)
        if text.endswith("%"):
            return float(text[:-1]) / 100
        if "/" in text:
            numerator, denominator = text.split("/", maxsplit=1)
            return float(numerator) / float(denominator)
        return float(text)
    return float(value)  # type: ignore[arg-type]


def _parse_interval(value: object) -> tuple[float, float]:
    if isinstance(value, str):
        text = value.strip().strip("[]()")
        separator = "," if "," in text else " "
        parts = [part for part in text.split(separator) if part]
        if len(parts) != 2:
            msg = "interval must contain exactly two numbers"
            raise ValueError(msg)
        return _parse_float(parts[0]), _parse_float(parts[1])
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        if len(value) != 2:
            msg = "interval sequence must contain exactly two numbers"
            raise ValueError(msg)
        return _parse_float(value[0]), _parse_float(value[1])
    msg = "interval must be a string or two-number sequence"
    raise TypeError(msg)


__all__ = [
    "STATISTICS_TOLERANCE",
    "validate_interval_answer",
    "validate_keyword_answer",
    "validate_numeric_answer",
]
