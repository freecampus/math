"""Expression parsing and evaluation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
import numpy.typing as npt
import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

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

_PARSE_TRANSFORMATIONS = (
    *standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


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
    evaluate: bool = True,
) -> sp.Expr:
    """Parse a math expression string into a SymPy expression.

    The parser accepts common classroom input such as implicit multiplication
    (``2x``) and ``^`` for powers. Unknown names are converted to SymPy symbols;
    known names such as ``sin``, ``sqrt``, ``pi``, and ``e`` keep their usual
    mathematical meaning.
    """

    if isinstance(source, sp.Expr):
        return source

    parsed = parse_expr(
        source.strip(),
        local_dict=_local_symbols(variables),
        transformations=_PARSE_TRANSFORMATIONS,
        evaluate=evaluate,
    )
    return cast(sp.Expr, parsed)


def parse_equation(
    source: str | sp.Equality | sp.Expr,
    *,
    variables: tuple[sp.Symbol, ...] = (),
    evaluate: bool = False,
) -> sp.Equality:
    """Parse text into a SymPy equality outside the solver layer.

    Text may be written as ``"2(x - 3) + 4 = 10"``. If the text does not
    contain an equals sign, it is interpreted as ``expression = 0``. SymPy
    expressions are also accepted and interpreted as ``expression = 0``.
    """

    if isinstance(source, sp.Equality):
        return source
    if isinstance(source, sp.Expr):
        return sp.Eq(source, 0, evaluate=evaluate)

    text = source.strip()
    if not text:
        msg = "equation text must not be empty"
        raise ValueError(msg)

    if "=" not in text:
        left = parse_expression(text, variables=variables, evaluate=evaluate)
        return sp.Eq(left, 0, evaluate=evaluate)

    parts = text.split("=")
    if len(parts) != 2:
        msg = "equation text must contain exactly one equals sign"
        raise ValueError(msg)

    left_text, right_text = parts
    left = parse_expression(left_text, variables=variables, evaluate=evaluate)
    right = parse_expression(right_text, variables=variables, evaluate=evaluate)
    return sp.Eq(left, right, evaluate=evaluate)


def infer_variable(
    source: sp.Basic,
    variable: str | sp.Symbol | None = None,
) -> sp.Symbol:
    """Infer the solving variable from a SymPy object.

    When ``variable`` is omitted, the source must contain exactly one free
    symbol. If the source has no symbols or more than one symbol, pass the
    intended variable explicitly.
    """

    if variable is not None:
        return sp.Symbol(variable) if isinstance(variable, str) else variable

    symbols = tuple(sorted(source.free_symbols, key=sp.default_sort_key))
    if len(symbols) == 1:
        return symbols[0]
    if not symbols:
        msg = "cannot infer a variable from an expression with no symbols"
        raise ValueError(msg)

    names = ", ".join(symbol.name for symbol in symbols)
    msg = f"expected exactly one free symbol; found {names}. Pass variable=..."
    raise ValueError(msg)


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


def _local_symbols(variables: tuple[sp.Symbol, ...]) -> dict[str, Any]:
    local_dict = DEFAULT_SYMBOLS.copy()
    local_dict.update({symbol.name: symbol for symbol in variables})
    return local_dict
