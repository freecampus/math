"""College algebra plotting helpers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import SupportsFloat, cast

import sympy as sp

from edumath.core import (
    ExplicitFunction2D,
    MathExpression,
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Point2D,
    Segment2D,
    Viewport2D,
    parse_expression,
)


def function_scene(
    expression: str | sp.Expr,
    *,
    x_min: float = -10,
    x_max: float = 10,
    y_min: float = -10,
    y_max: float = 10,
    title: str | None = None,
    color: str = "#1a73e8",
) -> PlotScene2D:
    """Create a reusable scene for a single algebraic function."""

    return PlotScene2D(
        elements=(
            ExplicitFunction2D(
                expression,
                domain=PlotRange(x_min, x_max),
                style=PlotStyle(color=color, label=f"y = {expression}"),
            ),
        ),
        viewport=Viewport2D(
            x=PlotRange(x_min, x_max),
            y=PlotRange(y_min, y_max),
        ),
        title=title or f"y = {expression}",
    )


def compare_functions_scene(
    expressions: tuple[str | sp.Expr, ...],
    *,
    labels: tuple[str, ...] | None = None,
    x_min: float = -10,
    x_max: float = 10,
    y_min: float = -10,
    y_max: float = 10,
    title: str = "Function comparison",
) -> PlotScene2D:
    """Create a scene comparing several functions."""

    colors = ("#1a73e8", "#d93025", "#137333", "#9334e6")
    return PlotScene2D(
        elements=tuple(
            ExplicitFunction2D(
                expression,
                domain=PlotRange(x_min, x_max),
                style=PlotStyle(
                    color=colors[index % len(colors)],
                    label=_label_for_expression(expression, index, labels),
                ),
            )
            for index, expression in enumerate(expressions)
        ),
        viewport=Viewport2D(
            x=PlotRange(x_min, x_max),
            y=PlotRange(y_min, y_max),
        ),
        title=title,
    )


def expression_table(
    expression: str | sp.Expr,
    inputs: Sequence[float],
    *,
    variable: str = "x",
) -> tuple[tuple[float, float], ...]:
    """Evaluate an algebraic expression on selected inputs.

    The returned table is intentionally simple so it can be displayed in tests,
    notebooks, and Quarto pages without requiring pandas.
    """

    math_expression = MathExpression.parse(expression, variable=variable)
    return tuple(
        (float(input_value), _evaluate_float(math_expression, float(input_value)))
        for input_value in inputs
    )


def input_output_scene(
    expression: str | sp.Expr,
    *,
    x_value: float,
    x_min: float = -5,
    x_max: float = 5,
    y_min: float = -5,
    y_max: float = 5,
    variable: str = "x",
    title: str | None = None,
) -> PlotScene2D:
    """Create a graph that highlights one input-output pair ``(x, f(x))``."""

    math_expression = MathExpression.parse(expression, variable=variable)
    y_value = _evaluate_float(math_expression, x_value)
    point = Point2D(
        x=x_value,
        y=y_value,
        style=PlotStyle(
            color="#d93025", marker="o", label=f"({x_value:g}, {y_value:g})"
        ),
    )
    return PlotScene2D(
        elements=(
            ExplicitFunction2D(
                expression,
                variable=variable,
                domain=PlotRange(x_min, x_max),
                style=PlotStyle(color="#1a73e8", label=f"f({variable}) = {expression}"),
            ),
            Segment2D(
                Point2D(x_value, 0),
                Point2D(x_value, y_value),
                style=PlotStyle(color="#d93025", linestyle="--", linewidth=1.8),
            ),
            Segment2D(
                Point2D(0, y_value),
                Point2D(x_value, y_value),
                style=PlotStyle(color="#d93025", linestyle="--", linewidth=1.8),
            ),
            point,
        ),
        viewport=Viewport2D(
            x=PlotRange(x_min, x_max),
            y=PlotRange(y_min, y_max),
        ),
        title=title or f"Input-output view of f({variable}) = {expression}",
    )


def transformed_expression(
    base_expression: str | sp.Expr,
    *,
    vertical_scale: float = 1,
    horizontal_scale: float = 1,
    horizontal_shift: float = 0,
    vertical_shift: float = 0,
    variable: str = "x",
) -> sp.Expr:
    """Return ``a * f(b * (x - h)) + k`` for a base expression ``f(x)``."""

    symbol = sp.Symbol(variable)
    base = parse_expression(base_expression, variables=(symbol,))
    transformed = (
        vertical_scale
        * base.subs(symbol, horizontal_scale * (symbol - horizontal_shift))
        + vertical_shift
    )
    return cast(sp.Expr, sp.expand(transformed))


def transformation_scene(
    base_expression: str | sp.Expr,
    *,
    vertical_scale: float = 1,
    horizontal_scale: float = 1,
    horizontal_shift: float = 0,
    vertical_shift: float = 0,
    x_min: float = -8,
    x_max: float = 8,
    y_min: float = -8,
    y_max: float = 8,
    variable: str = "x",
) -> PlotScene2D:
    """Compare a base function with a transformed function."""

    transformed = transformed_expression(
        base_expression,
        vertical_scale=vertical_scale,
        horizontal_scale=horizontal_scale,
        horizontal_shift=horizontal_shift,
        vertical_shift=vertical_shift,
        variable=variable,
    )
    return compare_functions_scene(
        (base_expression, transformed),
        labels=("base function", "transformed function"),
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        title="Function transformation",
    )


def _label_for_expression(
    expression: str | sp.Expr,
    index: int,
    labels: tuple[str, ...] | None,
) -> str:
    if labels is not None and index < len(labels):
        return labels[index]
    return f"y = {expression}"


def _evaluate_float(expression: MathExpression, value: float) -> float:
    return float(cast(SupportsFloat, expression.evaluate(value)))


__all__ = [
    "compare_functions_scene",
    "expression_table",
    "function_scene",
    "input_output_scene",
    "transformation_scene",
    "transformed_expression",
]
