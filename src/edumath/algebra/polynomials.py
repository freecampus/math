"""Reusable helpers for polynomial lessons."""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import sympy as sp

from edumath.algebra.plots import function_scene
from edumath.core import PlotScene2D, PlotStyle, Point2D, parse_expression

X = sp.Symbol("x")


@dataclass(frozen=True)
class PolynomialSummary:
    """Important symbolic facts about one polynomial."""

    expression: sp.Expr
    variable: sp.Symbol = X

    @property
    def degree(self) -> int:
        """Return the degree of the polynomial."""

        return int(sp.degree(self.expression, self.variable))

    @property
    def leading_coefficient(self) -> sp.Expr:
        """Return the leading coefficient."""

        polynomial = sp.Poly(self.expression, self.variable)
        return cast(sp.Expr, polynomial.LC())

    @property
    def factored(self) -> sp.Expr:
        """Return a factored form."""

        return cast(sp.Expr, sp.factor(self.expression))

    @property
    def roots(self) -> tuple[sp.Expr, ...]:
        """Return exact roots when SymPy can solve them."""

        return tuple(
            cast(sp.Expr, root) for root in sp.solve(self.expression, self.variable)
        )

    @property
    def root_multiplicities(self) -> tuple[tuple[sp.Expr, int], ...]:
        """Return roots with multiplicities."""

        roots = sp.roots(self.expression, self.variable)
        return tuple(
            (cast(sp.Expr, root), int(multiplicity))
            for root, multiplicity in roots.items()
        )


def polynomial_summary(
    expression: str | sp.Expr,
    *,
    variable: str | sp.Symbol = X,
) -> PolynomialSummary:
    """Summarize a polynomial expression."""

    symbol = sp.Symbol(variable) if isinstance(variable, str) else variable
    parsed = parse_expression(expression, variables=(symbol,))
    return PolynomialSummary(cast(sp.Expr, sp.expand(parsed)), variable=symbol)


def polynomial_from_roots(
    roots: tuple[float | int | sp.Expr, ...],
    *,
    leading_coefficient: float | int | sp.Expr = 1,
    variable: sp.Symbol = X,
) -> sp.Expr:
    """Create an expanded polynomial from roots."""

    expression = sp.sympify(leading_coefficient)
    for root in roots:
        expression *= variable - root
    return cast(sp.Expr, sp.expand(expression))


def polynomial_root_scene(
    expression: str | sp.Expr,
    *,
    x_min: float = -6,
    x_max: float = 6,
    y_min: float = -10,
    y_max: float = 10,
    variable: str | sp.Symbol = X,
) -> PlotScene2D:
    """Create a polynomial plot with real roots highlighted."""

    symbol = sp.Symbol(variable) if isinstance(variable, str) else variable
    summary = polynomial_summary(expression, variable=symbol)
    real_root_points = tuple(
        Point2D(
            float(root),
            0,
            style=PlotStyle(color="#d93025", marker="o", label=f"root {sp.sstr(root)}"),
        )
        for root in summary.roots
        if bool(root.is_real)
    )
    base = function_scene(
        summary.expression,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        title=f"Polynomial roots for y = {sp.sstr(summary.expression)}",
    )
    return PlotScene2D(
        elements=(*base.elements, *real_root_points),
        viewport=base.viewport,
        title=base.title,
    )


__all__ = [
    "PolynomialSummary",
    "polynomial_from_roots",
    "polynomial_root_scene",
    "polynomial_summary",
]
