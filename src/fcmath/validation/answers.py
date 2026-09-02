"""Safe, policy-driven validation for mathematical learner answers."""

from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass, field
from typing import Literal, cast

import sympy as sp

from fcmath.core.answers import AnswerCheck, NumericTolerance, check_numeric_answer
from fcmath.core.expressions import (
    DEFAULT_EXPRESSION_LIMITS,
    ExpressionLimits,
    parse_expression,
)

ValidationMode = Literal[
    "exact",
    "numeric",
    "symbolic-equivalence",
    "set-equality",
    "solution-set",
    "interval",
    "matrix",
    "normalized-output",
]
AlgebraicForm = Literal["any", "expanded", "factored"]
DomainName = Literal["real", "complex", "integer"]


@dataclass(frozen=True)
class ValidationPolicy:
    """Declarative rules for checking one answer without executing learner code."""

    mode: ValidationMode
    variables: tuple[str, ...] = ()
    domain: DomainName = "real"
    tolerance: NumericTolerance = field(default_factory=NumericTolerance)
    algebraic_form: AlgebraicForm = "any"
    matrix_shape: tuple[int, int] | None = None
    units: str | None = None
    units_required: bool = False
    expression_limits: ExpressionLimits = field(default_factory=ExpressionLimits)

    def __post_init__(self) -> None:
        """Validate policy semantics before any learner answer is checked."""

        modes = {
            "exact",
            "numeric",
            "symbolic-equivalence",
            "set-equality",
            "solution-set",
            "interval",
            "matrix",
            "normalized-output",
        }
        if self.mode not in modes:
            raise ValueError(f"unsupported validation mode {self.mode!r}")
        if self.domain not in _ALLOWED_DOMAINS:
            raise ValueError(f"unsupported mathematical domain {self.domain!r}")
        if self.algebraic_form not in {"any", "expanded", "factored"}:
            raise ValueError(f"unsupported algebraic form {self.algebraic_form!r}")
        if any(
            not re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", name) for name in self.variables
        ):
            raise ValueError("variables must use ordinary mathematical identifiers")
        if len(set(self.variables)) != len(self.variables):
            raise ValueError("variables must be unique")
        if self.matrix_shape is not None and (
            len(self.matrix_shape) != 2 or any(size < 1 for size in self.matrix_shape)
        ):
            raise ValueError("matrix_shape must contain two positive dimensions")
        if self.units_required and not self.units:
            raise ValueError("units_required needs a declared unit")


_ALLOWED_DOMAINS: dict[DomainName, sp.Set] = {
    "real": sp.S.Reals,
    "complex": sp.S.Complexes,
    "integer": sp.S.Integers,
}
_UNIT_ANSWER = re.compile(
    r"^\s*(?P<value>.*?)\s*(?P<unit>[A-Za-z][A-Za-z0-9*/^ -]*)?\s*$"
)


def check_answer(
    received: object,
    expected: object,
    policy: ValidationPolicy,
) -> AnswerCheck:
    """Validate ``received`` according to an explicit mathematical policy."""

    try:
        received_value = _strip_units(received, policy)
        if policy.mode == "numeric":
            return _check_numeric(received_value, expected, policy)
        if policy.mode == "symbolic-equivalence":
            return _check_symbolic(received_value, expected, policy)
        if policy.mode in {"solution-set", "interval"}:
            return _check_solution_set(received_value, expected, policy)
        if policy.mode == "matrix":
            return _check_matrix(received_value, expected, policy)
        if policy.mode == "set-equality":
            correct = _as_hashable_set(received_value) == _as_hashable_set(expected)
        elif policy.mode == "normalized-output":
            correct = _normalize_output(received_value) == _normalize_output(expected)
        else:
            correct = received_value == expected
    except (TypeError, ValueError, SyntaxError, sp.SympifyError) as error:
        return AnswerCheck(
            False, received, expected, f"Could not check answer: {error}"
        )

    message = (
        "Correct." if correct else "The answer does not satisfy the required policy."
    )
    return AnswerCheck(correct, received, expected, message)


def parse_solution_set(
    source: str | sp.Set,
    *,
    variables: tuple[str, ...] = (),
    limits: ExpressionLimits = DEFAULT_EXPRESSION_LIMITS,
) -> sp.Set:
    """Parse finite sets and real interval notation without arbitrary evaluation."""

    if isinstance(source, sp.Set):
        return source
    text = source.strip().replace("∞", "oo")
    if not text:
        raise ValueError("solution set must not be empty")
    if text in {"empty", "emptyset", "∅", "{}"}:
        return sp.EmptySet
    if text in {"R", "Reals", "real", "all real numbers", "(-oo,oo)"}:
        return sp.S.Reals

    union_parts = re.split(r"\s*(?:U|\u222a)\s*", text)
    if len(union_parts) > 1:
        return sp.Union(
            *(
                parse_solution_set(part, variables=variables, limits=limits)
                for part in union_parts
            )
        )

    interval_match = re.fullmatch(r"(\[|\()\s*(.*?)\s*,\s*(.*?)\s*(\]|\))", text)
    if interval_match:
        left_bracket, left_text, right_text, right_bracket = interval_match.groups()
        left = _parse_endpoint(left_text, variables, limits)
        right = _parse_endpoint(right_text, variables, limits)
        return sp.Interval(
            left,
            right,
            left_open=left_bracket == "(",
            right_open=right_bracket == ")",
        )

    if text.startswith("{") and text.endswith("}"):
        body = text[1:-1].strip()
        if not body:
            return sp.EmptySet
        values = [
            parse_expression(
                part,
                variables=tuple(sp.Symbol(name) for name in variables),
                limits=limits,
            )
            for part in body.split(",")
        ]
        return sp.FiniteSet(*values)

    expression = parse_expression(
        text,
        variables=tuple(sp.Symbol(name) for name in variables),
        limits=limits,
    )
    return sp.FiniteSet(expression)


def _check_numeric(
    received: object,
    expected: object,
    policy: ValidationPolicy,
) -> AnswerCheck:
    received_number = _numeric_value(received, policy)
    expected_number = _numeric_value(expected, policy)
    return check_numeric_answer(
        received_number,
        expected_number,
        tolerance=policy.tolerance,
    )


def _numeric_value(value: object, policy: ValidationPolicy) -> float:
    if isinstance(value, bool):
        raise TypeError("a Boolean is not a numeric answer")
    if isinstance(value, int | float):
        result = float(value)
    elif isinstance(value, sp.Basic):
        if value.free_symbols or value.is_number is not True:
            raise ValueError("numeric answer contains a variable")
        result = float(value)
    elif isinstance(value, str):
        expression = parse_expression(
            value,
            variables=(),
            limits=policy.expression_limits,
        )
        if expression.free_symbols or expression.is_number is not True:
            raise ValueError("numeric answer contains a variable")
        result = float(expression)
    else:
        raise TypeError("numeric answer must be a number or mathematical expression")
    if not math.isfinite(result):
        raise ValueError("numeric answer must be finite")
    return result


def _check_symbolic(
    received: object,
    expected: object,
    policy: ValidationPolicy,
) -> AnswerCheck:
    symbols = tuple(sp.Symbol(name) for name in policy.variables)
    received_expression = parse_expression(
        cast(str | sp.Expr, received),
        variables=symbols,
        evaluate=policy.algebraic_form == "any",
        limits=policy.expression_limits,
    )
    expected_expression = parse_expression(
        cast(str | sp.Expr, expected),
        variables=symbols,
        limits=policy.expression_limits,
    )
    declared = set(symbols)
    if received_expression.free_symbols - declared:
        unexpected = ", ".join(
            sorted(
                symbol.name for symbol in received_expression.free_symbols - declared
            )
        )
        raise ValueError(f"undeclared variable(s): {unexpected}")

    equivalent = bool(sp.simplify(received_expression - expected_expression) == 0)
    form_valid = True
    if policy.algebraic_form == "expanded":
        form_valid = received_expression == sp.expand(received_expression)
    elif policy.algebraic_form == "factored":
        form_valid = received_expression == sp.factor(received_expression)
    correct = equivalent and form_valid
    if correct:
        message = "Correct."
    elif equivalent:
        message = (
            f"Equivalent, but the requested {policy.algebraic_form} form is missing."
        )
    else:
        message = (
            "The expression is not mathematically equivalent to the expected answer."
        )
    return AnswerCheck(correct, received, expected, message)


def _check_solution_set(
    received: object,
    expected: object,
    policy: ValidationPolicy,
) -> AnswerCheck:
    received_set = parse_solution_set(
        cast(str | sp.Set, received),
        variables=policy.variables,
        limits=policy.expression_limits,
    )
    expected_set = parse_solution_set(
        cast(str | sp.Set, expected),
        variables=policy.variables,
        limits=policy.expression_limits,
    )
    domain = _ALLOWED_DOMAINS[policy.domain]
    correct = received_set.intersect(domain) == expected_set.intersect(domain)
    message = "Correct." if correct else "The solution set is not equivalent."
    return AnswerCheck(correct, received, expected, message)


def _check_matrix(
    received: object,
    expected: object,
    policy: ValidationPolicy,
) -> AnswerCheck:
    received_matrix = _matrix(received)
    expected_matrix = _matrix(expected)
    if policy.matrix_shape is not None and received_matrix.shape != policy.matrix_shape:
        rows, columns = policy.matrix_shape
        return AnswerCheck(
            False,
            received,
            expected,
            f"Expected a {rows} by {columns} matrix; received {received_matrix.shape}.",
        )
    correct = received_matrix.shape == expected_matrix.shape and all(
        sp.simplify(left - right) == 0
        for left, right in zip(received_matrix, expected_matrix, strict=True)
    )
    message = "Correct." if correct else "The matrix shape or entries differ."
    return AnswerCheck(correct, received, expected, message)


def _matrix(value: object) -> sp.Matrix:
    if isinstance(value, sp.MatrixBase):
        return sp.Matrix(value)
    data = ast.literal_eval(value) if isinstance(value, str) else value
    if not isinstance(data, list | tuple):
        raise TypeError("matrix answer must be a nested list")
    matrix = sp.Matrix(data)
    if matrix.rows * matrix.cols > 400:
        raise ValueError("matrix answer is too large")
    return matrix


def _strip_units(received: object, policy: ValidationPolicy) -> object:
    if policy.units is None:
        return received
    if not isinstance(received, str):
        if policy.units_required:
            raise ValueError(f"include the required unit {policy.units!r}")
        return received
    match = _UNIT_ANSWER.fullmatch(received)
    if match is None:
        raise ValueError("could not separate the value and unit")
    unit = (match.group("unit") or "").strip()
    if unit and unit != policy.units:
        raise ValueError(f"expected unit {policy.units!r}, received {unit!r}")
    if policy.units_required and not unit:
        raise ValueError(f"include the required unit {policy.units!r}")
    return match.group("value")


def _parse_endpoint(
    text: str,
    variables: tuple[str, ...],
    limits: ExpressionLimits,
) -> sp.Expr:
    normalized = text.strip()
    if normalized in {"-oo", "-inf", "-infinity"}:
        return cast(sp.Expr, -sp.oo)
    if normalized in {"oo", "+oo", "inf", "+inf", "infinity", "+infinity"}:
        return cast(sp.Expr, sp.oo)
    return parse_expression(
        normalized,
        variables=tuple(sp.Symbol(name) for name in variables),
        limits=limits,
    )


def _as_hashable_set(value: object) -> frozenset[object]:
    if isinstance(value, str):
        return frozenset(part.strip() for part in value.split(",") if part.strip())
    if isinstance(value, list | tuple | set | frozenset):
        return frozenset(value)
    raise TypeError("set answer must be a collection")


def _normalize_output(value: object) -> str:
    return " ".join(str(value).strip().split())
