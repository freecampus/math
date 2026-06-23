import math

import matplotlib.pyplot as plt
import sympy as sp

from edumath.calculus import (
    CALCULUS_PATH,
    antiderivative_question,
    average_rate_of_change,
    calculus_diagnostic_quiz,
    calculus_tool_question,
    critical_point_exercise,
    derivative_question,
    derivative_rule_exercise,
    derivative_sign_scene,
    left_riemann_sum,
    optimization_scene,
    riemann_sum_exercise,
    riemann_sum_scene,
    right_riemann_sum,
    secant_tangent_scene,
    tangent_line_exercise,
    tool_choice_exercise,
    trapezoid_rule,
    validate_antiderivative_equivalence,
    validate_derivative_equivalence,
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


def test_exercise_builders_accept_expected_answers() -> None:
    for exercise in (
        tangent_line_exercise(seed=1),
        derivative_rule_exercise(seed=1),
        critical_point_exercise(seed=1),
        riemann_sum_exercise(seed=1),
        tool_choice_exercise(seed=1),
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
