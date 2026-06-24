"""Step-by-step helpers for beginner calculus walkthroughs."""

from __future__ import annotations

import ast
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, cast

import sympy as sp

from edumath.calculus.derivatives import tangent_line
from edumath.core import SolutionStep, WorkedSolution, parse_expression

RiemannMethod = Literal["left", "midpoint", "right"]


@dataclass(frozen=True)
class RiemannSumRow:
    """One row in a Riemann-sum table."""

    index: int
    left: float
    right: float
    sample: float
    height: float
    width: float
    area: float


@dataclass(frozen=True)
class OptimizationCandidate:
    """One candidate point for an optimization comparison table."""

    location: sp.Expr
    value: sp.Expr
    source: str


def limit_factor_cancel_steps(
    expression: str | sp.Expr,
    point: float,
    *,
    variable: str = "x",
) -> WorkedSolution:
    """Return a beginner walkthrough for a factor-and-cancel limit."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    direct = sp.simplify(expr.subs(symbol, point))
    factored = sp.factor(expr)
    simplified = sp.cancel(expr)
    limit_value = sp.limit(expr, symbol, point)
    return WorkedSolution(
        answer=sp.sstr(limit_value),
        hint="Try substitution first; if you see 0/0, simplify before substituting.",
        explanation=(
            "A removable-hole limit depends on nearby values, "
            "not the missing point itself."
        ),
        steps=(
            SolutionStep(
                "Substitute first",
                (
                    f"Direct substitution gives {sp.sstr(direct)}, so direct "
                    "substitution needs review."
                ),
            ),
            SolutionStep(
                "Factor or cancel",
                f"Rewrite the expression as {sp.sstr(factored)}.",
            ),
            SolutionStep(
                "Simplify nearby formula",
                (
                    f"For {variable} not equal to {point}, this simplifies "
                    f"to {sp.sstr(simplified)}."
                ),
            ),
            SolutionStep(
                "Substitute into the simplified expression",
                (
                    f"Now let {variable} approach {point}: the value "
                    f"approaches {sp.sstr(limit_value)}."
                ),
            ),
        ),
        check="Use SymPy limit or evaluate the simplified expression near the point.",
    )


def tangent_line_steps(
    expression: str | sp.Expr,
    point: float,
    *,
    variable: str = "x",
) -> WorkedSolution:
    """Return a step-by-step tangent-line walkthrough."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    derivative_expr = sp.diff(expr, symbol)
    slope = sp.simplify(derivative_expr.subs(symbol, point))
    y_value = sp.simplify(expr.subs(symbol, point))
    line = tangent_line(expr, point, variable=variable)
    return WorkedSolution(
        answer=sp.sstr(line),
        hint="A tangent line needs a point and a slope.",
        explanation="Use the derivative for the slope, then use point-slope form.",
        steps=(
            SolutionStep("Find the point", f"f({point}) = {sp.sstr(y_value)}."),
            SolutionStep(
                "Differentiate",
                f"f'({variable}) = {sp.sstr(derivative_expr)}.",
            ),
            SolutionStep(
                "Evaluate the slope",
                f"f'({point}) = {sp.sstr(slope)}.",
            ),
            SolutionStep(
                "Use point-slope form",
                f"y - {sp.sstr(y_value)} = {sp.sstr(slope)}({variable} - {point}).",
            ),
            SolutionStep("Simplify", f"The tangent line is {sp.sstr(line)}."),
        ),
        check="Substitute the point into the line and compare slopes.",
    )


def derivative_rule_trace(
    expression: str | sp.Expr,
    *,
    variable: str = "x",
) -> tuple[str, ...]:
    """Return a simple rule-selection trace for a derivative expression."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    return tuple(_trace_expression(expr, symbol))


def optimization_candidate_table(
    expression: str | sp.Expr,
    domain: tuple[float, float] | None = None,
    *,
    variable: str = "x",
) -> tuple[OptimizationCandidate, ...]:
    """Return critical points and optional endpoints with function values."""

    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    derivative_expr = sp.diff(expr, symbol)
    raw_critical = sp.solve(sp.Eq(derivative_expr, 0), symbol)
    candidates: list[OptimizationCandidate] = []
    for critical in raw_critical:
        critical_expr = cast(sp.Expr, sp.sympify(critical))
        if domain is not None and not _inside_domain(critical_expr, domain):
            continue
        candidates.append(
            OptimizationCandidate(
                location=critical_expr,
                value=sp.simplify(expr.subs(symbol, critical_expr)),
                source="critical point",
            )
        )
    if domain is not None:
        for endpoint in domain:
            endpoint_expr = sp.sympify(endpoint)
            candidates.append(
                OptimizationCandidate(
                    location=endpoint_expr,
                    value=sp.simplify(expr.subs(symbol, endpoint_expr)),
                    source="endpoint",
                )
            )
    return tuple(candidates)


def riemann_sum_table(
    expression: str | sp.Expr,
    lower: float,
    upper: float,
    rectangles: int,
    *,
    method: RiemannMethod = "midpoint",
    variable: str = "x",
) -> tuple[RiemannSumRow, ...]:
    """Return subinterval, sample-point, height, and area rows for a Riemann sum."""

    if rectangles <= 0:
        msg = "rectangles must be positive"
        raise ValueError(msg)
    offsets: dict[RiemannMethod, float] = {"left": 0.0, "midpoint": 0.5, "right": 1.0}
    offset = offsets[method]
    symbol = sp.Symbol(variable)
    expr = parse_expression(expression, variables=(symbol,))
    function = sp.lambdify(symbol, expr, "math")
    width = (upper - lower) / rectangles
    rows: list[RiemannSumRow] = []
    for index in range(rectangles):
        left = lower + index * width
        right = left + width
        sample = lower + (index + offset) * width
        height = float(function(sample))
        rows.append(
            RiemannSumRow(
                index=index + 1,
                left=float(left),
                right=float(right),
                sample=float(sample),
                height=height,
                width=float(width),
                area=float(height * width),
            )
        )
    return tuple(rows)


def parse_point_list(received: object) -> tuple[sp.Expr, ...]:
    """Parse a critical-point answer from a sequence or simple string."""

    if isinstance(received, str):
        stripped = received.strip()
        try:
            parsed = ast.literal_eval(stripped)
        except (SyntaxError, ValueError):
            parsed = [part.strip() for part in stripped.replace(";", ",").split(",")]
        return parse_point_list(parsed)
    if isinstance(received, Sequence) and not isinstance(received, bytes | bytearray):
        return tuple(sp.sympify(value) for value in received)
    return (sp.sympify(received),)


def _trace_expression(expr: sp.Expr, symbol: sp.Symbol) -> list[str]:
    if not expr.has(symbol):
        return ["constant rule: the expression does not depend on the variable"]
    if isinstance(expr, sp.Add):
        return [
            "sum/difference rule: differentiate each term",
            *(
                detail
                for arg in expr.args
                for detail in _trace_expression(cast(sp.Expr, arg), symbol)
            ),
        ]
    if isinstance(expr, sp.Mul):
        constant, variable_part = expr.as_independent(symbol)
        if constant != 1:
            return [
                f"constant multiple rule: keep the factor {sp.sstr(constant)}",
                *_trace_expression(cast(sp.Expr, variable_part), symbol),
            ]
        return ["product rule: the expression is a product of changing factors"]
    if isinstance(expr, sp.Pow):
        base, exponent = expr.as_base_exp()
        if base == symbol:
            return [f"power rule: bring down {sp.sstr(exponent)} and subtract 1"]
        return [
            (
                "chain rule: differentiate the outside power and multiply "
                "by the inside derivative"
            ),
            *_trace_expression(cast(sp.Expr, base), symbol),
        ]
    if expr.is_Function:
        return [
            (
                "chain rule: differentiate the outside function and multiply "
                "by the inside derivative"
            )
        ]
    return ["basic derivative rule or known derivative"]


def _inside_domain(value: sp.Expr, domain: tuple[float, float]) -> bool:
    numeric = float(value)
    return domain[0] <= numeric <= domain[1]


__all__ = [
    "OptimizationCandidate",
    "RiemannMethod",
    "RiemannSumRow",
    "derivative_rule_trace",
    "limit_factor_cancel_steps",
    "optimization_candidate_table",
    "parse_point_list",
    "riemann_sum_table",
    "tangent_line_steps",
]
