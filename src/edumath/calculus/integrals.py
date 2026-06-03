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


__all__ = ["antiderivative", "definite_integral", "midpoint_riemann_sum"]
