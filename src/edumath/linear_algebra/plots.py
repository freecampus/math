"""Lightweight plotting helpers for linear algebra lessons."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import cast

import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes

from edumath.core import PlotRange, PlotScene2D, PlotStyle, Viewport2D
from edumath.core.plots import Drawable2D
from edumath.linear_algebra.concepts import matrix_vector_product


@dataclass(frozen=True)
class Vector2D:
    """Drawable 2D vector arrow."""

    end: tuple[float, float]
    start: tuple[float, float] = (0.0, 0.0)
    style: PlotStyle = field(default_factory=PlotStyle)

    def draw(self, axis: Axes) -> None:
        """Draw the vector as an arrow on ``axis``."""

        dx_value = self.end[0] - self.start[0]
        dy_value = self.end[1] - self.start[1]
        axis.arrow(
            self.start[0],
            self.start[1],
            dx_value,
            dy_value,
            color=self.style.color,
            linewidth=self.style.linewidth,
            linestyle=self.style.linestyle,
            length_includes_head=True,
            head_width=0.12,
            head_length=0.18,
            label=self.style.label,
        )
        if self.style.label:
            axis.text(
                self.end[0],
                self.end[1],
                f" {self.style.label}",
                color=self.style.color,
                va="center",
            )


@dataclass(frozen=True)
class LineEquation2D:
    """Drawable line from an equation ``a x + b y = c``."""

    coefficients: tuple[float, float]
    value: float
    domain: PlotRange = field(default_factory=lambda: PlotRange(-5, 5, 100))
    style: PlotStyle = field(default_factory=PlotStyle)

    def draw(self, axis: Axes) -> None:
        """Draw the line on ``axis``."""

        a_value, b_value = self.coefficients
        if abs(b_value) < 1e-12:
            if abs(a_value) < 1e-12:
                return
            x_value = self.value / a_value
            axis.axvline(
                x_value,
                color=self.style.color,
                linewidth=self.style.linewidth,
                linestyle=self.style.linestyle,
                label=self.style.label,
            )
            return
        x_values = self.domain.values()
        y_values = (self.value - a_value * x_values) / b_value
        axis.plot(
            x_values,
            y_values,
            color=self.style.color,
            linewidth=self.style.linewidth,
            linestyle=self.style.linestyle,
            label=self.style.label,
        )


def vector_scene(
    vectors: Sequence[npt.ArrayLike],
    *,
    labels: Sequence[str] | None = None,
) -> PlotScene2D:
    """Create a scene showing one or more vectors from the origin."""

    labels_tuple = (
        tuple(labels) if labels is not None else _default_labels(len(vectors))
    )
    vector_points = tuple(_as_vector_2d(vector) for vector in vectors)
    colors = _palette()
    elements = tuple(
        Vector2D(
            point,
            style=PlotStyle(color=colors[index % len(colors)], label=label),
        )
        for index, (point, label) in enumerate(
            zip(vector_points, labels_tuple, strict=True)
        )
    )
    return PlotScene2D(
        elements=elements,
        viewport=_viewport_for_points((*vector_points, (0.0, 0.0))),
        title="Vectors in the plane",
        equal_aspect=True,
    )


def vector_addition_scene(left: npt.ArrayLike, right: npt.ArrayLike) -> PlotScene2D:
    """Create a head-to-tail vector addition scene."""

    left_point = _as_vector_2d(left)
    right_point = _as_vector_2d(right)
    sum_point = (left_point[0] + right_point[0], left_point[1] + right_point[1])
    elements: tuple[Drawable2D, ...] = (
        Vector2D(left_point, style=PlotStyle(color="#1a73e8", label="u")),
        Vector2D(
            sum_point,
            start=left_point,
            style=PlotStyle(color="#d93025", label="v"),
        ),
        Vector2D(sum_point, style=PlotStyle(color="#137333", label="u + v")),
    )
    return PlotScene2D(
        elements=elements,
        viewport=_viewport_for_points(((0.0, 0.0), left_point, right_point, sum_point)),
        title="Vector addition",
        equal_aspect=True,
    )


def matrix_transformation_scene(
    matrix: npt.ArrayLike,
    vectors: Sequence[npt.ArrayLike] | None = None,
) -> PlotScene2D:
    """Create a scene comparing input vectors with their matrix images."""

    input_vectors = vectors if vectors is not None else ((1, 0), (0, 1), (1, 1))
    matrix_array = _as_matrix_2x2(matrix)
    elements: list[Drawable2D] = []
    points: list[tuple[float, float]] = [(0.0, 0.0)]
    for index, vector in enumerate(input_vectors, start=1):
        point = _as_vector_2d(vector)
        image = _as_vector_2d(matrix_vector_product(matrix_array, point))
        points.extend((point, image))
        elements.append(
            Vector2D(
                point,
                style=PlotStyle(
                    color="#5f6368",
                    linestyle="--",
                    label=f"v{index}",
                ),
            )
        )
        elements.append(
            Vector2D(
                image,
                style=PlotStyle(color="#1a73e8", label=f"A v{index}"),
            )
        )
    return PlotScene2D(
        elements=tuple(elements),
        viewport=_viewport_for_points(tuple(points)),
        title="Matrix transformation",
        equal_aspect=True,
    )


def basis_transformation_scene(matrix: npt.ArrayLike) -> PlotScene2D:
    """Create a scene showing where a matrix sends the standard basis vectors."""

    return matrix_transformation_scene(matrix, vectors=((1, 0), (0, 1)))


def system_lines_scene(
    matrix: npt.ArrayLike,
    values: npt.ArrayLike,
    *,
    x_min: float = -5,
    x_max: float = 5,
    y_min: float = -5,
    y_max: float = 5,
) -> PlotScene2D:
    """Create a scene for a 2-by-2 linear system as two lines."""

    matrix_array = _as_matrix_2x2(matrix)
    values_array = np.asarray(values, dtype=float)
    if values_array.shape != (2,):
        msg = "values must have shape (2,)"
        raise ValueError(msg)
    colors = _palette()
    elements = tuple(
        LineEquation2D(
            coefficients=(float(matrix_array[index, 0]), float(matrix_array[index, 1])),
            value=float(values_array[index]),
            domain=PlotRange(x_min, x_max, 200),
            style=PlotStyle(color=colors[index], label=f"equation {index + 1}"),
        )
        for index in range(2)
    )
    return PlotScene2D(
        elements=elements,
        viewport=Viewport2D(x=PlotRange(x_min, x_max), y=PlotRange(y_min, y_max)),
        title="Linear system as lines",
        equal_aspect=True,
    )


def eigenvector_scene(matrix: npt.ArrayLike, vector: npt.ArrayLike) -> PlotScene2D:
    """Create a scene comparing a vector with its image under a matrix."""

    matrix_array = _as_matrix_2x2(matrix)
    vector_point = _as_vector_2d(vector)
    image_point = _as_vector_2d(matrix_vector_product(matrix_array, vector_point))
    elements: tuple[Drawable2D, ...] = (
        Vector2D(vector_point, style=PlotStyle(color="#1a73e8", label="v")),
        Vector2D(image_point, style=PlotStyle(color="#d93025", label="A v")),
    )
    return PlotScene2D(
        elements=elements,
        viewport=_viewport_for_points(((0.0, 0.0), vector_point, image_point)),
        title="Eigenvector check",
        equal_aspect=True,
    )


def _as_vector_2d(vector: npt.ArrayLike) -> tuple[float, float]:
    array = np.asarray(vector, dtype=float).reshape(-1)
    if array.shape != (2,):
        msg = "vector must have exactly two coordinates"
        raise ValueError(msg)
    return (float(array[0]), float(array[1]))


def _as_matrix_2x2(matrix: npt.ArrayLike) -> npt.NDArray[np.float64]:
    array = np.asarray(matrix, dtype=float)
    if array.shape != (2, 2):
        msg = "matrix must have shape (2, 2)"
        raise ValueError(msg)
    return cast(npt.NDArray[np.float64], array)


def _default_labels(count: int) -> tuple[str, ...]:
    return tuple(f"v{index}" for index in range(1, count + 1))


def _palette() -> tuple[str, ...]:
    return ("#1a73e8", "#d93025", "#137333", "#f9ab00", "#9334e6")


def _viewport_for_points(points: Sequence[tuple[float, float]]) -> Viewport2D:
    max_coordinate = max(
        1.0,
        *(max(abs(x_value), abs(y_value)) for x_value, y_value in points),
    )
    bound = max_coordinate + 1.0
    return Viewport2D(x=PlotRange(-bound, bound), y=PlotRange(-bound, bound))


__all__ = [
    "LineEquation2D",
    "Vector2D",
    "basis_transformation_scene",
    "eigenvector_scene",
    "matrix_transformation_scene",
    "system_lines_scene",
    "vector_addition_scene",
    "vector_scene",
]
