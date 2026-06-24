"""Deterministic exercise builders for linear algebra lessons."""

from __future__ import annotations

from random import Random

from edumath.core import AnswerCheck, Exercise
from edumath.linear_algebra.concepts import (
    dot_product,
    matrix_shape,
    matrix_vector_product,
    solve_linear_system,
    vector_norm,
)
from edumath.linear_algebra.validators import (
    validate_eigenpair,
    validate_scalar_answer,
    validate_shape_answer,
    validate_solution_vector,
    validate_vector_answer,
)


def vector_norm_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a vector-norm exercise with a Pythagorean-style vector."""

    rng = Random(seed)
    vectors = ((3, 4), (5, 12), (8, 15), (7, 24), (6, 8))
    vector = rng.choice(vectors)
    expected = vector_norm(vector)
    return Exercise(
        prompt=f"Find the length of the vector {list(vector)}.",
        expected=expected,
        validator=lambda received: validate_scalar_answer(received, expected),
        hint="Square each coordinate, add, and take the square root.",
        explanation="Use ||v|| = sqrt(v1^2 + v2^2).",
        tags=("linear-algebra", "vectors", "norm"),
        exercise_id="linear-algebra-vector-norm",
        answer_type="numeric",
    )


def dot_product_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a dot-product exercise."""

    rng = Random(seed)
    left = (rng.randint(-4, 4), rng.randint(-4, 4))
    right = (rng.randint(-4, 4), rng.randint(-4, 4))
    expected = dot_product(left, right)
    return Exercise(
        prompt=f"Compute the dot product {list(left)} · {list(right)}.",
        expected=expected,
        validator=lambda received: validate_scalar_answer(received, expected),
        hint="Multiply matching coordinates, then add the products.",
        explanation="The dot product is a1*b1 + a2*b2.",
        tags=("linear-algebra", "vectors", "dot-product"),
        exercise_id="linear-algebra-dot-product",
        answer_type="numeric",
    )


def matrix_shape_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a matrix-shape exercise."""

    rng = Random(seed)
    rows = rng.randint(2, 4)
    columns = rng.randint(2, 5)
    matrix = [
        [row * columns + column + 1 for column in range(columns)] for row in range(rows)
    ]
    expected = matrix_shape(matrix)
    return Exercise(
        prompt=f"What is the shape of the matrix {matrix}? Give rows by columns.",
        expected=expected,
        validator=lambda received: validate_shape_answer(received, expected),
        hint="Count rows first, then columns.",
        explanation="Matrix shape is always written as rows by columns.",
        tags=("linear-algebra", "matrices", "shape"),
        exercise_id="linear-algebra-matrix-shape",
        answer_type="exact",
    )


def matrix_vector_product_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a matrix-vector product exercise."""

    rng = Random(seed)
    matrix = [[rng.randint(-3, 4), rng.randint(-3, 4)] for _ in range(2)]
    vector = [rng.randint(-3, 4), rng.randint(-3, 4)]
    expected = matrix_vector_product(matrix, vector)
    return Exercise(
        prompt=f"Compute {matrix} times {vector}.",
        expected=expected.tolist(),
        validator=lambda received: validate_vector_answer(received, expected),
        hint="Each output entry is a row dot the input vector.",
        explanation="Multiply each row of the matrix by the vector and add.",
        tags=("linear-algebra", "matrix-operations", "matrix-vector-product"),
        exercise_id="linear-algebra-matrix-vector-product",
        answer_type="exact",
    )


def linear_system_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a 2-by-2 linear-system exercise with an integer solution."""

    rng = Random(seed)
    cases = (
        ([[1, 1], [1, -1]], [5, 1]),
        ([[2, 1], [1, -1]], [7, 1]),
        ([[1, 2], [3, -1]], [8, 3]),
        ([[2, -1], [1, 1]], [1, 5]),
    )
    matrix, values = rng.choice(cases)
    expected = solve_linear_system(matrix, values)
    return Exercise(
        prompt=f"Solve A x = b for A = {matrix} and b = {values}.",
        expected=expected.tolist(),
        validator=lambda received: validate_solution_vector(received, matrix, values),
        hint="Use elimination or solve the two equations by substitution.",
        explanation="Check a solution by substituting it back into every equation.",
        tags=("linear-algebra", "systems", "elimination"),
        exercise_id="linear-algebra-linear-system",
        answer_type="exact",
        difficulty="guided",
    )


def transformation_classification_exercise(*, seed: int | None = None) -> Exercise:
    """Generate a matrix-transformation classification exercise."""

    rng = Random(seed)
    options = (
        ([[2, 0], [0, 2]], "scaling", "Both coordinate directions are doubled."),
        ([[1, 0], [0, -1]], "reflection", "The y-coordinate changes sign."),
        ([[1, 1], [0, 1]], "shear", "The x-coordinate receives some of y."),
        ([[1, 0], [0, 0]], "projection", "The y-coordinate becomes zero."),
    )
    matrix, expected, explanation = rng.choice(options)
    return Exercise(
        prompt=f"Classify the transformation represented by {matrix}.",
        expected=expected,
        validator=lambda received: _validate_keyword(received, expected),
        hint="Ask what happens to the basis vectors [1, 0] and [0, 1].",
        explanation=explanation,
        tags=("linear-algebra", "linear-transformations"),
        exercise_id="linear-algebra-transformation-classification",
        answer_type="multiple_choice",
    )


def eigenvector_check_exercise(*, seed: int | None = None) -> Exercise:
    """Generate an eigenpair-checking exercise."""

    rng = Random(seed)
    options = (
        ([[3, 0], [0, 1]], [1, 0], 3.0),
        ([[2, 0], [0, 5]], [0, 1], 5.0),
        ([[1, 1], [0, 1]], [1, 0], 1.0),
        ([[4, 0], [0, -2]], [0, 1], -2.0),
    )
    matrix, vector, eigenvalue = rng.choice(options)
    return Exercise(
        prompt=(
            f"Check whether v = {vector} is an eigenvector of A = {matrix}. "
            "If yes, give the eigenvalue."
        ),
        expected=eigenvalue,
        validator=lambda received: validate_eigenpair(matrix, vector, received),
        hint="Compute A v and see whether the result is a scalar multiple of v.",
        explanation="An eigenpair satisfies A v = lambda v with v nonzero.",
        tags=("linear-algebra", "eigenvalues", "eigenvectors"),
        exercise_id="linear-algebra-eigenvector-check",
        answer_type="numeric",
    )


def _validate_keyword(received: object, expected: str) -> AnswerCheck:
    normalized = str(received).strip().lower()
    correct = normalized == expected
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message="Correct." if correct else f"Expected {expected}.",
    )


__all__ = [
    "dot_product_exercise",
    "eigenvector_check_exercise",
    "linear_system_exercise",
    "matrix_shape_exercise",
    "matrix_vector_product_exercise",
    "transformation_classification_exercise",
    "vector_norm_exercise",
]
