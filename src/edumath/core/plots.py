"""Reusable 2D plotting primitives inspired by graphing tools such as Winplot."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, cast

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import sympy as sp
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from edumath.core.expressions import MathExpression, parse_expression


@dataclass(frozen=True)
class PlotRange:
    """A sampled one-dimensional range."""

    minimum: float = -10
    maximum: float = 10
    samples: int = 400

    def values(self) -> npt.NDArray[np.float64]:
        if self.samples < 2:
            msg = "samples must be at least 2"
            raise ValueError(msg)
        if self.minimum >= self.maximum:
            msg = "minimum must be smaller than maximum"
            raise ValueError(msg)
        return np.linspace(self.minimum, self.maximum, self.samples)


@dataclass(frozen=True)
class Viewport2D:
    """Visible 2D coordinate window."""

    x: PlotRange = field(default_factory=PlotRange)
    y: PlotRange = field(default_factory=PlotRange)


@dataclass(frozen=True)
class PlotStyle:
    """Style for a rendered object."""

    color: str = "#1a73e8"
    linewidth: float = 2.4
    linestyle: str = "-"
    marker: str | None = None
    label: str | None = None


@dataclass(frozen=True)
class SampledCurve2D:
    """Sampled x/y curve values."""

    x: npt.NDArray[np.float64]
    y: npt.NDArray[np.float64]
    style: PlotStyle = field(default_factory=PlotStyle)


class Drawable2D(Protocol):
    """Object that can draw itself on a Matplotlib axis."""

    def draw(self, axis: Axes) -> None:
        """Draw the object on ``axis``."""


@dataclass(frozen=True)
class ExplicitFunction2D:
    """A Cartesian graph of ``y = f(x)``."""

    expression: str | sp.Expr
    variable: str = "x"
    domain: PlotRange = field(default_factory=PlotRange)
    style: PlotStyle = field(default_factory=PlotStyle)

    def sample(self) -> SampledCurve2D:
        values = self.domain.values()
        expression = MathExpression.parse(self.expression, variable=self.variable)
        return SampledCurve2D(
            x=values,
            y=expression.sample(values),
            style=self.style,
        )

    def draw(self, axis: Axes) -> None:
        curve = self.sample()
        _draw_curve(axis, curve)


@dataclass(frozen=True)
class ParametricCurve2D:
    """A parametric curve ``(x(t), y(t))``."""

    x_expression: str | sp.Expr
    y_expression: str | sp.Expr
    parameter: str = "t"
    domain: PlotRange = field(default_factory=PlotRange)
    style: PlotStyle = field(default_factory=PlotStyle)

    def sample(self) -> SampledCurve2D:
        parameter = sp.Symbol(self.parameter)
        values = self.domain.values()
        x_expr = MathExpression(
            parse_expression(self.x_expression, variables=(parameter,)),
            parameter,
        )
        y_expr = MathExpression(
            parse_expression(self.y_expression, variables=(parameter,)),
            parameter,
        )
        return SampledCurve2D(
            x=x_expr.sample(values),
            y=y_expr.sample(values),
            style=self.style,
        )

    def draw(self, axis: Axes) -> None:
        curve = self.sample()
        _draw_curve(axis, curve)


@dataclass(frozen=True)
class PolarCurve2D:
    """A polar curve ``r = f(theta)`` rendered in the Cartesian plane."""

    radius_expression: str | sp.Expr
    parameter: str = "theta"
    domain: PlotRange = field(
        default_factory=lambda: PlotRange(0, float(2 * np.pi), 400),
    )
    style: PlotStyle = field(default_factory=PlotStyle)

    def sample(self) -> SampledCurve2D:
        parameter = sp.Symbol(self.parameter)
        theta = self.domain.values()
        radius_expr = MathExpression(
            parse_expression(self.radius_expression, variables=(parameter,)),
            parameter,
        )
        radius = radius_expr.sample(theta)
        return SampledCurve2D(
            x=radius * np.cos(theta),
            y=radius * np.sin(theta),
            style=self.style,
        )

    def draw(self, axis: Axes) -> None:
        curve = self.sample()
        _draw_curve(axis, curve)


@dataclass(frozen=True)
class Point2D:
    """A point in the plane."""

    x: float
    y: float
    style: PlotStyle = field(default_factory=lambda: PlotStyle(marker="o"))

    def draw(self, axis: Axes) -> None:
        axis.plot(
            [self.x],
            [self.y],
            color=self.style.color,
            marker=self.style.marker or "o",
            label=self.style.label,
        )


@dataclass(frozen=True)
class Segment2D:
    """A segment between two points."""

    start: Point2D
    end: Point2D
    style: PlotStyle = field(default_factory=PlotStyle)

    def draw(self, axis: Axes) -> None:
        axis.plot(
            [self.start.x, self.end.x],
            [self.start.y, self.end.y],
            color=self.style.color,
            linewidth=self.style.linewidth,
            linestyle=self.style.linestyle,
            marker=self.style.marker,
            label=self.style.label,
        )


@dataclass(frozen=True)
class PlotScene2D:
    """A composed 2D plot with reusable graph elements."""

    elements: tuple[Drawable2D, ...]
    viewport: Viewport2D = field(default_factory=Viewport2D)
    title: str | None = None
    show_axes: bool = True
    show_grid: bool = True
    equal_aspect: bool = False

    def render(self, axis: Axes | None = None) -> tuple[Figure, Axes]:
        if axis is None:
            figure, axis = plt.subplots(figsize=(8, 5), constrained_layout=True)
        else:
            figure = cast(Figure, axis.figure)

        for element in self.elements:
            element.draw(axis)

        axis.set_xlim(self.viewport.x.minimum, self.viewport.x.maximum)
        axis.set_ylim(self.viewport.y.minimum, self.viewport.y.maximum)
        if self.title:
            axis.set_title(self.title)
        if self.show_axes:
            axis.axhline(0, color="#202124", linewidth=1)
            axis.axvline(0, color="#202124", linewidth=1)
        if self.show_grid:
            axis.grid(True, alpha=0.28)
        if self.equal_aspect:
            axis.set_aspect("equal")
        if any(_has_label(element) for element in self.elements):
            axis.legend()

        return figure, axis


def _draw_curve(axis: Axes, curve: SampledCurve2D) -> None:
    axis.plot(
        curve.x,
        curve.y,
        color=curve.style.color,
        linewidth=curve.style.linewidth,
        linestyle=curve.style.linestyle,
        marker=curve.style.marker,
        label=curve.style.label,
    )


def _has_label(element: Drawable2D) -> bool:
    style = getattr(element, "style", None)
    return bool(getattr(style, "label", None))
