"""College algebra concept metadata."""

from __future__ import annotations

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

EXPRESSIONS_AND_EQUATIONS = Lesson(
    title="Expressions and equations",
    slug="expressions-and-equations",
    objectives=(
        LearningObjective("Distinguish expressions from equations."),
        LearningObjective("Evaluate algebraic expressions by substitution."),
        LearningObjective("Solve one-variable linear equations."),
    ),
    sections=(
        LessonSection(
            title="Expressions",
            body=(
                "An expression is a mathematical phrase that can be simplified "
                "or evaluated, such as 3*x + 2."
            ),
        ),
        LessonSection(
            title="Equations",
            body=(
                "An equation states that two expressions are equal. Solving an "
                "equation means finding values that make the statement true."
            ),
        ),
    ),
    tags=("algebra", "equations"),
)

FUNCTIONS_AND_GRAPHS = Lesson(
    title="Functions and graphs",
    slug="functions-and-graphs",
    objectives=(
        LearningObjective("Interpret a function as an input-output rule."),
        LearningObjective("Identify slope, intercepts, domain, and range."),
        LearningObjective("Connect symbolic functions to their graphs."),
    ),
    sections=(
        LessonSection(
            title="Functions",
            body="A function assigns each input exactly one output.",
        ),
        LessonSection(
            title="Graphs",
            body=("A graph shows the ordered pairs (x, f(x)) produced by a function."),
        ),
    ),
    tags=("algebra", "functions", "graphs"),
)

POLYNOMIALS = Lesson(
    title="Polynomials",
    slug="polynomials",
    objectives=(
        LearningObjective("Recognize polynomial degree and leading coefficient."),
        LearningObjective("Factor common polynomial forms."),
        LearningObjective("Use roots to interpret polynomial graphs."),
    ),
    sections=(
        LessonSection(
            title="Polynomial structure",
            body=(
                "A polynomial is a sum of constant multiples of non-negative "
                "integer powers of a variable."
            ),
        ),
    ),
    tags=("algebra", "polynomials"),
)

EXPONENTIALS_AND_LOGARITHMS = Lesson(
    title="Exponentials and logarithms",
    slug="exponentials-and-logarithms",
    objectives=(
        LearningObjective("Recognize exponential growth and decay."),
        LearningObjective("Use logarithms as inverse operations for exponentials."),
        LearningObjective("Solve basic exponential and logarithmic equations."),
    ),
    sections=(
        LessonSection(
            title="Inverse relationship",
            body="A logarithm answers the question: what exponent produced this value?",
        ),
    ),
    tags=("algebra", "exponentials", "logarithms"),
)

SYSTEMS_OF_EQUATIONS = Lesson(
    title="Systems of equations",
    slug="systems-of-equations",
    objectives=(
        LearningObjective("Interpret a solution as a point satisfying all equations."),
        LearningObjective("Solve small linear systems by substitution or elimination."),
        LearningObjective("Connect systems to line intersections."),
    ),
    sections=(
        LessonSection(
            title="Shared solutions",
            body=(
                "A system asks for values that make every equation true at the "
                "same time."
            ),
        ),
    ),
    tags=("algebra", "systems"),
)

COLLEGE_ALGEBRA_PATH = StudyPath(
    title="College Algebra",
    lessons=(
        EXPRESSIONS_AND_EQUATIONS,
        FUNCTIONS_AND_GRAPHS,
        POLYNOMIALS,
        EXPONENTIALS_AND_LOGARITHMS,
        SYSTEMS_OF_EQUATIONS,
    ),
)


__all__ = [
    "COLLEGE_ALGEBRA_PATH",
    "EXPONENTIALS_AND_LOGARITHMS",
    "EXPRESSIONS_AND_EQUATIONS",
    "FUNCTIONS_AND_GRAPHS",
    "POLYNOMIALS",
    "SYSTEMS_OF_EQUATIONS",
]
