"""College algebra exercise builders."""

from __future__ import annotations

from random import Random
from typing import SupportsFloat, cast

import sympy as sp

from edumath.core import (
    AnswerCheck,
    Exercise,
    check_expression_answer,
    check_numeric_answer,
)


def linear_equation_exercise(
    *,
    seed: int | None = None,
) -> Exercise:
    """Generate a one-variable linear equation exercise."""

    rng = Random(seed)
    x = sp.Symbol("x")
    solution = rng.randint(-8, 8)
    coefficient = _nonzero_int(rng, -6, 6)
    constant = rng.randint(-10, 10)
    equation = sp.Eq(coefficient * x + constant, coefficient * solution + constant)
    expected = float(solution)

    def validator(received: object) -> AnswerCheck:
        return check_numeric_answer(float(cast(SupportsFloat, received)), expected)

    return Exercise(
        prompt=f"Solve for x: {sp.sstr(equation)}",
        expected=expected,
        validator=validator,
        explanation=(
            "Undo the addition/subtraction first, then divide by the coefficient of x."
        ),
        tags=("algebra", "linear-equations"),
    )


def expand_expression_exercise(
    *,
    seed: int | None = None,
) -> Exercise:
    """Generate a polynomial expansion exercise."""

    rng = Random(seed)
    x = sp.Symbol("x")
    a = _nonzero_int(rng, -5, 5)
    b = rng.randint(-6, 6)
    expression = (x + a) * (x + b)
    expected = sp.expand(expression)

    return Exercise(
        prompt=f"Expand: {sp.sstr(expression)}",
        expected=expected,
        validator=lambda received: check_expression_answer(
            str(received),
            expected,
        ),
        explanation=(
            "Use distribution: multiply each term in the first factor by each "
            "term in the second."
        ),
        tags=("algebra", "polynomials"),
    )


def _nonzero_int(rng: Random, start: int, stop: int) -> int:
    value = 0
    while value == 0:
        value = rng.randint(start, stop)
    return value


__all__ = ["expand_expression_exercise", "linear_equation_exercise"]
