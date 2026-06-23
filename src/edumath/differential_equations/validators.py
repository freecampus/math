"""Answer validators for differential equations lessons."""

from __future__ import annotations

from collections.abc import Sequence
from typing import SupportsFloat, cast

import sympy as sp

from edumath.core import AnswerCheck, NumericTolerance, check_numeric_answer
from edumath.core.expressions import parse_expression

ODE_TOLERANCE = NumericTolerance(absolute=1e-6, relative=1e-6)
TRAJECTORY_TOLERANCE = NumericTolerance(absolute=1e-5, relative=1e-5)


def validate_solution_satisfies_ode(
    candidate: str | sp.Expr,
    ode_rhs: str | sp.Expr,
    *,
    variable: str = "x",
    function_name: str = "y",
) -> AnswerCheck:
    """Validate that ``candidate`` satisfies ``dy/dx = ode_rhs``."""

    x_symbol = sp.Symbol(variable)
    y_symbol = sp.Symbol(function_name)
    try:
        candidate_expr = parse_expression(candidate, variables=(x_symbol,))
        rhs_expr = parse_expression(ode_rhs, variables=(x_symbol, y_symbol))
        residual = sp.simplify(
            sp.diff(candidate_expr, x_symbol) - rhs_expr.subs(y_symbol, candidate_expr)
        )
        correct = bool(residual == 0)
    except (TypeError, ValueError, sp.SympifyError) as error:
        return AnswerCheck(
            correct=False,
            received=candidate,
            expected=ode_rhs,
            message=f"Could not verify the differential equation: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=candidate,
        expected=ode_rhs,
        message="Correct." if correct else f"The residual simplifies to {residual}.",
    )


def validate_initial_condition(
    candidate: str | sp.Expr,
    *,
    x0: object,
    y0: object,
    variable: str = "x",
    tolerance: NumericTolerance = ODE_TOLERANCE,
) -> AnswerCheck:
    """Validate that a candidate solution satisfies ``y(x0)=y0``."""

    symbol = sp.Symbol(variable)
    try:
        expr = parse_expression(candidate, variables=(symbol,))
        received_value = float(expr.subs(symbol, x0))
        expected_value = float(cast(SupportsFloat, y0))
        return check_numeric_answer(
            received_value,
            expected_value,
            tolerance=tolerance,
        )
    except (TypeError, ValueError, sp.SympifyError) as error:
        return AnswerCheck(
            correct=False,
            received=candidate,
            expected=y0,
            message=f"Could not check the initial condition: {error}",
        )


def validate_numeric_trajectory(
    received: Sequence[Sequence[object]],
    expected: Sequence[Sequence[object]],
    *,
    tolerance: NumericTolerance = TRAJECTORY_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric trajectory such as Euler-method points."""

    if len(received) != len(expected):
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Expected {len(expected)} points, received {len(received)}.",
        )

    for point_index, (received_point, expected_point) in enumerate(
        zip(received, expected, strict=True),
        start=1,
    ):
        if len(received_point) != len(expected_point):
            return AnswerCheck(
                correct=False,
                received=received,
                expected=expected,
                message=f"Point {point_index} has the wrong dimension.",
            )
        for coordinate_index, (received_value, expected_value) in enumerate(
            zip(received_point, expected_point, strict=True),
            start=1,
        ):
            check = check_numeric_answer(
                float(cast(SupportsFloat, received_value)),
                float(cast(SupportsFloat, expected_value)),
                tolerance=tolerance,
            )
            if not check.correct:
                return AnswerCheck(
                    correct=False,
                    received=received,
                    expected=expected,
                    message=(
                        f"Point {point_index}, coordinate {coordinate_index}: "
                        f"{check.message}"
                    ),
                )

    return AnswerCheck(
        correct=True,
        received=received,
        expected=expected,
        message="Correct.",
    )


def validate_equilibrium(
    candidate: object,
    rhs: str | sp.Expr,
    *,
    variable: str = "y",
) -> AnswerCheck:
    """Validate an equilibrium value for an autonomous equation ``y'=f(y)``."""

    symbol = sp.Symbol(variable)
    try:
        value = sp.sympify(candidate)
        rhs_expr = parse_expression(rhs, variables=(symbol,))
        residual = sp.simplify(rhs_expr.subs(symbol, value))
        correct = bool(residual == 0)
    except (TypeError, ValueError, sp.SympifyError) as error:
        return AnswerCheck(
            correct=False,
            received=candidate,
            expected=rhs,
            message=f"Could not check equilibrium: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=candidate,
        expected=rhs,
        message="Correct." if correct else f"Substitution gives {residual}, not 0.",
    )


__all__ = [
    "ODE_TOLERANCE",
    "TRAJECTORY_TOLERANCE",
    "validate_equilibrium",
    "validate_initial_condition",
    "validate_numeric_trajectory",
    "validate_solution_satisfies_ode",
]
