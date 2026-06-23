"""Plotting helpers for differential equations lessons."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import pairwise

import numpy as np
from matplotlib.axes import Axes

from edumath.core import (
    ExplicitFunction2D,
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Point2D,
    Segment2D,
    Viewport2D,
)
from edumath.core.plots import Drawable2D
from edumath.differential_equations.solvers import (
    DerivativeFunction,
    direction_field_values,
    euler_method,
)


@dataclass(frozen=True)
class SlopeField2D:
    """Drawable slope field made of short normalized segments."""

    segments: tuple[tuple[float, float, float, float], ...]
    style: PlotStyle = field(
        default_factory=lambda: PlotStyle(color="#5f6368", linewidth=1.2)
    )

    def draw(self, axis: Axes) -> None:
        """Draw all slope-field segments on an axis."""

        for x_value, y_value, dx_value, dy_value in self.segments:
            axis.plot(
                [x_value - dx_value / 2, x_value + dx_value / 2],
                [y_value - dy_value / 2, y_value + dy_value / 2],
                color=self.style.color,
                linewidth=self.style.linewidth,
                alpha=0.8,
            )


@dataclass(frozen=True)
class PhaseLine2D:
    """Simple phase-line drawing for one-dimensional autonomous ODEs."""

    equilibria: tuple[float, ...]
    arrows: tuple[tuple[float, int], ...]
    y_level: float = 0.0
    style: PlotStyle = field(default_factory=lambda: PlotStyle(color="#1a73e8"))

    def draw(self, axis: Axes) -> None:
        """Draw a horizontal phase line with arrows and equilibrium points."""

        for x_value, direction in self.arrows:
            axis.arrow(
                x_value - 0.15 * direction,
                self.y_level,
                0.3 * direction,
                0,
                color=self.style.color,
                head_width=0.08,
                length_includes_head=True,
            )
        for equilibrium in self.equilibria:
            axis.plot([equilibrium], [self.y_level], marker="o", color="#d93025")


def slope_field_scene(
    derivative: DerivativeFunction,
    *,
    x_min: float = -3,
    x_max: float = 3,
    y_min: float = -3,
    y_max: float = 3,
    density: int = 13,
) -> PlotScene2D:
    """Create a slope-field scene for ``dy/dx = f(x, y)``."""

    if density < 2:
        msg = "density must be at least 2"
        raise ValueError(msg)

    x_values = np.linspace(x_min, x_max, density)
    y_values = np.linspace(y_min, y_max, density)
    field = SlopeField2D(tuple(direction_field_values(derivative, x_values, y_values)))
    return PlotScene2D(
        elements=(field,),
        viewport=Viewport2D(x=PlotRange(x_min, x_max), y=PlotRange(y_min, y_max)),
        title="Slope field",
    )


def euler_method_scene(
    derivative: DerivativeFunction,
    *,
    initial_x: float,
    initial_y: float,
    step: float,
    steps: int,
    x_min: float | None = None,
    x_max: float | None = None,
    y_min: float = -1,
    y_max: float = 5,
) -> PlotScene2D:
    """Create a scene showing Euler-method segments on top of a slope field."""

    points = euler_method(
        derivative,
        initial_x=initial_x,
        initial_y=initial_y,
        step=step,
        steps=steps,
    )
    x_lower = x_min if x_min is not None else min(x for x, _ in points) - abs(step)
    x_upper = x_max if x_max is not None else max(x for x, _ in points) + abs(step)
    elements: list[Drawable2D] = [
        SlopeField2D(
            tuple(
                direction_field_values(
                    derivative,
                    np.linspace(x_lower, x_upper, 11),
                    np.linspace(y_min, y_max, 11),
                )
            )
        )
    ]
    elements.extend(
        Segment2D(
            Point2D(start_x, start_y),
            Point2D(end_x, end_y),
            style=PlotStyle(color="#d93025", linewidth=2.0),
        )
        for (start_x, start_y), (end_x, end_y) in pairwise(points)
    )
    elements.extend(
        Point2D(x_value, y_value, style=PlotStyle(color="#d93025", marker="o"))
        for x_value, y_value in points
    )
    return PlotScene2D(
        elements=tuple(elements),
        viewport=Viewport2D(x=PlotRange(x_lower, x_upper), y=PlotRange(y_min, y_max)),
        title="Euler approximation",
    )


def solution_family_scene(
    expressions: Sequence[str],
    *,
    x_min: float = -3,
    x_max: float = 3,
    y_min: float = -3,
    y_max: float = 3,
    variable: str = "x",
) -> PlotScene2D:
    """Create a scene containing several solution curves."""

    colors = ("#1a73e8", "#d93025", "#137333", "#f9ab00", "#9334e6")
    curves = tuple(
        ExplicitFunction2D(
            expression,
            variable=variable,
            domain=PlotRange(x_min, x_max),
            style=PlotStyle(
                color=colors[index % len(colors)], label=f"solution {index + 1}"
            ),
        )
        for index, expression in enumerate(expressions)
    )
    return PlotScene2D(
        elements=curves,
        viewport=Viewport2D(x=PlotRange(x_min, x_max), y=PlotRange(y_min, y_max)),
        title="Solution family",
    )


def phase_line_scene(
    rhs: DerivativeFunction,
    *,
    equilibria: Sequence[float],
    y_min: float = -3,
    y_max: float = 3,
    samples: int = 9,
) -> PlotScene2D:
    """Create a simple phase-line scene for ``y'=f(y)``."""

    y_values = np.linspace(y_min, y_max, samples)
    arrows = tuple(
        (float(y_value), 1 if rhs(0, float(y_value)) > 0 else -1)
        for y_value in y_values
    )
    return PlotScene2D(
        elements=(PhaseLine2D(tuple(float(value) for value in equilibria), arrows),),
        viewport=Viewport2D(x=PlotRange(y_min, y_max), y=PlotRange(-1, 1)),
        title="Phase line",
        show_axes=False,
    )


def linear_system_phase_plane_scene(
    matrix: Sequence[Sequence[float]],
    *,
    x_min: float = -3,
    x_max: float = 3,
    y_min: float = -3,
    y_max: float = 3,
    density: int = 11,
) -> PlotScene2D:
    """Create a direction-field style phase plane for a 2-by-2 linear system."""

    if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
        msg = "matrix must be 2 by 2"
        raise ValueError(msg)

    a, b = matrix[0]
    c, d = matrix[1]
    x_values = np.linspace(x_min, x_max, density)
    y_values = np.linspace(y_min, y_max, density)
    segments: list[tuple[float, float, float, float]] = []
    for x_value in x_values:
        for y_value in y_values:
            dx_value = a * x_value + b * y_value
            dy_value = c * x_value + d * y_value
            length = float(np.hypot(dx_value, dy_value))
            if length == 0:
                continue
            scale = 0.35 / length
            segments.append(
                (
                    float(x_value),
                    float(y_value),
                    float(dx_value * scale),
                    float(dy_value * scale),
                )
            )
    return PlotScene2D(
        elements=(SlopeField2D(tuple(segments), PlotStyle(color="#1a73e8")),),
        viewport=Viewport2D(x=PlotRange(x_min, x_max), y=PlotRange(y_min, y_max)),
        title="Phase plane",
    )


__all__ = [
    "PhaseLine2D",
    "SlopeField2D",
    "euler_method_scene",
    "linear_system_phase_plane_scene",
    "phase_line_scene",
    "slope_field_scene",
    "solution_family_scene",
]
