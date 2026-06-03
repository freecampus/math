import math

import sympy as sp

from edumath.calculus.derivatives import derivative, finite_difference, tangent_line
from edumath.calculus.integrals import antiderivative, definite_integral
from edumath.differential_equations.solvers import euler_method
from edumath.discrete_math.logic import implies, truth_table
from edumath.linear_algebra.concepts import (
    dot_product,
    matrix_vector_product,
    solve_linear_system,
    vector_norm,
)
from edumath.probability.distributions import (
    binomial_pmf,
    combinations,
    expected_value,
    factorial,
)
from edumath.statistics.concepts import describe, z_score
from edumath.trigonometry.concepts import (
    coterminal_angle,
    degrees_to_radians,
    radians_to_degrees,
)


def test_calculus_helpers() -> None:
    x = sp.Symbol("x")

    assert derivative("x**2") == 2 * x
    assert sp.simplify(tangent_line("x**2", 2) - (4 * x - 4)) == 0
    assert math.isclose(finite_difference("x**2", 2), 4, rel_tol=1e-5)
    assert antiderivative("2*x") == x**2
    assert definite_integral("2*x", 0, 3) == 9


def test_linear_algebra_helpers() -> None:
    assert dot_product([1, 2], [3, 4]) == 11
    assert vector_norm([3, 4]) == 5
    assert matrix_vector_product([[2, 0], [0, 3]], [5, 4]).tolist() == [10, 12]
    assert solve_linear_system([[1, 1], [1, -1]], [5, 1]).tolist() == [3, 2]


def test_probability_helpers() -> None:
    assert factorial(5) == 120
    assert combinations(5, 2) == 10
    assert math.isclose(binomial_pmf(2, 1, 0.5), 0.5)
    assert expected_value([0, 1], [0.25, 0.75]) == 0.75


def test_statistics_helpers() -> None:
    stats = describe([1, 2, 3], sample=False)

    assert stats.mean == 2
    assert stats.minimum == 1
    assert stats.maximum == 3
    assert z_score(3, 2, 1) == 1


def test_differential_equations_helpers() -> None:
    points = euler_method(
        lambda _x, y: y,
        initial_x=0,
        initial_y=1,
        step=0.1,
        steps=2,
    )

    assert points == [(0, 1), (0.1, 1.1), (0.2, 1.2100000000000002)]


def test_discrete_math_helpers() -> None:
    assert implies(True, False) is False
    assert len(truth_table(("p", "q"), implies)) == 4


def test_trigonometry_helpers() -> None:
    assert math.isclose(degrees_to_radians(180), math.pi)
    assert math.isclose(radians_to_degrees(math.pi), 180)
    assert coterminal_angle(-30) == 330
