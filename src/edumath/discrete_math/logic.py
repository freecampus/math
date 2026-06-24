"""Discrete mathematics logic helpers."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from itertools import product
from typing import Any, cast

import sympy as sp

TruthFunction = Callable[..., bool]
TruthRow = dict[str, bool]


def truth_table(
    variables: tuple[str, ...],
    function: TruthFunction,
) -> list[TruthRow]:
    """Return truth assignments plus the result of a Boolean function."""

    rows: list[TruthRow] = []
    for values in product((False, True), repeat=len(variables)):
        row = dict(zip(variables, values, strict=True))
        row["result"] = bool(function(*values))
        rows.append(row)
    return rows


def truth_table_rows(variables: tuple[str, ...], expression: str) -> list[TruthRow]:
    """Return a truth table for a simple SymPy Boolean expression string."""

    symbols = {name: sp.Symbol(name) for name in variables}
    expr = sp.sympify(expression, locals=symbols)
    rows: list[TruthRow] = []
    for values in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, values, strict=True))
        substitutions = {symbols[name]: value for name, value in assignment.items()}
        result = bool(expr.subs(substitutions))
        rows.append({**assignment, "result": result})
    return rows


def not_(value: bool) -> bool:
    """Return logical negation."""

    return not value


def and_(*values: bool) -> bool:
    """Return logical conjunction of all values."""

    return all(values)


def or_(*values: bool) -> bool:
    """Return inclusive logical disjunction of all values."""

    return any(values)


def xor(left: bool, right: bool) -> bool:
    """Return exclusive or."""

    return left != right


def implies(left: bool, right: bool) -> bool:
    """Return logical implication ``left -> right``."""

    return (not left) or right


def iff(left: bool, right: bool) -> bool:
    """Return biconditional truth value."""

    return left == right


def is_tautology(rows: Sequence[Mapping[str, bool]]) -> bool:
    """Return whether every row has result true."""

    return all(row.get("result", False) for row in rows)


def is_contradiction(rows: Sequence[Mapping[str, bool]]) -> bool:
    """Return whether every row has result false."""

    return all(not row.get("result", False) for row in rows)


def is_equivalent(
    function_a: TruthFunction,
    function_b: TruthFunction,
    variables: tuple[str, ...],
) -> bool:
    """Return whether two truth functions agree on every truth assignment."""

    for values in product((False, True), repeat=len(variables)):
        args = cast(tuple[Any, ...], values)
        if bool(function_a(*args)) != bool(function_b(*args)):
            return False
    return True


__all__ = [
    "TruthFunction",
    "TruthRow",
    "and_",
    "iff",
    "implies",
    "is_contradiction",
    "is_equivalent",
    "is_tautology",
    "not_",
    "or_",
    "truth_table",
    "truth_table_rows",
    "xor",
]
