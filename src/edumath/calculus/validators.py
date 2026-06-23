"""Calculus answer validators."""

from __future__ import annotations

from typing import SupportsFloat, cast

import sympy as sp

from edumath.core import (
    AnswerCheck,
    NumericTolerance,
    check_expression_answer,
    check_numeric_answer,
)

LIMIT_TOLERANCE = NumericTolerance(absolute=1e-6, relative=1e-6)
APPROXIMATION_TOLERANCE = NumericTolerance(absolute=1e-4, relative=1e-4)
CRITICAL_POINT_TOLERANCE = NumericTolerance(absolute=1e-9, relative=1e-9)


def validate_derivative_equivalence(
    received: str | sp.Expr,
    expected: str | sp.Expr,
    *,
    variable: str = "x",
) -> AnswerCheck:
    """Validate that two derivative expressions are equivalent."""

    return check_expression_answer(received, expected, variable=variable)


def validate_antiderivative_equivalence(
    received: str | sp.Expr,
    expected: str | sp.Expr,
    *,
    variable: str = "x",
) -> AnswerCheck:
    """Validate antiderivatives up to an additive constant."""

    symbol = sp.Symbol(variable)
    try:
        received_expr = sp.sympify(received)
        expected_expr = sp.sympify(expected)
        difference_derivative = sp.diff(received_expr - expected_expr, symbol)
        correct = bool(sp.simplify(difference_derivative) == 0)
    except (TypeError, ValueError, sp.SympifyError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare antiderivatives: {error}",
        )

    message = "Correct." if correct else f"Expected an antiderivative of {expected}."
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message=message,
    )


def validate_limit_value(
    received: object,
    expected: object,
    *,
    tolerance: NumericTolerance = LIMIT_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric limit estimate."""

    try:
        return check_numeric_answer(
            float(cast(SupportsFloat, received)),
            float(cast(SupportsFloat, expected)),
            tolerance=tolerance,
        )
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare numeric limit: {error}",
        )


def validate_numeric_approximation(
    received: object,
    expected: object,
    *,
    tolerance: NumericTolerance = APPROXIMATION_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric approximation such as a Riemann sum."""

    return validate_limit_value(received, expected, tolerance=tolerance)


def validate_critical_point(
    received: object,
    expected: object,
    *,
    tolerance: NumericTolerance = CRITICAL_POINT_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric critical-point location."""

    return validate_limit_value(received, expected, tolerance=tolerance)


__all__ = [
    "validate_antiderivative_equivalence",
    "validate_critical_point",
    "validate_derivative_equivalence",
    "validate_limit_value",
    "validate_numeric_approximation",
]
