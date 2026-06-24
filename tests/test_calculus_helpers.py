import math

import matplotlib.pyplot as plt
import sympy as sp

from edumath.calculus import (
    CALCULUS_PATH,
    antiderivative_question,
    average_rate_of_change,
    calculus_application_tool_choice_exercise,
    calculus_diagnostic_quiz,
    calculus_tool_question,
    critical_point_exercise,
    derivative_question,
    derivative_rule_exercise,
    derivative_rule_trace,
    derivative_sign_scene,
    left_riemann_sum,
    limit_factor_cancel_exercise,
    limit_factor_cancel_steps,
    optimization_candidate_table,
    optimization_scene,
    riemann_sum_exercise,
    riemann_sum_scene,
    riemann_sum_table,
    riemann_sum_table_exercise,
    right_riemann_sum,
    rule_selection_exercise,
    secant_tangent_scene,
    substitution_exercise,
    tangent_line_exercise,
    tangent_line_steps,
    tool_choice_exercise,
    trapezoid_rule,
    validate_antiderivative_equivalence,
    validate_critical_points,
    validate_derivative_equivalence,
    validate_limit_answer,
    validate_tangent_line,
)


def test_calculus_path_has_expected_lessons() -> None:
    assert CALCULUS_PATH.slugs() == [
        "limits",
        "derivatives",
        "derivative-rules",
        "optimization",
        "integrals",
        "integration-techniques",
        "applications",
    ]


def test_average_rate_of_change() -> None:
    assert average_rate_of_change("x**2", 1, 3) == 4


def test_riemann_and_trapezoid_helpers() -> None:
    assert math.isclose(left_riemann_sum("x", 0, 1, 10), 0.45)
    assert math.isclose(right_riemann_sum("x", 0, 1, 10), 0.55)
    assert math.isclose(trapezoid_rule("x", 0, 1, 10), 0.5)


def test_calculus_validators_accept_equivalent_answers() -> None:
    x = sp.Symbol("x")

    assert validate_derivative_equivalence("2*x", 2 * x).correct
    assert validate_antiderivative_equivalence("x**2 + 7", x**2).correct


def test_step_by_step_calculus_helpers() -> None:
    limit_solution = limit_factor_cancel_steps("(x**2 - 9)/(x - 3)", 3)
    assert limit_solution.answer == "6"
    assert len(limit_solution.steps) == 4

    tangent_solution = tangent_line_steps("x**2", 3)
    assert tangent_solution.answer == "6*x - 9"

    trace = derivative_rule_trace("(x**2 + 1)**3")
    assert any("chain rule" in step for step in trace)

    candidates = optimization_candidate_table("x**2 - 6*x + 10", domain=(0, 5))
    candidate_rows = [
        (candidate.location, candidate.value, candidate.source)
        for candidate in candidates
    ]
    assert candidate_rows == [
        (sp.Integer(3), sp.Integer(1), "critical point"),
        (sp.Integer(0), sp.Integer(10), "endpoint"),
        (sp.Integer(5), sp.Integer(5), "endpoint"),
    ]

    rows = riemann_sum_table("x**2", 0, 1, 2, method="midpoint")
    assert len(rows) == 2
    assert math.isclose(sum(row.area for row in rows), 0.3125)


def test_calculus_validators_for_problem_solving_answers() -> None:
    assert validate_limit_answer(6, "(x**2 - 9)/(x - 3)", 3).correct
    assert validate_tangent_line("6*x - 9", "x**2", 3).correct
    assert validate_critical_points("3", "x**2 - 6*x + 10").correct


def test_exercise_builders_accept_expected_answers() -> None:
    for exercise in (
        tangent_line_exercise(seed=1),
        limit_factor_cancel_exercise(seed=1),
        derivative_rule_exercise(seed=1),
        rule_selection_exercise(seed=1),
        critical_point_exercise(seed=1),
        riemann_sum_exercise(seed=1),
        riemann_sum_table_exercise(seed=1),
        substitution_exercise(seed=1),
        tool_choice_exercise(seed=1),
        calculus_application_tool_choice_exercise(seed=1),
    ):
        assert exercise.check(exercise.expected).correct


def test_quiz_builders_check_answers() -> None:
    assert derivative_question("x**2").check("2*x").correct
    assert antiderivative_question("2*x").check("x**2 + 5").correct
    assert calculus_tool_question().check("integral").correct

    quiz = calculus_diagnostic_quiz()
    assert quiz.total == 4


def test_calculus_plot_scenes_render() -> None:
    scenes = (
        secant_tangent_scene("x**2", point=1, y_min=-1, y_max=5),
        riemann_sum_scene("x**2", 0, 1, 4, y_min=-1, y_max=2),
        derivative_sign_scene("x**2", x_min=-2, x_max=2, y_min=-2, y_max=4),
        optimization_scene("(x - 1)**2", candidates=(1,), x_min=-2, x_max=3),
    )

    for scene in scenes:
        figure, axis = scene.render()
        assert axis.get_title()
        plt.close(figure)
