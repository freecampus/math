"""Calculus quiz helpers."""

from __future__ import annotations

import sympy as sp

from edumath.calculus.derivatives import derivative
from edumath.calculus.integrals import antiderivative, definite_integral
from edumath.calculus.validators import (
    validate_antiderivative_equivalence,
    validate_derivative_equivalence,
    validate_numeric_approximation,
)
from edumath.core import AnswerOption, Question, QuizSession, SympyResolver


def derivative_question(
    expression: object,
    *,
    prompt: str | None = None,
    variable: str = "x",
) -> Question:
    """Create an auto-checkable derivative question."""

    expected = derivative(str(expression), variable=variable)
    return Question(
        prompt=prompt or f"Differentiate `{expression}`.",
        expected=expected,
        answer_type="symbolic",
        validator=lambda received: validate_derivative_equivalence(
            str(received),
            expected,
            variable=variable,
        ),
        tags=("calculus", "derivatives"),
    )


def antiderivative_question(
    expression: object,
    *,
    prompt: str | None = None,
    variable: str = "x",
) -> Question:
    """Create an auto-checkable antiderivative question."""

    expected = antiderivative(str(expression), variable=variable)
    return Question(
        prompt=prompt or f"Find an antiderivative of `{expression}`.",
        expected=expected,
        answer_type="symbolic",
        validator=lambda received: validate_antiderivative_equivalence(
            str(received),
            expected,
            variable=variable,
        ),
        tags=("calculus", "integrals"),
    )


def definite_integral_question(
    expression: object,
    lower: float,
    upper: float,
    *,
    prompt: str | None = None,
    variable: str = "x",
) -> Question:
    """Create an auto-checkable definite-integral question."""

    expected = definite_integral(str(expression), lower, upper, variable=variable)
    return Question(
        prompt=prompt
        or f"Compute the integral of `{expression}` from {lower} to {upper}.",
        expected=expected,
        answer_type="numeric",
        validator=lambda received: validate_numeric_approximation(received, expected),
        tags=("calculus", "integrals"),
    )


def optimization_question(
    expression: object,
    *,
    variable: str = "x",
) -> Question:
    """Create a question asking for critical points of an expression."""

    symbol = sp.Symbol(variable)
    expr = sp.sympify(expression)
    expected = tuple(sp.solve(sp.Eq(sp.diff(expr, symbol), 0), symbol))
    return Question(
        prompt=f"Find the critical point(s) of `{expression}`.",
        expected=expected,
        answer_type="exact",
        tags=("calculus", "optimization"),
        explanation="Critical points occur where the derivative is zero or undefined.",
    )


def calculus_tool_question() -> Question:
    """Create a multiple-choice question about choosing a calculus tool."""

    return Question(
        prompt="Which tool finds total distance from a velocity function over time?",
        expected="integral",
        options=(
            AnswerOption("Derivative", "derivative"),
            AnswerOption("Integral", "integral"),
            AnswerOption("Tangent line", "tangent"),
        ),
        explanation=(
            "Distance accumulates velocity over an interval, so use an integral."
        ),
        tags=("calculus", "applications"),
    )


def calculus_diagnostic_quiz() -> QuizSession:
    """Return a short calculus diagnostic quiz."""

    return QuizSession(
        questions=(
            Question(
                "Evaluate lim as x -> 2 of x + 3.",
                expression="x + 3",
                resolver=SympyResolver("limit", point=2),
                answer_type="numeric",
            ),
            derivative_question("x**2"),
            antiderivative_question("2*x"),
            calculus_tool_question(),
        )
    )


__all__ = [
    "antiderivative_question",
    "calculus_diagnostic_quiz",
    "calculus_tool_question",
    "definite_integral_question",
    "derivative_question",
    "optimization_question",
]
