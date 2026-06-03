"""College algebra answer validators."""

from __future__ import annotations

import sympy as sp

from edumath.core import AnswerCheck, check_expression_answer, check_numeric_answer


def validate_expression_equivalence(
    received: str | sp.Expr,
    expected: str | sp.Expr,
) -> AnswerCheck:
    """Validate that two algebraic expressions are equivalent."""

    return check_expression_answer(received, expected)


def validate_numeric_solution(received: float, expected: float) -> AnswerCheck:
    """Validate a numeric algebra solution."""

    return check_numeric_answer(received, expected)


__all__ = ["validate_expression_equivalence", "validate_numeric_solution"]
