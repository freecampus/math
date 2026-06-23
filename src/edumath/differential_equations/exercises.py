"""Differential equations exercise builders."""

from __future__ import annotations

from random import Random
from typing import cast

import sympy as sp

from edumath.core import AnswerCheck, Exercise, check_expression_answer
from edumath.differential_equations.solvers import euler_method
from edumath.differential_equations.validators import validate_equilibrium

X = sp.Symbol("x")
Y = sp.Symbol("y")


def classify_ode_exercise(*, seed: int | None = None) -> Exercise:
    """Generate an ODE classification exercise."""

    rng = Random(seed)
    options = (
        ("dy/dx = x*y", "separable", "It has the product form g(x)h(y)."),
        ("dy/dx + 2*y = x", "linear", "It matches y' + p(x)y = q(x)."),
        ("dy/dx = y*(1-y)", "separable", "All y terms can be moved to one side."),
        (
            "dy/dx = x + y**2",
            "neither",
            "It is not linear and does not separate directly.",
        ),
    )
    prompt, expected, explanation = rng.choice(options)
    return Exercise(
        prompt=(
            f"Classify the equation `{prompt}` as separable, linear, both, or neither."
        ),
        expected=expected,
        validator=lambda received: _check_string(received, expected),
        explanation=explanation,
        tags=("differential-equations", "classification"),
        answer_type="multiple_choice",
    )


def separable_solution_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a separable exponential-growth or decay exercise."""

    rng = Random(seed)
    rate = rng.choice([-3, -2, -1, 1, 2, 3])
    initial = rng.randint(1, 5)
    expected = initial * sp.exp(rate * X)
    return Exercise(
        prompt=(f"Solve dy/dx = {rate}y with initial condition y(0) = {initial}."),
        expected=expected,
        validator=lambda received: check_expression_answer(
            cast(str | sp.Expr, received),
            expected,
        ),
        explanation="Separate variables to get y = C e^(kx), then use y(0).",
        tags=("differential-equations", "separable"),
        answer_type="symbolic",
    )


def linear_integrating_factor_exercise(*, seed: int | None = None) -> Exercise:
    """Generate an integrating-factor identification exercise."""

    rng = Random(seed)
    coefficient = rng.randint(1, 5)
    expected = sp.exp(coefficient * X)
    return Exercise(
        prompt=(f"Find the integrating factor for dy/dx + {coefficient}y = x."),
        expected=expected,
        validator=lambda received: check_expression_answer(
            cast(str | sp.Expr, received),
            expected,
        ),
        explanation="For y' + p(x)y = q(x), use mu(x)=e^(integral p(x) dx).",
        tags=("differential-equations", "linear", "integrating-factor"),
        answer_type="symbolic",
    )


def euler_step_exercise(*, seed: int | None = None) -> Exercise:
    """Generate one Euler-step exercise."""

    rng = Random(seed)
    rate = rng.randint(1, 4)
    initial_y = rng.randint(1, 5)
    step = rng.choice([0.1, 0.2, 0.5])
    expected = euler_method(
        lambda _x, y_value: rate * y_value,
        initial_x=0,
        initial_y=initial_y,
        step=step,
        steps=1,
    )[-1]
    return Exercise(
        prompt=(
            f"Use one Euler step for y'={rate}y, y(0)={initial_y}, "
            f"step h={step}. Give (x1, y1)."
        ),
        expected=expected,
        explanation="Euler uses y1 = y0 + h f(x0,y0) and x1 = x0 + h.",
        tags=("differential-equations", "euler-method"),
        answer_type="numeric",
    )


def equilibrium_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a one-dimensional equilibrium exercise."""

    rng = Random(seed)
    capacity = rng.randint(2, 8)
    rhs = Y * (capacity - Y)
    expected = (sp.Integer(0), sp.Integer(capacity))
    return Exercise(
        prompt=f"Find the equilibria of y' = {sp.sstr(rhs)}.",
        expected=expected,
        validator=lambda received: _check_equilibrium_tuple(received, rhs),
        explanation="Equilibria occur where the right-hand side equals zero.",
        tags=("differential-equations", "equilibria"),
        answer_type="exact",
    )


def system_equilibrium_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a simple system-equilibrium exercise."""

    rng = Random(seed)
    x_star = rng.randint(-3, 3)
    y_star = rng.randint(-3, 3)
    expected = (x_star, y_star)
    return Exercise(
        prompt=(
            f"Find the equilibrium of the system x' = {x_star} - x, y' = {y_star} - y."
        ),
        expected=expected,
        explanation="Set both derivatives equal to zero and solve simultaneously.",
        tags=("differential-equations", "systems", "equilibria"),
        answer_type="exact",
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


def _check_equilibrium_tuple(received: object, rhs: sp.Expr) -> AnswerCheck:
    if not isinstance(received, (tuple, list)):
        return AnswerCheck(
            correct=False,
            received=received,
            expected="tuple of equilibria",
            message="Enter the equilibrium values as a tuple or list.",
        )
    checks = [
        validate_equilibrium(value, rhs, variable="y").correct for value in received
    ]
    expected = tuple(sp.solve(sp.Eq(rhs, 0), Y))
    correct = all(checks) and len(received) == len(expected)
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


__all__ = [
    "classify_ode_exercise",
    "equilibrium_exercise",
    "euler_step_exercise",
    "linear_integrating_factor_exercise",
    "separable_solution_exercise",
    "system_equilibrium_exercise",
]
