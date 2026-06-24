"""Calculus answer validators."""

from __future__ import annotations

from typing import SupportsFloat, cast

import sympy as sp

from edumath.calculus.derivatives import tangent_line
from edumath.calculus.steps import parse_point_list
from edumath.core import (
    AnswerCheck,
    NumericTolerance,
    check_expression_answer,
    check_numeric_answer,
    parse_expression,
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


def validate_limit_answer(
    received: object,
    expression: str | sp.Expr,
    point: object,
    *,
    direction: str | None = None,
    variable: str = "x",
) -> AnswerCheck:
    """Validate a limit answer for an expression at a point."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    try:
        if direction is None:
            expected = sp.limit(expr, symbol, point)
        else:
            expected = sp.limit(expr, symbol, point, dir=direction)
        received_expr = sp.sympify(received)
        if expected in {sp.oo, -sp.oo, sp.zoo}:
            correct = bool(received_expr == expected)
        else:
            correct = bool(sp.simplify(received_expr - expected) == 0)
    except (TypeError, ValueError, sp.SympifyError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expression,
            message=f"Could not compare limit answer: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected limit {expected}.",
    )


def validate_tangent_line(
    received: str | sp.Expr,
    expression: str | sp.Expr,
    point: float,
    *,
    variable: str = "x",
) -> AnswerCheck:
    """Validate a tangent-line equation written as an expression in x."""

    expected = tangent_line(expression, point, variable=variable)
    return check_expression_answer(received, expected, variable=variable)


def validate_critical_points(
    received: object,
    expression: str | sp.Expr,
    *,
    variable: str = "x",
) -> AnswerCheck:
    """Validate the critical points where f'(x)=0 for a differentiable expression."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    expected = tuple(sp.solve(sp.Eq(sp.diff(expr, symbol), 0), symbol))
    try:
        received_points = parse_point_list(received)
        correct = _same_symbolic_set(received_points, expected)
    except (TypeError, ValueError, sp.SympifyError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare critical points: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected critical point(s) {expected}.",
    )


def _same_symbolic_set(left: tuple[sp.Expr, ...], right: tuple[object, ...]) -> bool:
    if len(left) != len(right):
        return False
    unmatched = [sp.sympify(value) for value in right]
    for candidate in left:
        for index, expected in enumerate(unmatched):
            if sp.simplify(candidate - expected) == 0:
                unmatched.pop(index)
                break
        else:
            return False
    return not unmatched


__all__ = [
    "validate_antiderivative_equivalence",
    "validate_critical_point",
    "validate_critical_points",
    "validate_derivative_equivalence",
    "validate_limit_answer",
    "validate_limit_value",
    "validate_numeric_approximation",
    "validate_tangent_line",
]
