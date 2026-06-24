"""Answer validators for linear algebra lessons."""

from __future__ import annotations

import ast
import re
from collections.abc import Sequence
from typing import SupportsFloat, cast

import numpy as np
import numpy.typing as npt

from edumath.core import AnswerCheck, NumericTolerance, check_numeric_answer
from edumath.linear_algebra.concepts import matrix_vector_product

LINEAR_ALGEBRA_TOLERANCE = NumericTolerance(absolute=1e-9, relative=1e-9)
SHAPE_PATTERN = re.compile(r"-?\d+")


def validate_scalar_answer(
    received: object,
    expected: object,
    *,
    tolerance: NumericTolerance = LINEAR_ALGEBRA_TOLERANCE,
) -> AnswerCheck:
    """Validate a numeric scalar answer."""

    try:
        return check_numeric_answer(
            float(cast(SupportsFloat, received)),
            float(cast(SupportsFloat, expected)),
            tolerance=tolerance,
        )
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare scalar answer: {error}",
        )


def validate_vector_answer(
    received: object,
    expected: npt.ArrayLike,
    *,
    tolerance: float = 1e-9,
) -> AnswerCheck:
    """Validate a vector answer from a list, tuple, array, or string."""

    try:
        received_array = _parse_array(received)
        expected_array = np.asarray(expected, dtype=float)
        correct = received_array.shape == expected_array.shape and bool(
            np.allclose(received_array, expected_array, atol=tolerance, rtol=tolerance)
        )
    except (TypeError, ValueError, SyntaxError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare vector answer: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message=(
            "Correct." if correct else f"Expected vector {expected_array.tolist()}."
        ),
    )


def validate_matrix_answer(
    received: object,
    expected: npt.ArrayLike,
    *,
    tolerance: float = 1e-9,
) -> AnswerCheck:
    """Validate a matrix answer from a list, tuple, array, or string."""

    try:
        received_array = _parse_array(received)
        expected_array = np.asarray(expected, dtype=float)
        correct = received_array.shape == expected_array.shape and bool(
            np.allclose(received_array, expected_array, atol=tolerance, rtol=tolerance)
        )
    except (TypeError, ValueError, SyntaxError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected,
            message=f"Could not compare matrix answer: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected,
        message=(
            "Correct." if correct else f"Expected matrix {expected_array.tolist()}."
        ),
    )


def validate_shape_answer(received: object, expected: Sequence[int]) -> AnswerCheck:
    """Validate a matrix shape such as ``(2, 3)`` or ``2 x 3``."""

    expected_shape = tuple(int(value) for value in expected)
    try:
        received_shape = _parse_shape(received)
    except (TypeError, ValueError, SyntaxError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=expected_shape,
            message=f"Could not read shape answer: {error}",
        )
    correct = received_shape == expected_shape
    return AnswerCheck(
        correct=correct,
        received=received,
        expected=expected_shape,
        message="Correct." if correct else f"Expected shape {expected_shape}.",
    )


def validate_solution_vector(
    received: object,
    matrix: npt.ArrayLike,
    values: npt.ArrayLike,
    *,
    tolerance: float = 1e-9,
) -> AnswerCheck:
    """Validate that a proposed vector solves ``A x = b``."""

    try:
        received_array = _parse_array(received)
        values_array = np.asarray(values, dtype=float)
        product = matrix_vector_product(matrix, received_array)
        correct = product.shape == values_array.shape and bool(
            np.allclose(product, values_array, atol=tolerance, rtol=tolerance)
        )
    except (TypeError, ValueError, SyntaxError) as error:
        return AnswerCheck(
            correct=False,
            received=received,
            expected=values,
            message=f"Could not check solution vector: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=received,
        expected=values,
        message=(
            "Correct."
            if correct
            else "Substituting your vector into A x did not produce b."
        ),
    )


def validate_eigenpair(
    matrix: npt.ArrayLike,
    vector: npt.ArrayLike,
    eigenvalue: object,
    *,
    tolerance: float = 1e-9,
) -> AnswerCheck:
    """Validate whether ``A v = lambda v`` for a nonzero vector."""

    vector_array = np.asarray(vector, dtype=float)
    try:
        scalar = float(cast(SupportsFloat, eigenvalue))
        if np.linalg.norm(vector_array) <= tolerance:
            return AnswerCheck(
                correct=False,
                received=(vector, eigenvalue),
                expected="nonzero eigenvector",
                message="The zero vector is not considered an eigenvector.",
            )
        left = matrix_vector_product(matrix, vector_array)
        right = scalar * vector_array
        correct = left.shape == right.shape and bool(
            np.allclose(left, right, atol=tolerance, rtol=tolerance)
        )
    except (TypeError, ValueError) as error:
        return AnswerCheck(
            correct=False,
            received=(vector, eigenvalue),
            expected="A v = lambda v",
            message=f"Could not check eigenpair: {error}",
        )

    return AnswerCheck(
        correct=correct,
        received=(vector, eigenvalue),
        expected="A v = lambda v",
        message="Correct." if correct else "A v was not equal to lambda v.",
    )


def _parse_array(value: object) -> npt.NDArray[np.float64]:
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            msg = "empty answer"
            raise ValueError(msg)
        try:
            parsed = ast.literal_eval(stripped)
        except (SyntaxError, ValueError):
            if ";" in stripped:
                rows = [
                    [float(part) for part in row.replace(",", " ").split()]
                    for row in stripped.split(";")
                ]
                return np.asarray(rows, dtype=float)
            parsed = [float(part) for part in stripped.replace(",", " ").split()]
        return np.asarray(parsed, dtype=float)
    return np.asarray(value, dtype=float)


def _parse_shape(value: object) -> tuple[int, ...]:
    if isinstance(value, str):
        stripped = value.strip().lower()
        if not stripped:
            msg = "empty shape"
            raise ValueError(msg)
        try:
            parsed = ast.literal_eval(stripped)
        except (SyntaxError, ValueError):
            numbers = SHAPE_PATTERN.findall(stripped)
            if not numbers:
                msg = "shape must contain dimensions"
                raise ValueError(msg) from None
            return tuple(int(number) for number in numbers)
        return _parse_shape(parsed)
    if isinstance(value, int):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(int(float(cast(SupportsFloat, dimension))) for dimension in value)
    msg = "shape must be a sequence or string"
    raise TypeError(msg)


__all__ = [
    "LINEAR_ALGEBRA_TOLERANCE",
    "validate_eigenpair",
    "validate_matrix_answer",
    "validate_scalar_answer",
    "validate_shape_answer",
    "validate_solution_vector",
    "validate_vector_answer",
]
