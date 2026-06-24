"""Quiz helpers for linear algebra lessons."""

from __future__ import annotations

from edumath.core import AnswerOption, Question, QuizSession
from edumath.linear_algebra.concepts import (
    can_multiply,
    matrix_vector_product,
    vector_norm,
)
from edumath.linear_algebra.validators import (
    validate_scalar_answer,
    validate_shape_answer,
    validate_vector_answer,
)


def vector_norm_question(vector: tuple[float, ...] = (3, 4)) -> Question:
    """Create an auto-checkable vector-norm question."""

    expected = vector_norm(vector)
    return Question(
        prompt=f"What is the length of the vector {list(vector)}?",
        expected=expected,
        validator=lambda received: validate_scalar_answer(received, expected),
        answer_type="numeric",
        explanation="Use the square root of the sum of squared coordinates.",
        tags=("linear-algebra", "vectors"),
    )


def perpendicular_question() -> Question:
    """Create a multiple-choice question about perpendicular vectors."""

    return Question(
        prompt="Which dot product means two nonzero vectors are perpendicular?",
        expected="zero",
        options=(
            AnswerOption("The dot product is 0", "zero"),
            AnswerOption("The dot product is 1", "one"),
            AnswerOption("The dot product is negative", "negative"),
        ),
        explanation="A zero dot product means nonzero vectors meet at a right angle.",
        tags=("linear-algebra", "vectors", "dot-product"),
    )


def matrix_shape_question(shape: tuple[int, int] = (2, 3)) -> Question:
    """Create a matrix-shape question."""

    return Question(
        prompt=(
            f"A matrix has {shape[0]} rows and {shape[1]} columns. What is its shape?"
        ),
        expected=shape,
        validator=lambda received: validate_shape_answer(received, shape),
        answer_type="exact",
        explanation="Shape is written rows by columns.",
        tags=("linear-algebra", "matrices"),
    )


def product_defined_question(
    left_shape: tuple[int, ...] = (2, 3),
    right_shape: tuple[int, ...] = (3, 4),
) -> Question:
    """Create a question about whether a matrix product is defined."""

    expected = can_multiply(left_shape, right_shape)
    return Question(
        prompt=f"Is a product with shapes {left_shape} and {right_shape} defined?",
        expected=expected,
        options=(
            AnswerOption("Yes", True),
            AnswerOption("No", False),
        ),
        explanation="The inner dimensions must match.",
        tags=("linear-algebra", "matrix-operations"),
    )


def matrix_vector_product_question() -> Question:
    """Create a matrix-vector product question."""

    matrix = [[2, -1], [0, 3]]
    vector = [4, 5]
    expected = matrix_vector_product(matrix, vector)
    return Question(
        prompt=f"Compute {matrix} times {vector}.",
        expected=expected.tolist(),
        validator=lambda received: validate_vector_answer(received, expected),
        answer_type="exact",
        explanation="Each output entry is a row dot product with the vector.",
        tags=("linear-algebra", "matrix-operations"),
    )


def system_classification_question() -> Question:
    """Create a question about classifying a small linear system."""

    return Question(
        prompt="The equations x + y = 2 and 2x + 2y = 4 represent which case?",
        expected="infinitely many",
        options=(
            AnswerOption("One solution", "one"),
            AnswerOption("No solution", "none"),
            AnswerOption("Infinitely many solutions", "infinitely many"),
        ),
        explanation="The second equation is exactly twice the first.",
        tags=("linear-algebra", "systems"),
    )


def transformation_action_question() -> Question:
    """Create a question about identifying a transformation from a matrix."""

    return Question(
        prompt="What does the matrix [[1, 0], [0, 0]] do in the plane?",
        expected="projection",
        options=(
            AnswerOption("Projection onto the x-axis", "projection"),
            AnswerOption("Rotation by 90 degrees", "rotation"),
            AnswerOption("Reflection over the y-axis", "reflection"),
        ),
        explanation="The x-coordinate stays and the y-coordinate becomes zero.",
        tags=("linear-algebra", "linear-transformations"),
    )


def eigenvalue_question() -> Question:
    """Create a question about reading an eigenvalue from A v = lambda v."""

    return Question(
        prompt="If A v = 5 v for a nonzero vector v, what is the eigenvalue?",
        expected=5.0,
        validator=lambda received: validate_scalar_answer(received, 5.0),
        answer_type="numeric",
        explanation="The eigenvalue is the scalar multiplying v.",
        tags=("linear-algebra", "eigenvalues", "eigenvectors"),
    )


def linear_algebra_diagnostic_quiz() -> QuizSession:
    """Return a short diagnostic quiz for the linear algebra path."""

    return QuizSession(
        questions=(
            vector_norm_question(),
            perpendicular_question(),
            matrix_shape_question(),
            product_defined_question(),
            matrix_vector_product_question(),
            system_classification_question(),
            transformation_action_question(),
            eigenvalue_question(),
        )
    )


__all__ = [
    "eigenvalue_question",
    "linear_algebra_diagnostic_quiz",
    "matrix_shape_question",
    "matrix_vector_product_question",
    "perpendicular_question",
    "product_defined_question",
    "system_classification_question",
    "transformation_action_question",
    "vector_norm_question",
]
