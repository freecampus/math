"""SymPy-backed equation solving with optional AI tutor explanations."""

from __future__ import annotations

from dataclasses import replace
from typing import cast

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

from edumath.solvers.explanations import (
    DEFAULT_OPENAI_MODEL,
    EquationExplanationClient,
    OpenAIEquationExplanationClient,
)
from edumath.solvers.models import (
    EquationSolution,
    EquationSolutionCheck,
    EquationStep,
)

_TRANSFORMATIONS = (
    *standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
_PARSE_SYMBOLS = {
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


def parse_equation(
    source: str | sp.Basic,
    *,
    variable: str | sp.Symbol = "x",
) -> sp.Equality:
    """Parse an equation from text or a SymPy equality.

    Text may be written as ``"2(x - 3) + 4 = 10"``. If the text does not
    contain an equals sign, it is interpreted as ``expression = 0``.
    """

    symbol = _symbol(variable)
    if isinstance(source, sp.Equality):
        return source
    if isinstance(source, sp.Basic):
        return sp.Eq(source, 0, evaluate=False)

    text = source.strip()
    if not text:
        msg = "equation text must not be empty"
        raise ValueError(msg)

    if "=" in text:
        parts = text.split("=")
        if len(parts) != 2:
            msg = "equation text must contain exactly one equals sign"
            raise ValueError(msg)
        left_text, right_text = parts
        left = _parse_math_text(left_text, symbol)
        right = _parse_math_text(right_text, symbol)
    else:
        left = _parse_math_text(text, symbol)
        right = sp.Integer(0)
    return sp.Eq(left, right, evaluate=False)


def solve_equation_steps(
    equation: str | sp.Basic,
    *,
    variable: str | sp.Symbol = "x",
    domain: sp.Set = sp.S.Reals,
    api_key: str | None = None,
    explain: bool | None = None,
    explanation_client: EquationExplanationClient | None = None,
    model: str = DEFAULT_OPENAI_MODEL,
    raise_on_explanation_error: bool = False,
) -> EquationSolution:
    """Solve an equation and return structured steps.

    SymPy/edumath produce the answer and algebraic transformations locally. If
    ``api_key`` or ``explanation_client`` is supplied, an optional AI tutor
    explanation is added after the solution has been computed. Without an API
    key the function simply returns the symbolic solution with no AI prose.
    """

    symbol = _symbol(variable)
    parsed = parse_equation(equation, variable=symbol)
    original_display = _original_display(equation)
    solution = _solve_with_sympy_steps(parsed, symbol, domain, original_display)
    if explain is None:
        should_explain = api_key is not None or explanation_client is not None
    else:
        should_explain = explain
    if not should_explain:
        return solution

    client = explanation_client
    if client is None and api_key is not None:
        client = OpenAIEquationExplanationClient(api_key=api_key, model=model)
    if client is None:
        return solution

    try:
        explanation = client.explain_equation_solution(solution)
    except Exception as error:
        if raise_on_explanation_error:
            raise
        return replace(solution, explanation_error=str(error))
    return replace(solution, explanation=explanation)


def solve_equation(
    equation: str | sp.Basic,
    *,
    variable: str | sp.Symbol = "x",
    domain: sp.Set = sp.S.Reals,
    api_key: str | None = None,
    explain: bool | None = None,
    explanation_client: EquationExplanationClient | None = None,
    model: str = DEFAULT_OPENAI_MODEL,
    raise_on_explanation_error: bool = False,
) -> EquationSolution:
    """Alias for :func:`solve_equation_steps`."""

    return solve_equation_steps(
        equation,
        variable=variable,
        domain=domain,
        api_key=api_key,
        explain=explain,
        explanation_client=explanation_client,
        model=model,
        raise_on_explanation_error=raise_on_explanation_error,
    )


def _solve_with_sympy_steps(
    equation: sp.Equality,
    symbol: sp.Symbol,
    domain: sp.Set,
    original_display: str | None,
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
            steps=_generic_steps(equation, solution_set, symbol, original_display),
            checks=checks,
            method="SymPy solveset",
        )

    degree = polynomial.degree()
    if degree <= 0:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_constant_steps(
                equation,
                polynomial.as_expr(),
                solution_set,
                original_display,
            ),
            checks=checks,
            method="constant equation",
        )
    if degree == 1:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_linear_steps(equation, polynomial, symbol, original_display),
            checks=checks,
            method="linear equation",
        )
    if degree == 2:
        return EquationSolution(
            original=equation,
            variable=symbol,
            solution_set=solution_set,
            steps=_quadratic_steps(equation, polynomial, symbol, original_display),
            checks=checks,
            method="quadratic equation",
        )

    return EquationSolution(
        original=equation,
        variable=symbol,
        solution_set=solution_set,
        steps=_generic_steps(equation, solution_set, symbol, original_display),
        checks=checks,
        method="SymPy solveset",
    )


def _linear_steps(
    equation: sp.Equality,
    polynomial: sp.Poly,
    symbol: sp.Symbol,
    original_display: str | None,
) -> tuple[EquationStep, ...]:
    expr = sp.collect(polynomial.as_expr(), symbol)
    coefficient = polynomial.coeff_monomial(symbol)
    constant = polynomial.coeff_monomial(1)
    solution = sp.simplify(-constant / coefficient)
    steps: list[EquationStep] = [_original_step(equation, original_display)]
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
    original_display: str | None,
) -> tuple[EquationStep, ...]:
    expr = sp.collect(polynomial.as_expr(), symbol)
    steps: list[EquationStep] = [_original_step(equation, original_display)]
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
    original_display: str | None,
) -> tuple[EquationStep, ...]:
    if solution_set == sp.S.Reals:
        note = "The equation is always true."
    else:
        note = "The equation is never true."
    return (
        _original_step(equation, original_display),
        EquationStep("Simplify", sp.Eq(expression, 0, evaluate=False), note),
    )


def _generic_steps(
    equation: sp.Equality,
    solution_set: sp.Set,
    symbol: sp.Symbol,
    original_display: str | None,
) -> tuple[EquationStep, ...]:
    return (
        _original_step(equation, original_display),
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


def _parse_math_text(text: str, symbol: sp.Symbol) -> sp.Expr:
    local_dict = _PARSE_SYMBOLS.copy()
    local_dict[symbol.name] = symbol
    parsed = parse_expr(
        text.strip(),
        local_dict=local_dict,
        transformations=_TRANSFORMATIONS,
        evaluate=False,
    )
    return cast(sp.Expr, parsed)


def _symbol(variable: str | sp.Symbol) -> sp.Symbol:
    if isinstance(variable, sp.Symbol):
        return variable
    return sp.Symbol(variable)


def _original_display(equation: str | sp.Basic) -> str | None:
    if not isinstance(equation, str):
        return None
    text = equation.strip()
    if not text:
        return None
    if "=" not in text:
        return f"{text} = 0"
    left, right = text.split("=", maxsplit=1)
    return f"{left.strip()} = {right.strip()}"


def _original_step(
    equation: sp.Equality,
    original_display: str | None,
) -> EquationStep:
    return EquationStep("Original equation", original_display or equation)


def _append_expansion_step(
    steps: list[EquationStep],
    equation: sp.Equality,
) -> None:
    expanded = sp.Eq(sp.expand(equation.lhs), sp.expand(equation.rhs), evaluate=False)
    if sp.sstr(expanded) != sp.sstr(equation):
        steps.append(EquationStep("Expand both sides", expanded))


__all__ = ["parse_equation", "solve_equation", "solve_equation_steps"]
