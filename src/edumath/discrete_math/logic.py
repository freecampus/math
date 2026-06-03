"""Discrete mathematics logic helpers."""

from __future__ import annotations

from collections.abc import Callable
from itertools import product

TruthFunction = Callable[..., bool]


def truth_table(
    variables: tuple[str, ...],
    function: TruthFunction,
) -> list[dict[str, bool]]:
    """Return truth assignments plus the result of a Boolean function."""

    rows: list[dict[str, bool]] = []
    for values in product((False, True), repeat=len(variables)):
        row = dict(zip(variables, values, strict=True))
        row["result"] = bool(function(*values))
        rows.append(row)
    return rows


def implies(left: bool, right: bool) -> bool:
    """Return logical implication ``left -> right``."""

    return (not left) or right


__all__ = ["TruthFunction", "implies", "truth_table"]
