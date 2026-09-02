import pytest
import sympy as sp

from fcmath.core import NumericTolerance
from fcmath.validation import ValidationPolicy, check_answer, parse_solution_set


def test_symbolic_policy_checks_equivalence_not_strings() -> None:
    policy = ValidationPolicy(mode="symbolic-equivalence", variables=("x",))

    assert check_answer("(x + 1)^2", "x^2 + 2*x + 1", policy).correct
    assert not check_answer("x^2 + 1", "x^2 + 2*x + 1", policy).correct


def test_symbolic_policy_rejects_undeclared_variables() -> None:
    policy = ValidationPolicy(mode="symbolic-equivalence", variables=("x",))

    result = check_answer("x + y", "x + 1", policy)

    assert not result.correct
    assert "undeclared variable" in result.message


def test_numeric_policy_uses_explicit_absolute_and_relative_tolerances() -> None:
    policy = ValidationPolicy(
        mode="numeric",
        tolerance=NumericTolerance(absolute=1e-3, relative=0),
    )

    assert check_answer("1/3", 0.3334, policy).correct
    assert not check_answer("1/3", 0.34, policy).correct


def test_solution_sets_and_intervals_are_compared_as_sets() -> None:
    policy = ValidationPolicy(mode="solution-set", domain="real")

    assert check_answer("{2, 1}", "{1, 2}", policy).correct
    assert check_answer(
        "(-oo, 2] U (3, oo)",
        sp.Union(sp.Interval(-sp.oo, 2), sp.Interval.open(3, sp.oo)),
        policy,
    ).correct
    assert parse_solution_set("[0, 1)") == sp.Interval.Ropen(0, 1)


def test_matrix_policy_checks_shape_and_symbolic_entries() -> None:
    policy = ValidationPolicy(mode="matrix", matrix_shape=(2, 2))

    assert check_answer("[[1, 2], [3, 4]]", [[1, 2], [3, 4]], policy).correct
    result = check_answer("[[1, 2, 3]]", [[1, 2], [3, 4]], policy)
    assert not result.correct
    assert "2 by 2" in result.message


def test_units_can_be_required_without_evaluating_input() -> None:
    policy = ValidationPolicy(
        mode="numeric",
        units="m/s",
        units_required=True,
        tolerance=NumericTolerance(absolute=0, relative=0),
    )

    assert check_answer("3 m/s", 3, policy).correct
    assert not check_answer("3 km/h", 3, policy).correct
    assert not check_answer("3", 3, policy).correct


def test_validation_policies_reject_invalid_runtime_configuration() -> None:
    with pytest.raises(ValueError, match="validation mode"):
        ValidationPolicy(mode="arbitrary-python")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="nonnegative"):
        ValidationPolicy(
            mode="numeric",
            tolerance=NumericTolerance(absolute=-1, relative=0),
        )

    with pytest.raises(ValueError, match="declared unit"):
        ValidationPolicy(mode="numeric", units_required=True)
