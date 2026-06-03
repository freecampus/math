"""Expression parsing and evaluation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt
import sympy as sp

DEFAULT_SYMBOLS: dict[str, Any] = {
    "pi": sp.pi,
    "e": sp.E,
    "E": sp.E,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sec": sp.sec,
    "csc": sp.csc,
    "cot": sp.cot,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "sqrt": sp.sqrt,
    "exp": sp.exp,
    "log": sp.log,
    "ln": sp.log,
    "abs": sp.Abs,
}


@dataclass(frozen=True)
class MathExpression:
    """Parsed symbolic expression with a preferred variable."""

    expression: sp.Expr
    variable: sp.Symbol

    @classmethod
    def parse(
        cls,
        source: str | sp.Expr,
        *,
        variable: str | sp.Symbol = "x",
    ) -> MathExpression:
        symbol = sp.Symbol(variable) if isinstance(variable, str) else variable
        return cls(
            expression=parse_expression(source, variables=(symbol,)),
            variable=symbol,
        )

    def evaluate(self, values: float | npt.NDArray[np.float64]) -> Any:
        function = sp.lambdify(self.variable, self.expression, "numpy")
        return function(values)

    def sample(
        self,
        values: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]:
        result = self.evaluate(values)
        if np.isscalar(result):
            return np.full_like(values, result, dtype=float)

        sampled = np.asarray(result, dtype=float)
        if sampled.shape != values.shape:
            sampled = np.broadcast_to(sampled, values.shape).astype(float)
        return np.where(np.isfinite(sampled), sampled, np.nan)

    def equivalent_to(self, other: str | sp.Expr | MathExpression) -> bool:
        other_expr = other.expression if isinstance(other, MathExpression) else other
        return expression_equivalent(self.expression, other_expr)


def parse_expression(
    source: str | sp.Expr,
    *,
    variables: tuple[sp.Symbol, ...] = (sp.Symbol("x"),),
) -> sp.Expr:
    """Parse a math expression string into a SymPy expression."""

    if isinstance(source, sp.Expr):
        return source

    local_dict = DEFAULT_SYMBOLS.copy()
    local_dict.update({symbol.name: symbol for symbol in variables})
    return sp.sympify(source, locals=local_dict)


def expression_equivalent(
    left: str | sp.Expr,
    right: str | sp.Expr,
    *,
    variables: tuple[sp.Symbol, ...] = (sp.Symbol("x"),),
) -> bool:
    """Return true when two expressions simplify to the same expression."""

    left_expr = parse_expression(left, variables=variables)
    right_expr = parse_expression(right, variables=variables)
    return bool(sp.simplify(left_expr - right_expr) == 0)
