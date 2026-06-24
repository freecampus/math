import numpy as np
import pytest
import sympy as sp

from edumath.core import (
    MathExpression,
    expression_equivalent,
    infer_variable,
    parse_equation,
    parse_expression,
)


def test_parse_expression_supports_common_math_names() -> None:
    expression = parse_expression("sin(pi / 2) + cos(0)")

    assert expression == 2


def test_parse_expression_supports_implicit_multiplication_and_caret_power() -> None:
    expression = parse_expression("2x^2 + 3x")
    x = sp.Symbol("x")

    assert expression == 2 * x**2 + 3 * x


def test_parse_equation_converts_text_to_sympy_equality() -> None:
    equation = parse_equation("2y + 3 = 7")

    assert isinstance(equation, sp.Equality)
    assert str(equation.lhs) == "2*y + 3"
    assert str(equation.rhs) == "7"


def test_parse_equation_interprets_expression_as_equal_to_zero() -> None:
    equation = parse_equation("z^2 - 4")

    z = sp.Symbol("z")

    assert sp.simplify(equation.lhs - (z**2 - 4)) == 0
    assert equation.rhs == 0


def test_infer_variable_returns_single_free_symbol() -> None:
    equation = parse_equation("2a + 1 = 9")

    assert infer_variable(equation) == sp.Symbol("a")


def test_infer_variable_requires_explicit_choice_for_multiple_symbols() -> None:
    x, y = sp.symbols("x y")

    with pytest.raises(ValueError, match="Pass variable"):
        infer_variable(sp.Eq(x + y, 5, evaluate=False))


def test_math_expression_samples_scalar_and_array_values() -> None:
    expression = MathExpression.parse("x**2 + 1")
    values = np.array([-1.0, 0.0, 1.0])

    sampled = expression.sample(values)

    assert sampled.tolist() == [2.0, 1.0, 2.0]


def test_expression_equivalent_checks_symbolic_equivalence() -> None:
    assert expression_equivalent("(x + 1)**2", "x**2 + 2*x + 1")
