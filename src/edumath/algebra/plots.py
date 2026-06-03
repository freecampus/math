"""College algebra plotting helpers."""

from __future__ import annotations

import sympy as sp

from edumath.core import (
    ExplicitFunction2D,
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Viewport2D,
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
                    label=f"y = {expression}",
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


__all__ = ["compare_functions_scene", "function_scene"]
