"""Linear algebra helpers."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


def dot_product(left: npt.ArrayLike, right: npt.ArrayLike) -> float:
    """Return the dot product of two vectors."""

    return float(np.dot(np.asarray(left, dtype=float), np.asarray(right, dtype=float)))


def vector_norm(vector: npt.ArrayLike) -> float:
    """Return the Euclidean norm of a vector."""

    return float(np.linalg.norm(np.asarray(vector, dtype=float)))


def matrix_vector_product(
    matrix: npt.ArrayLike,
    vector: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Multiply a matrix by a vector."""

    return np.asarray(np.asarray(matrix, dtype=float) @ np.asarray(vector, dtype=float))


def solve_linear_system(
    matrix: npt.ArrayLike,
    values: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Solve ``A x = b``."""

    solution = np.linalg.solve(
        np.asarray(matrix, dtype=float),
        np.asarray(values, dtype=float),
    )
    return np.asarray(solution, dtype=float)


__all__ = [
    "dot_product",
    "matrix_vector_product",
    "solve_linear_system",
    "vector_norm",
]
