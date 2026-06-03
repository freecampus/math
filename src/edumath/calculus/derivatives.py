"""Derivative helpers for calculus lessons."""

from __future__ import annotations

import sympy as sp

from edumath.core import parse_expression


def derivative(expression: str | sp.Expr, *, variable: str = "x") -> sp.Expr:
    """Return the symbolic derivative of an expression."""

    symbol = sp.Symbol(variable)
    return sp.diff(parse_expression(expression, variables=(symbol,)), symbol)


def tangent_line(
    expression: str | sp.Expr,
    point: float,
    *,
    variable: str = "x",
) -> sp.Expr:
    """Return the tangent line at one input value."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    slope = sp.diff(expr, symbol).subs(symbol, point)
    y_value = expr.subs(symbol, point)
    return sp.expand(slope * (symbol - point) + y_value)


def finite_difference(
    expression: str | sp.Expr,
    point: float,
    *,
    step: float = 1e-5,
    variable: str = "x",
) -> float:
    """Approximate a derivative with a centered finite difference."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    return float((function(point + step) - function(point - step)) / (2 * step))


__all__ = ["derivative", "finite_difference", "tangent_line"]
