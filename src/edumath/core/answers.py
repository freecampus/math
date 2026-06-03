"""Reusable answer checking helpers for quizzes and exercises."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from edumath.core.expressions import expression_equivalent


@dataclass(frozen=True)
class AnswerCheck:
    """Result of checking one learner answer."""

    correct: bool
    received: object
    expected: object
    message: str = ""


@dataclass(frozen=True)
class NumericTolerance:
    """Absolute and relative tolerance for numeric answers."""

    absolute: float = 1e-9
    relative: float = 1e-9


DEFAULT_NUMERIC_TOLERANCE = NumericTolerance()


def check_numeric_answer(
    received: float,
    expected: float,
    *,
    tolerance: NumericTolerance = DEFAULT_NUMERIC_TOLERANCE,
) -> AnswerCheck:
    """Check a numeric answer with absolute and relative tolerances."""

    difference = abs(received - expected)
    scale = max(abs(received), abs(expected), 1.0)
    correct = difference <= max(tolerance.absolute, tolerance.relative * scale)
    message = "Correct." if correct else f"Expected {expected}, received {received}."
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message=message,
    )


def check_expression_answer(
    received: str | sp.Expr,
    expected: str | sp.Expr,
    *,
    variable: str = "x",
) -> AnswerCheck:
    """Check whether two symbolic expressions are equivalent."""

    symbol = sp.Symbol(variable)
    correct = expression_equivalent(
        received,
        expected,
        variables=(symbol,),
    )
    message = (
        "Correct." if correct else f"Expected an expression equivalent to {expected}."
    )
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message=message,
    )
