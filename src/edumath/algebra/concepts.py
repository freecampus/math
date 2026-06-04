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

INEQUALITIES_AND_ABSOLUTE_VALUE = Lesson(
    title="Inequalities and absolute value",
    slug="inequalities-and-absolute-value",
    objectives=(
        LearningObjective("Solve linear and compound inequalities."),
        LearningObjective("Interpret interval notation and number-line graphs."),
        LearningObjective("Use absolute value as a distance from a center."),
    ),
    sections=(
        LessonSection(
            title="Intervals and constraints",
            body=(
                "Inequalities describe sets of allowed values instead of one "
                "single solution."
            ),
        ),
        LessonSection(
            title="Distance interpretation",
            body="The expression |x - a| measures the distance from x to a.",
        ),
    ),
    tags=("algebra", "inequalities", "absolute-value"),
)

TRANSFORMATIONS_COMPOSITION_INVERSES = Lesson(
    title="Transformations, composition, and inverses",
    slug="transformations-composition-inverses",
    objectives=(
        LearningObjective("Describe shifts, stretches, and reflections of graphs."),
        LearningObjective("Compose functions and track domains."),
        LearningObjective("Interpret inverse functions as reversing a rule."),
    ),
    sections=(
        LessonSection(
            title="Transformations",
            body="Parameters in a formula move, stretch, compress, or reflect graphs.",
        ),
        LessonSection(
            title="Composition and inverses",
            body=(
                "Composition chains functions together; inverse functions undo "
                "a previous function when that reversal is well-defined."
            ),
        ),
    ),
    tags=("algebra", "functions", "transformations", "inverses"),
)

LINEAR_AND_QUADRATIC_FUNCTIONS = Lesson(
    title="Linear and quadratic functions",
    slug="linear-and-quadratic-functions",
    objectives=(
        LearningObjective("Interpret slope and intercepts in linear functions."),
        LearningObjective("Move among standard, factored, and vertex quadratic forms."),
        LearningObjective("Use discriminants, roots, and vertices to read graphs."),
    ),
    sections=(
        LessonSection(
            title="Linear models",
            body="A line models constant rate of change.",
        ),
        LessonSection(
            title="Quadratic models",
            body=(
                "A quadratic models a changing rate of change and graphs as a parabola."
            ),
        ),
    ),
    tags=("algebra", "linear-functions", "quadratics"),
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
        INEQUALITIES_AND_ABSOLUTE_VALUE,
        FUNCTIONS_AND_GRAPHS,
        TRANSFORMATIONS_COMPOSITION_INVERSES,
        LINEAR_AND_QUADRATIC_FUNCTIONS,
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
    "INEQUALITIES_AND_ABSOLUTE_VALUE",
    "LINEAR_AND_QUADRATIC_FUNCTIONS",
    "POLYNOMIALS",
    "SYSTEMS_OF_EQUATIONS",
    "TRANSFORMATIONS_COMPOSITION_INVERSES",
]
