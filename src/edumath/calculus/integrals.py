"""Integral helpers for calculus lessons."""

from __future__ import annotations

import sympy as sp

from edumath.core import parse_expression


def antiderivative(expression: str | sp.Expr, *, variable: str = "x") -> sp.Expr:
    """Return a symbolic antiderivative."""

    symbol = sp.Symbol(variable)
    return sp.integrate(parse_expression(expression, variables=(symbol,)), symbol)


def definite_integral(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    *,
    variable: str = "x",
) -> sp.Expr:
    """Return a symbolic definite integral."""

    symbol = sp.Symbol(variable)
    return sp.integrate(
        parse_expression(expression, variables=(symbol,)),
        (symbol, lower, upper),
    )


def midpoint_riemann_sum(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    rectangles: int,
    *,
    variable: str = "x",
) -> float:
    """Approximate an integral with midpoint rectangles."""

    if rectangles <= 0:
        msg = "rectangles must be positive"
        raise ValueError(msg)

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    width = (upper - lower) / rectangles
    return float(
        sum(
            function(lower + (index + 0.5) * width) * width
            for index in range(rectangles)
        )
    )


__all__ = [
    "antiderivative",
    "definite_integral",
    "left_riemann_sum",
    "midpoint_riemann_sum",
    "right_riemann_sum",
    "trapezoid_rule",
]


def left_riemann_sum(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    rectangles: int,
    *,
    variable: str = "x",
) -> float:
    """Approximate an integral with left-endpoint rectangles."""

    return _endpoint_riemann_sum(
        expression,
        lower,
        upper,
        rectangles,
        offset=0.0,
        variable=variable,
    )


def right_riemann_sum(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    rectangles: int,
    *,
    variable: str = "x",
) -> float:
    """Approximate an integral with right-endpoint rectangles."""

    return _endpoint_riemann_sum(
        expression,
        lower,
        upper,
        rectangles,
        offset=1.0,
        variable=variable,
    )


def trapezoid_rule(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    intervals: int,
    *,
    variable: str = "x",
) -> float:
    """Approximate an integral with the trapezoid rule."""

    if intervals <= 0:
        msg = "intervals must be positive"
        raise ValueError(msg)

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    width = (upper - lower) / intervals
    total = 0.5 * (function(lower) + function(upper))
    total += sum(function(lower + index * width) for index in range(1, intervals))
    return float(total * width)


def _endpoint_riemann_sum(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    rectangles: int,
    *,
    offset: float,
    variable: str,
) -> float:
    if rectangles <= 0:
        msg = "rectangles must be positive"
        raise ValueError(msg)

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    width = (upper - lower) / rectangles
    return float(
        sum(
            function(lower + (index + offset) * width) * width
            for index in range(rectangles)
        )
    )
