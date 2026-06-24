"""Linear algebra concepts and small computational helpers."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import numpy.typing as npt

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

VECTORS = Lesson(
    title="Vectors",
    slug="vectors",
    prerequisites=("coordinate plane", "distance formula", "signed numbers"),
    objectives=(
        LearningObjective("Represent quantities as ordered lists of coordinates."),
        LearningObjective("Compute vector length and dot products."),
        LearningObjective("Explain vectors as positions, movements, or data points."),
    ),
    sections=(
        LessonSection(
            title="Magnitude and direction",
            body=(
                "A vector stores several numbers at once and can be read as a "
                "movement, position, or data record."
            ),
        ),
    ),
    summary="Vectors are the basic objects of linear algebra.",
    tags=("linear-algebra", "vectors", "norm", "dot-product"),
)

MATRICES = Lesson(
    title="Matrices",
    slug="matrices",
    prerequisites=("tables of numbers", "rows and columns", "vectors"),
    objectives=(
        LearningObjective("Read the shape of a matrix as rows by columns."),
        LearningObjective("Interpret rows and columns in context."),
        LearningObjective(
            "Recognize identity, zero, diagonal, and coefficient matrices."
        ),
    ),
    sections=(
        LessonSection(
            title="Rows, columns, and shape",
            body="A matrix is a rectangular array whose shape controls what it can do.",
        ),
    ),
    summary="Matrices organize numbers for systems, data, and transformations.",
    tags=("linear-algebra", "matrices", "shape"),
)

MATRIX_OPERATIONS = Lesson(
    title="Matrix operations",
    slug="matrix-operations",
    prerequisites=("matrix shape", "vector arithmetic"),
    objectives=(
        LearningObjective("Add matrices only when their shapes match."),
        LearningObjective("Use inner dimensions to decide whether products exist."),
        LearningObjective("Compute matrix-vector and small matrix products."),
    ),
    sections=(
        LessonSection(
            title="Shape before arithmetic",
            body=(
                "Linear algebra calculations are governed by dimension rules before "
                "any arithmetic begins."
            ),
        ),
    ),
    summary="Operations combine vectors and matrices while respecting dimensions.",
    tags=("linear-algebra", "matrix-products", "dimension-checks"),
)

SYSTEMS_AND_ELIMINATION = Lesson(
    title="Systems and elimination",
    slug="systems-and-elimination",
    prerequisites=("linear equations", "matrices", "matrix operations"),
    objectives=(
        LearningObjective("Write a system of linear equations as A x = b."),
        LearningObjective("Use elimination to solve small systems."),
        LearningObjective(
            "Classify systems as one solution, none, or infinitely many."
        ),
    ),
    sections=(
        LessonSection(
            title="Many conditions at once",
            body=(
                "A linear system asks for one vector that satisfies several linear "
                "equations simultaneously."
            ),
        ),
    ),
    summary="Elimination preserves the solution set while simplifying equations.",
    tags=("linear-algebra", "systems", "elimination"),
)

LINEAR_TRANSFORMATIONS = Lesson(
    title="Linear transformations",
    slug="linear-transformations",
    prerequisites=("functions", "matrix-vector products", "basis vectors"),
    objectives=(
        LearningObjective("Interpret a matrix as a function from vectors to vectors."),
        LearningObjective("Predict transformations from images of basis vectors."),
        LearningObjective(
            "Identify common scalings, reflections, shears, and projections."
        ),
    ),
    sections=(
        LessonSection(
            title="Matrices as movement rules",
            body=(
                "A linear transformation preserves addition and scaling, so a matrix "
                "is determined by what it does to basis vectors."
            ),
        ),
    ),
    summary="Matrices describe geometric and data transformations.",
    tags=("linear-algebra", "transformations", "basis"),
)

EIGENVALUES_EIGENVECTORS = Lesson(
    title="Eigenvalues and eigenvectors",
    slug="eigenvalues-eigenvectors",
    prerequisites=(
        "matrix-vector products",
        "linear transformations",
        "scalar multiples",
    ),
    objectives=(
        LearningObjective("Check whether a nonzero vector is an eigenvector."),
        LearningObjective(
            "Interpret eigenvalues as scale factors along special directions."
        ),
        LearningObjective(
            "Explain why eigenvectors help describe repeated transformations."
        ),
    ),
    sections=(
        LessonSection(
            title="Directions that keep their line",
            body=(
                "An eigenvector may stretch, shrink, or flip, but after the matrix "
                "acts it still lies on the same line."
            ),
        ),
    ),
    summary="Eigenvectors reveal directions a transformation preserves.",
    tags=("linear-algebra", "eigenvalues", "eigenvectors"),
)

LINEAR_ALGEBRA_PATH = StudyPath(
    title="Linear Algebra",
    lessons=(
        VECTORS,
        MATRICES,
        MATRIX_OPERATIONS,
        SYSTEMS_AND_ELIMINATION,
        LINEAR_TRANSFORMATIONS,
        EIGENVALUES_EIGENVECTORS,
    ),
)


def vector_add(left: npt.ArrayLike, right: npt.ArrayLike) -> npt.NDArray[np.float64]:
    """Return the coordinate-wise sum of two vectors."""

    return np.asarray(np.asarray(left, dtype=float) + np.asarray(right, dtype=float))


def scalar_multiply(
    scalar: float,
    vector_or_matrix: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Multiply every entry of a vector or matrix by ``scalar``."""

    return np.asarray(float(scalar) * np.asarray(vector_or_matrix, dtype=float))


def dot_product(left: npt.ArrayLike, right: npt.ArrayLike) -> float:
    """Return the dot product of two vectors."""

    return float(np.dot(np.asarray(left, dtype=float), np.asarray(right, dtype=float)))


def vector_norm(vector: npt.ArrayLike) -> float:
    """Return the Euclidean norm of a vector."""

    return float(np.linalg.norm(np.asarray(vector, dtype=float)))


def matrix_shape(matrix: npt.ArrayLike) -> tuple[int, ...]:
    """Return the shape of a vector or matrix as a tuple of dimensions."""

    return tuple(int(dimension) for dimension in np.asarray(matrix, dtype=float).shape)


def can_multiply(left_shape: Sequence[int], right_shape: Sequence[int]) -> bool:
    """Return whether two shapes can be multiplied in the order given."""

    if len(left_shape) == 0 or len(right_shape) == 0:
        return False
    return int(left_shape[-1]) == int(right_shape[0])


def matrix_vector_product(
    matrix: npt.ArrayLike,
    vector: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Multiply a matrix by a vector."""

    return np.asarray(np.asarray(matrix, dtype=float) @ np.asarray(vector, dtype=float))


def matrix_product(
    left: npt.ArrayLike,
    right: npt.ArrayLike,
) -> npt.NDArray[np.float64]:
    """Multiply two matrices or matrix-like arrays."""

    return np.asarray(np.asarray(left, dtype=float) @ np.asarray(right, dtype=float))


def identity_matrix(size: int) -> npt.NDArray[np.float64]:
    """Return the ``size`` by ``size`` identity matrix."""

    if size <= 0:
        msg = "size must be positive"
        raise ValueError(msg)
    return np.asarray(np.eye(size, dtype=float))


def determinant_2x2(matrix: npt.ArrayLike) -> float:
    """Return the determinant of a 2-by-2 matrix."""

    array = _as_matrix_2x2(matrix)
    return float(array[0, 0] * array[1, 1] - array[0, 1] * array[1, 0])


def inverse_2x2(matrix: npt.ArrayLike) -> npt.NDArray[np.float64]:
    """Return the inverse of a nonsingular 2-by-2 matrix."""

    array = _as_matrix_2x2(matrix)
    determinant = determinant_2x2(array)
    if abs(determinant) < 1e-12:
        msg = "matrix is singular and has no inverse"
        raise ValueError(msg)
    inverse = np.array(
        [[array[1, 1], -array[0, 1]], [-array[1, 0], array[0, 0]]],
        dtype=float,
    )
    return np.asarray(inverse / determinant)


def eigenvalues_2x2(matrix: npt.ArrayLike) -> tuple[complex, complex]:
    """Return the two eigenvalues of a 2-by-2 matrix."""

    array = _as_matrix_2x2(matrix)
    values = np.linalg.eigvals(array)
    return (complex(values[0]), complex(values[1]))


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


def _as_matrix_2x2(matrix: npt.ArrayLike) -> npt.NDArray[np.float64]:
    array = np.asarray(matrix, dtype=float)
    if array.shape != (2, 2):
        msg = "matrix must have shape (2, 2)"
        raise ValueError(msg)
    return np.asarray(array, dtype=float)


__all__ = [
    "EIGENVALUES_EIGENVECTORS",
    "LINEAR_ALGEBRA_PATH",
    "LINEAR_TRANSFORMATIONS",
    "MATRICES",
    "MATRIX_OPERATIONS",
    "SYSTEMS_AND_ELIMINATION",
    "VECTORS",
    "can_multiply",
    "determinant_2x2",
    "dot_product",
    "eigenvalues_2x2",
    "identity_matrix",
    "inverse_2x2",
    "matrix_product",
    "matrix_shape",
    "matrix_vector_product",
    "scalar_multiply",
    "solve_linear_system",
    "vector_add",
    "vector_norm",
]
