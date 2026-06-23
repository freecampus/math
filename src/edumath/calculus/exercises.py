"""Calculus exercise builders."""

from __future__ import annotations

from random import Random
from typing import SupportsFloat, cast

import sympy as sp

from edumath.calculus.derivatives import derivative, tangent_line
from edumath.calculus.integrals import midpoint_riemann_sum
from edumath.calculus.validators import (
    validate_critical_point,
    validate_derivative_equivalence,
    validate_numeric_approximation,
)
from edumath.core import (
    AnswerCheck,
    Exercise,
    check_expression_answer,
    check_numeric_answer,
)

X = sp.Symbol("x")


def tangent_line_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a tangent-line exercise for a quadratic."""

    rng = Random(seed)
    point = rng.randint(-3, 3)
    expression = X**2 + rng.randint(-3, 3) * X
    expected = tangent_line(expression, point)
    return Exercise(
        prompt=f"Find the tangent line to f(x) = {sp.sstr(expression)} at x = {point}.",
        expected=expected,
        validator=lambda received: check_expression_answer(
            cast(str | sp.Expr, received),
            expected,
        ),
        explanation="Differentiate to find the slope, then use point-slope form.",
        tags=("calculus", "derivatives", "tangent-lines"),
        answer_type="symbolic",
    )


def derivative_rule_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a derivative practice exercise."""

    rng = Random(seed)
    exponent = rng.randint(2, 6)
    coefficient = rng.randint(1, 5)
    expression = coefficient * X**exponent
    expected = derivative(expression)
    return Exercise(
        prompt=f"Differentiate: {sp.sstr(expression)}.",
        expected=expected,
        validator=lambda received: validate_derivative_equivalence(
            cast(str | sp.Expr, received),
            expected,
        ),
        explanation="Use the constant multiple rule and the power rule.",
        tags=("calculus", "derivative-rules"),
        answer_type="symbolic",
    )


def critical_point_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a quadratic critical-point exercise."""

    rng = Random(seed)
    critical = rng.randint(-5, 5)
    expression = (X - critical) ** 2 + rng.randint(-4, 4)
    expected = float(critical)
    return Exercise(
        prompt=f"Find the critical point of f(x) = {sp.sstr(sp.expand(expression))}.",
        expected=expected,
        validator=lambda received: validate_critical_point(received, expected),
        explanation="Set the derivative equal to zero and solve for x.",
        tags=("calculus", "optimization"),
        answer_type="numeric",
    )


def riemann_sum_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a midpoint Riemann-sum approximation exercise."""

    rng = Random(seed)
    rectangles = rng.choice([4, 5, 10])
    expected = midpoint_riemann_sum("x**2", 0, 1, rectangles)
    return Exercise(
        prompt=(
            "Approximate the integral of x^2 from 0 to 1 using "
            f"{rectangles} midpoint rectangles."
        ),
        expected=expected,
        validator=lambda received: validate_numeric_approximation(received, expected),
        explanation="Use midpoint rectangles with equal width on [0, 1].",
        tags=("calculus", "integrals", "riemann-sums"),
        answer_type="numeric",
    )


def tool_choice_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a derivative/integral/optimization tool-choice exercise."""

    rng = Random(seed)
    options = (
        (
            "A problem asks for marginal cost at a production level.",
            "derivative",
            "Marginal means local rate of change.",
        ),
        (
            "A problem asks for total distance from a velocity graph.",
            "integral",
            "Total distance accumulates rate over time.",
        ),
        (
            "A problem asks for the maximum profit.",
            "optimization",
            "Best-value questions use an optimization workflow.",
        ),
    )
    prompt, expected, explanation = rng.choice(options)
    return Exercise(
        prompt=prompt,
        expected=expected,
        validator=lambda received: _check_string(received, expected),
        explanation=explanation,
        tags=("calculus", "applications"),
        answer_type="multiple_choice",
    )


def limit_estimate_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a simple limit-estimate exercise."""

    rng = Random(seed)
    point = rng.randint(-3, 3)
    expression = X + rng.randint(-5, 5)
    expected = float(expression.subs(X, point))
    return Exercise(
        prompt=f"Estimate lim as x -> {point} of {sp.sstr(expression)}.",
        expected=expected,
        validator=lambda received: check_numeric_answer(
            float(cast(SupportsFloat, received)),
            expected,
        ),
        explanation="For a continuous linear function, substitute the target value.",
        tags=("calculus", "limits"),
        answer_type="numeric",
    )


def _check_string(received: object, expected: str) -> AnswerCheck:
    normalized = str(received).strip().lower()
    correct = normalized == expected
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


__all__ = [
    "critical_point_exercise",
    "derivative_rule_exercise",
    "limit_estimate_exercise",
    "riemann_sum_exercise",
    "tangent_line_exercise",
    "tool_choice_exercise",
]
