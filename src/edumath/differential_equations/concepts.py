"""Differential equations concept metadata."""

from __future__ import annotations

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

FIRST_ORDER_EQUATIONS = Lesson(
    title="First-order differential equations",
    slug="first-order-equations",
    objectives=(
        LearningObjective("Recognize first-order differential equations."),
        LearningObjective("Interpret derivatives as dynamic change rules."),
        LearningObjective("Verify candidate solutions by substitution."),
    ),
    sections=(
        LessonSection(
            title="Rules for change",
            body=(
                "A first-order ODE relates an unknown function to its first derivative."
            ),
        ),
    ),
    prerequisites=("derivatives", "function notation", "units"),
    summary="First-order ODEs describe how one quantity changes.",
    tags=("differential-equations", "first-order"),
)

SEPARABLE_EQUATIONS = Lesson(
    title="Separable equations",
    slug="separable-equations",
    objectives=(
        LearningObjective("Recognize separable differential equations."),
        LearningObjective("Separate variables and integrate both sides."),
        LearningObjective("Use initial conditions to choose one solution."),
    ),
    sections=(
        LessonSection(
            title="Separate and integrate",
            body="A separable ODE can be rearranged so y terms and x terms separate.",
        ),
    ),
    prerequisites=("integration", "logarithms", "algebraic rearrangement"),
    summary="Separable equations are solved by moving variables apart and integrating.",
    tags=("differential-equations", "separable"),
)

LINEAR_EQUATIONS = Lesson(
    title="Linear differential equations",
    slug="linear-equations",
    objectives=(
        LearningObjective("Recognize standard linear form."),
        LearningObjective("Compute and use an integrating factor."),
        LearningObjective("Interpret forcing and proportional feedback terms."),
    ),
    sections=(
        LessonSection(
            title="Integrating factors",
            body=(
                "A first-order linear ODE uses an integrating factor to turn "
                "the left side into a product derivative."
            ),
        ),
    ),
    prerequisites=("product rule", "antiderivatives", "exponentials"),
    summary="Linear ODEs have a systematic symbolic solution method.",
    tags=("differential-equations", "linear"),
)

SLOPE_FIELDS = Lesson(
    title="Slope fields",
    slug="slope-fields",
    objectives=(
        LearningObjective("Read a slope field as local derivative information."),
        LearningObjective("Use Euler's method for approximate solutions."),
        LearningObjective("Identify equilibria from direction information."),
    ),
    sections=(
        LessonSection(
            title="Visual change",
            body="A slope field shows the derivative predicted at many points.",
        ),
    ),
    prerequisites=("graph reading", "derivative meaning", "arithmetic"),
    summary="Slope fields and Euler's method help study ODEs without exact formulas.",
    tags=("differential-equations", "slope-fields", "numerical"),
)

SYSTEMS = Lesson(
    title="Systems of differential equations",
    slug="systems",
    objectives=(
        LearningObjective("Recognize coupled differential equations."),
        LearningObjective(
            "Find equilibrium points by setting all derivatives to zero."
        ),
        LearningObjective("Connect linear systems to matrix notation."),
    ),
    sections=(
        LessonSection(
            title="Coupled change",
            body=(
                "A system tracks several quantities whose rates may affect each other."
            ),
        ),
    ),
    prerequisites=("systems of equations", "vectors", "basic matrices"),
    summary="Systems model several changing quantities at the same time.",
    tags=("differential-equations", "systems"),
)

DIFFERENTIAL_EQUATIONS_PATH = StudyPath(
    title="Differential Equations",
    lessons=(
        FIRST_ORDER_EQUATIONS,
        SEPARABLE_EQUATIONS,
        LINEAR_EQUATIONS,
        SLOPE_FIELDS,
        SYSTEMS,
    ),
)

__all__ = [
    "DIFFERENTIAL_EQUATIONS_PATH",
    "FIRST_ORDER_EQUATIONS",
    "LINEAR_EQUATIONS",
    "SEPARABLE_EQUATIONS",
    "SLOPE_FIELDS",
    "SYSTEMS",
]
