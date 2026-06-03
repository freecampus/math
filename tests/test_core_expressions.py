import numpy as np

from edumath.core import MathExpression, expression_equivalent, parse_expression


def test_parse_expression_supports_common_math_names() -> None:
    expression = parse_expression("sin(pi / 2) + cos(0)")

    assert expression == 2


def test_math_expression_samples_scalar_and_array_values() -> None:
    expression = MathExpression.parse("x**2 + 1")
    values = np.array([-1.0, 0.0, 1.0])

    sampled = expression.sample(values)

    assert sampled.tolist() == [2.0, 1.0, 2.0]


def test_expression_equivalent_checks_symbolic_equivalence() -> None:
    assert expression_equivalent("(x + 1)**2", "x**2 + 2*x + 1")
