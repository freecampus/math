"""Quiz helpers for differential equations lessons."""

from __future__ import annotations

import sympy as sp

from edumath.core import AnswerOption, Question, QuizSession
from edumath.differential_equations.solvers import euler_method
from edumath.differential_equations.validators import (
    validate_equilibrium,
    validate_solution_satisfies_ode,
)


def classify_ode_question() -> Question:
    """Create a multiple-choice ODE classification question."""

    return Question(
        prompt="Classify `dy/dx = x*y`.",
        expected="separable",
        options=(
            AnswerOption("Separable", "separable"),
            AnswerOption("Linear only", "linear"),
            AnswerOption("Neither", "neither"),
        ),
        explanation="It can be rearranged as (1/y) dy = x dx.",
        tags=("differential-equations", "classification"),
    )


def initial_condition_question() -> Question:
    """Create a question about the meaning of an initial condition."""

    return Question(
        prompt="What does `y(0)=5` tell you?",
        expected="starting value",
        options=(
            AnswerOption("The starting value is 5 when x=0", "starting value"),
            AnswerOption("The derivative is 5", "derivative"),
            AnswerOption("Every solution equals 5", "all values"),
        ),
        explanation="An initial condition selects one curve from a solution family.",
        tags=("differential-equations", "initial-conditions"),
    )


def solution_verification_question() -> Question:
    """Create a symbolic solution-verification question."""

    expected = sp.exp(2 * sp.Symbol("x"))
    return Question(
        prompt="Give a solution of `dy/dx = 2y` with `y(0)=1`.",
        expected=expected,
        answer_type="symbolic",
        validator=lambda received: validate_solution_satisfies_ode(received, "2*y"),
        explanation="The family is C e^(2x), and y(0)=1 gives C=1.",
        tags=("differential-equations", "verification"),
    )


def euler_step_question() -> Question:
    """Create a one-step Euler method question."""

    expected = euler_method(
        lambda _x, y_value: y_value,
        initial_x=0,
        initial_y=2,
        step=0.5,
        steps=1,
    )[-1]
    return Question(
        prompt="Use one Euler step for `y'=y`, `y(0)=2`, `h=0.5`. What is `(x1,y1)`?",
        expected=expected,
        explanation="x increases by h and y increases by h times the current slope.",
        tags=("differential-equations", "euler-method"),
    )


def equilibrium_question() -> Question:
    """Create a one-dimensional equilibrium question."""

    return Question(
        prompt="Which value is an equilibrium for `y' = y(3-y)`?",
        expected="3",
        options=(
            AnswerOption("3", "3"),
            AnswerOption("1", "1"),
            AnswerOption("-3", "-3"),
        ),
        validator=lambda received: validate_equilibrium(received, "y*(3-y)"),
        explanation="Equilibria occur where y(3-y)=0, so y=0 or y=3.",
        tags=("differential-equations", "equilibria"),
    )


def slope_field_behavior_question() -> Question:
    """Create a slope-field interpretation question."""

    return Question(
        prompt="In a slope field, what does a horizontal segment mean?",
        expected="zero derivative",
        options=(
            AnswerOption("The derivative is zero", "zero derivative"),
            AnswerOption("The solution is undefined", "undefined"),
            AnswerOption("The x-value is zero", "x zero"),
        ),
        explanation="Horizontal means slope 0 at that point.",
        tags=("differential-equations", "slope-fields"),
    )


def differential_equations_diagnostic_quiz() -> QuizSession:
    """Return a short differential equations diagnostic quiz."""

    return QuizSession(
        questions=(
            classify_ode_question(),
            initial_condition_question(),
            slope_field_behavior_question(),
            equilibrium_question(),
        )
    )


__all__ = [
    "classify_ode_question",
    "differential_equations_diagnostic_quiz",
    "equilibrium_question",
    "euler_step_question",
    "initial_condition_question",
    "slope_field_behavior_question",
    "solution_verification_question",
]
