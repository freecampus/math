"""SymPy-backed equation solving with optional AI tutor explanations."""

from __future__ import annotations

from dataclasses import replace
from typing import TypeAlias, cast

import sympy as sp

from edumath.core import infer_variable
from edumath.settings import get_settings
from edumath.solvers.explanations import (
    EquationExplanationClient,
    OpenAIEquationExplanationClient,
)
from edumath.solvers.models import (
    EquationSolution,
    EquationSolutionCheck,
    EquationStep,
)

EquationInput: TypeAlias = sp.Equality | sp.Expr


def solve_equation_steps(
    equation: EquationInput,
    *,
    variable: str | sp.Symbol | None = None,
    domain: sp.Set = sp.S.Reals,
    explain: bool = False,
    explanation_client: EquationExplanationClient | None = None,
    raise_on_explanation_error: bool = False,
) -> EquationSolution:
    """Solve a SymPy equation or expression and return structured steps.

    The solver layer intentionally does not parse raw strings. Use
    :func:`edumath.core.parse_equation` or :func:`edumath.core.parse_expression`
    before calling this function when the starting point is user text.

    SymPy/edumath produce the answer and algebraic transformations locally. If
    ``explain=True`` and an OpenAI key has been configured through
    :func:`edumath.settings.configure`, an optional AI tutor explanation is
    added after the solution has been computed. Without configured settings the
    function simply returns the symbolic solution with no AI prose.
    """

    parsed = _coerce_equation(equation)
    symbol = infer_variable(parsed, variable)
    solution = _solve_with_sympy_steps(parsed, symbol, domain)
    if not explain:
        return solution

    client = explanation_client
    if client is None:
        settings = get_settings()
        if settings.openai_api_key is None:
            return solution
        client = OpenAIEquationExplanationClient()

    try:
        explanation = client.explain_equation_solution(solution)
    except Exception as error:
        if raise_on_explanation_error:
            raise
        return replace(solution, explanation_error=str(error))
    return replace(solution, explanation=explanation)


def solve_equation(
    equation: EquationInput,
    *,
    variable: str | sp.Symbol | None = None,
    domain: sp.Set = sp.S.Reals,
    explain: bool = False,
    explanation_client: EquationExplanationClient | None = None,
    raise_on_explanation_error: bool = False,
) -> EquationSolution:
    """Alias for :func:`solve_equation_steps`."""

    return solve_equation_steps(
        equation,
        variable=variable,
        domain=domain,
        explain=explain,
        explanation_client=explanation_client,
        raise_on_explanation_error=raise_on_explanation_error,
    )


def _solve_with_sympy_steps(
    equation: sp.Equality,
    symbol: sp.Symbol,
    domain: sp.Set,
) -> EquationSolution:
    expression = sp.cancel(sp.expand(equation.lhs - equation.rhs))
    solution_set = cast(sp.Set, sp.solveset(expression, symbol, domain=domain))
    checks = _solution_checks(equation, symbol, solution_set)
    polynomial = _polynomial_for_steps(expression, symbol)

    if polynomial is None:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_generic_steps(equation, solution_set, symbol),
            checks=checks,
            method="SymPy solveset",
        )

    degree = polynomial.degree()
    if degree <= 0:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_constant_steps(equation, polynomial.as_expr(), solution_set),
            checks=checks,
            method="constant equation",
        )
    if degree == 1:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_linear_steps(equation, polynomial, symbol),
            checks=checks,
            method="linear equation",
        )
    if degree == 2:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_quadratic_steps(equation, polynomial, symbol),
            checks=checks,
            method="quadratic equation",
        )

    return EquationSolution(
        original=equation,
        variable=symbol,
        solution_set=solution_set,
        steps=_generic_steps(equation, solution_set, symbol),
        checks=checks,
        method="SymPy solveset",
    )


def _linear_steps(
    equation: sp.Equality,
    polynomial: sp.Poly,
    symbol: sp.Symbol,
) -> tuple[EquationStep, ...]:
    expr = sp.collect(polynomial.as_expr(), symbol)
    coefficient = polynomial.coeff_monomial(symbol)
    constant = polynomial.coeff_monomial(1)
    solution = sp.simplify(-constant / coefficient)
    steps: list[EquationStep] = [_original_step(equation)]
    _append_expansion_step(steps, equation)
    steps.append(
        EquationStep(
            "Move everything to one side",
            sp.Eq(expr, 0, evaluate=False),
            "This writes the equation in the form ax + b = 0.",
        )
    )
    if constant != 0:
        steps.append(
            EquationStep(
                "Move the constant term",
                sp.Eq(coefficient * symbol, -constant, evaluate=False),
            )
        )
    if coefficient != 1:
        steps.append(
            EquationStep(
                "Divide by the coefficient of the variable",
                sp.Eq(symbol, solution, evaluate=False),
            )
        )
    return tuple(steps)


def _quadratic_steps(
    equation: sp.Equality,
    polynomial: sp.Poly,
    symbol: sp.Symbol,
) -> tuple[EquationStep, ...]:
    expr = sp.collect(polynomial.as_expr(), symbol)
    steps: list[EquationStep] = [_original_step(equation)]
    _append_expansion_step(steps, equation)
    steps.append(
        EquationStep(
            "Write in standard form",
            sp.Eq(expr, 0, evaluate=False),
            "A quadratic equation is easiest to solve from ax^2 + bx + c = 0.",
        )
    )

    factored = sp.factor(expr)
    if factored != expr:
        roots = sorted(sp.solve(sp.Eq(expr, 0), symbol), key=sp.default_sort_key)
        root_text = ", ".join(f"{symbol} = {sp.sstr(root)}" for root in roots)
        steps.append(EquationStep("Factor", sp.Eq(factored, 0, evaluate=False)))
        steps.append(
            EquationStep(
                "Use the zero-product property",
                root_text,
                "If a product is zero, at least one factor must be zero.",
            )
        )
        return tuple(steps)

    a = polynomial.coeff_monomial(symbol**2)
    b = polynomial.coeff_monomial(symbol)
    c = polynomial.coeff_monomial(1)
    discriminant = sp.simplify(b**2 - 4 * a * c)
    roots = sorted(sp.solve(sp.Eq(expr, 0), symbol), key=sp.default_sort_key)
    root_text = ", ".join(f"{symbol} = {sp.sstr(root)}" for root in roots)
    steps.extend(
        (
            EquationStep(
                "Identify coefficients",
                f"a = {sp.sstr(a)}, b = {sp.sstr(b)}, c = {sp.sstr(c)}",
            ),
            EquationStep(
                "Compute the discriminant",
                f"b^2 - 4ac = {sp.sstr(discriminant)}",
            ),
            EquationStep(
                "Apply the quadratic formula",
                root_text,
                "Use x = (-b ± sqrt(b^2 - 4ac)) / (2a).",
            ),
        )
    )
    return tuple(steps)


def _constant_steps(
    equation: sp.Equality,
    expression: sp.Expr,
    solution_set: sp.Set,
) -> tuple[EquationStep, ...]:
    if solution_set == sp.S.Reals:
        note = "The equation is always true."
    else:
        note = "The equation is never true."
    return (
        _original_step(equation),
        EquationStep("Simplify", sp.Eq(expression, 0, evaluate=False), note),
    )


def _generic_steps(
    equation: sp.Equality,
    solution_set: sp.Set,
    symbol: sp.Symbol,
) -> tuple[EquationStep, ...]:
    return (
        _original_step(equation),
        EquationStep(
            "Solve symbolically",
            f"{symbol} ∈ {sp.sstr(solution_set)}",
            "SymPy found the solution set directly.",
        ),
    )


def _solution_checks(
    equation: sp.Equality,
    symbol: sp.Symbol,
    solution_set: sp.Set,
) -> tuple[EquationSolutionCheck, ...]:
    if not isinstance(solution_set, sp.FiniteSet):
        return ()
    checks: list[EquationSolutionCheck] = []
    expression = equation.lhs - equation.rhs
    for value in sorted(solution_set, key=sp.default_sort_key):
        result = sp.checksol(expression, symbol, value)
        checks.append(
            EquationSolutionCheck(
                value=sp.sympify(value),
                valid=result if result is None else bool(result),
            )
        )
    return tuple(checks)


def _polynomial_for_steps(expression: sp.Expr, symbol: sp.Symbol) -> sp.Poly | None:
    numerator, denominator = sp.fraction(sp.cancel(expression))
    if denominator.has(symbol):
        return None
    numerator = sp.expand(numerator)
    if not numerator.is_polynomial(symbol):
        return None
    try:
        return sp.Poly(numerator, symbol)
    except sp.PolynomialError:
        return None


def _coerce_equation(equation: EquationInput) -> sp.Equality:
    if isinstance(equation, str):
        msg = (
            "solve_equation_steps() expects a SymPy equation or expression, "
            "not a string. Use edumath.core.parse_equation() first."
        )
        raise TypeError(msg)
    if isinstance(equation, sp.Equality):
        return equation
    if isinstance(equation, sp.Expr):
        return sp.Eq(equation, 0, evaluate=False)

    msg = "equation must be a SymPy Equality or Expr"
    raise TypeError(msg)


def _original_step(equation: sp.Equality) -> EquationStep:
    return EquationStep("Original equation", equation)


def _append_expansion_step(
    steps: list[EquationStep],
    equation: sp.Equality,
) -> None:
    expanded = sp.Eq(sp.expand(equation.lhs), sp.expand(equation.rhs), evaluate=False)
    if sp.sstr(expanded) != sp.sstr(equation):
        steps.append(EquationStep("Expand both sides", expanded))


__all__ = ["solve_equation", "solve_equation_steps"]
