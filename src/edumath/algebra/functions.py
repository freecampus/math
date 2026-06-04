"""Reusable helpers for linear and quadratic functions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import sympy as sp

X = sp.Symbol("x")


@dataclass(frozen=True)
class LinearModel:
    """A line written as ``y = slope*x + intercept``."""

    slope: sp.Expr
    intercept: sp.Expr
    variable: sp.Symbol = X

    @property
    def expression(self) -> sp.Expr:
        """Return the symbolic expression for the line."""

        return cast(sp.Expr, self.slope * self.variable + self.intercept)

    def evaluate(self, value: float) -> float:
        """Evaluate the line at one input."""

        return float(self.expression.subs(self.variable, value))


@dataclass(frozen=True)
class QuadraticModel:
    """A quadratic model with useful derived quantities."""

    a: sp.Expr
    b: sp.Expr
    c: sp.Expr
    variable: sp.Symbol = X

    @property
    def expression(self) -> sp.Expr:
        """Return ``a*x**2 + b*x + c``."""

        x = self.variable
        a, b, c = _quadratic_coefficients(self)
        return cast(sp.Expr, a * x**2 + b * x + c)

    @property
    def discriminant(self) -> sp.Expr:
        """Return ``b**2 - 4*a*c``."""

        a, b, c = _quadratic_coefficients(self)
        return cast(sp.Expr, sp.expand(b**2 - 4 * a * c))

    @property
    def vertex(self) -> tuple[sp.Expr, sp.Expr]:
        """Return the vertex ``(h, k)``."""

        a, b, _c = _quadratic_coefficients(self)
        h = cast(sp.Expr, -b / (2 * a))
        k = cast(sp.Expr, sp.simplify(self.expression.subs(self.variable, h)))
        return h, k

    @property
    def roots(self) -> tuple[sp.Expr, ...]:
        """Return exact roots when SymPy can solve them."""

        return tuple(
            cast(sp.Expr, root) for root in sp.solve(self.expression, self.variable)
        )


def line_from_points(
    first: tuple[float, float],
    second: tuple[float, float],
    *,
    variable: sp.Symbol = X,
) -> LinearModel:
    """Return the line passing through two points."""

    x1, y1 = first
    x2, y2 = second
    if x1 == x2:
        msg = "x-coordinates must be different for a non-vertical line"
        raise ValueError(msg)

    slope = sp.Rational(str(y2 - y1)) / sp.Rational(str(x2 - x1))
    intercept = sp.Rational(str(y1)) - slope * sp.Rational(str(x1))
    return LinearModel(
        slope=cast(sp.Expr, sp.simplify(slope)),
        intercept=cast(sp.Expr, sp.simplify(intercept)),
        variable=variable,
    )


def quadratic_from_vertex(
    *,
    a: float | int | sp.Expr,
    h: float | int | sp.Expr,
    k: float | int | sp.Expr,
    variable: sp.Symbol = X,
) -> sp.Expr:
    """Return the expanded expression for ``a*(x-h)**2 + k``."""

    return cast(sp.Expr, sp.expand(a * (variable - h) ** 2 + k))


def _quadratic_coefficients(model: QuadraticModel) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    return (
        cast(sp.Expr, sp.sympify(model.a)),
        cast(sp.Expr, sp.sympify(model.b)),
        cast(sp.Expr, sp.sympify(model.c)),
    )


__all__ = [
    "LinearModel",
    "QuadraticModel",
    "line_from_points",
    "quadratic_from_vertex",
]
