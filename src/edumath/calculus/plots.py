"""Calculus plotting helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast

import sympy as sp
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

from edumath.calculus.derivatives import tangent_line
from edumath.core import (
    ExplicitFunction2D,
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Point2D,
    Segment2D,
    Viewport2D,
    parse_expression,
)


@dataclass(frozen=True)
class RiemannRectangle2D:
    """A rectangle used to visualize a Riemann sum."""

    left: float
    width: float
    height: float
    style: PlotStyle = field(
        default_factory=lambda: PlotStyle(color="#1a73e8", linewidth=1.2)
    )

    def draw(self, axis: Axes) -> None:
        bottom = min(0.0, self.height)
        patch = Rectangle(
            (self.left, bottom),
            self.width,
            abs(self.height),
            facecolor=self.style.color,
            edgecolor="#202124",
            linewidth=self.style.linewidth,
            alpha=0.25,
            label=self.style.label,
        )
        axis.add_patch(patch)


def secant_tangent_scene(
    expression: str | sp.Expr,
    *,
    point: float,
    step: float = 1.0,
    x_min: float | None = None,
    x_max: float | None = None,
    y_min: float = -10,
    y_max: float = 10,
    variable: str = "x",
) -> PlotScene2D:
    """Create a scene comparing a secant line with a tangent line."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    left_x = point - step
    right_x = point + step
    left_y = float(expr.subs(symbol, left_x))
    right_y = float(expr.subs(symbol, right_x))
    point_y = float(expr.subs(symbol, point))
    tangent = tangent_line(expr, point, variable=variable)
    x_lower = x_min if x_min is not None else point - 4 * step
    x_upper = x_max if x_max is not None else point + 4 * step

    return PlotScene2D(
        elements=(
            ExplicitFunction2D(
                expr,
                variable=variable,
                domain=PlotRange(x_lower, x_upper),
                style=PlotStyle(color="#1a73e8", label=f"f({variable})"),
            ),
            ExplicitFunction2D(
                tangent,
                variable=variable,
                domain=PlotRange(x_lower, x_upper),
                style=PlotStyle(color="#d93025", linestyle="--", label="tangent"),
            ),
            Segment2D(
                Point2D(left_x, left_y),
                Point2D(right_x, right_y),
                style=PlotStyle(color="#137333", linewidth=2.0, label="secant"),
            ),
            Point2D(point, point_y, style=PlotStyle(color="#d93025", marker="o")),
        ),
        viewport=Viewport2D(x=PlotRange(x_lower, x_upper), y=PlotRange(y_min, y_max)),
        title="Secant and tangent view",
    )


def riemann_sum_scene(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    rectangles: int,
    *,
    method: str = "midpoint",
    y_min: float = -1,
    y_max: float = 5,
    variable: str = "x",
) -> PlotScene2D:
    """Create a scene showing Riemann rectangles under a curve."""

    if rectangles <= 0:
        msg = "rectangles must be positive"
        raise ValueError(msg)

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    width = (upper - lower) / rectangles
    offsets = {"left": 0.0, "midpoint": 0.5, "right": 1.0}
    if method not in offsets:
        msg = "method must be 'left', 'midpoint', or 'right'"
        raise ValueError(msg)
    offset = offsets[method]
    rects = tuple(
        RiemannRectangle2D(
            left=lower + index * width,
            width=width,
            height=float(function(lower + (index + offset) * width)),
        )
        for index in range(rectangles)
    )

    return PlotScene2D(
        elements=(
            *rects,
            ExplicitFunction2D(
                expr,
                variable=variable,
                domain=PlotRange(lower, upper),
                style=PlotStyle(color="#d93025", label=f"f({variable})"),
            ),
        ),
        viewport=Viewport2D(x=PlotRange(lower, upper), y=PlotRange(y_min, y_max)),
        title=f"{method.title()} Riemann sum",
    )


def derivative_sign_scene(
    expression: str | sp.Expr,
    *,
    x_min: float = -5,
    x_max: float = 5,
    y_min: float = -10,
    y_max: float = 10,
    variable: str = "x",
) -> PlotScene2D:
    """Create a scene comparing a function and its derivative."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    derivative_expr = cast(sp.Expr, sp.diff(expr, symbol))
    return PlotScene2D(
        elements=(
            ExplicitFunction2D(
                expr,
                variable=variable,
                domain=PlotRange(x_min, x_max),
                style=PlotStyle(color="#1a73e8", label="function"),
            ),
            ExplicitFunction2D(
                derivative_expr,
                variable=variable,
                domain=PlotRange(x_min, x_max),
                style=PlotStyle(color="#d93025", label="derivative"),
            ),
        ),
        viewport=Viewport2D(x=PlotRange(x_min, x_max), y=PlotRange(y_min, y_max)),
        title="Function and derivative",
    )


def optimization_scene(
    expression: str | sp.Expr,
    *,
    candidates: tuple[float, ...],
    x_min: float = -5,
    x_max: float = 5,
    y_min: float = -10,
    y_max: float = 10,
    variable: str = "x",
) -> PlotScene2D:
    """Create a function scene with optimization candidates marked."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    points = tuple(
        Point2D(
            candidate,
            float(expr.subs(symbol, candidate)),
            style=PlotStyle(color="#d93025", marker="o", label="candidate"),
        )
        for candidate in candidates
    )
    return PlotScene2D(
        elements=(
            ExplicitFunction2D(
                expr,
                variable=variable,
                domain=PlotRange(x_min, x_max),
                style=PlotStyle(color="#1a73e8", label="function"),
            ),
            *points,
        ),
        viewport=Viewport2D(x=PlotRange(x_min, x_max), y=PlotRange(y_min, y_max)),
        title="Optimization candidates",
    )


accumulation_scene = riemann_sum_scene

__all__ = [
    "RiemannRectangle2D",
    "accumulation_scene",
    "derivative_sign_scene",
    "optimization_scene",
    "riemann_sum_scene",
    "secant_tangent_scene",
]
