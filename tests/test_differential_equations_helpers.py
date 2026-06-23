import math

import matplotlib.pyplot as plt
import sympy as sp

from edumath.differential_equations import (
    DIFFERENTIAL_EQUATIONS_PATH,
    classify_equilibrium_1d,
    classify_ode_exercise,
    differential_equations_diagnostic_quiz,
    direction_field_values,
    equilibrium_exercise,
    equilibrium_points_1d,
    euler_method,
    euler_method_scene,
    euler_step_exercise,
    improved_euler_method,
    linear_integrating_factor_exercise,
    linear_system_phase_plane_scene,
    phase_line_scene,
    separable_solution_exercise,
    slope_field_scene,
    solution_family_scene,
    system_equilibrium_exercise,
    system_euler_method,
    validate_equilibrium,
    validate_initial_condition,
    validate_numeric_trajectory,
    validate_solution_satisfies_ode,
)


def test_differential_equations_path_has_expected_lessons() -> None:
    assert DIFFERENTIAL_EQUATIONS_PATH.slugs() == [
        "first-order-equations",
        "separable-equations",
        "linear-equations",
        "slope-fields",
        "systems",
    ]


def test_euler_and_improved_euler_methods() -> None:
    points = euler_method(lambda _x, y: y, initial_x=0, initial_y=1, step=0.1, steps=2)
    assert points == [(0, 1), (0.1, 1.1), (0.2, 1.2100000000000002)]

    improved = improved_euler_method(
        lambda _x, y: y,
        initial_x=0,
        initial_y=1,
        step=0.1,
        steps=1,
    )
    assert math.isclose(improved[-1][1], 1.105)


def test_system_euler_method() -> None:
    points = system_euler_method(
        lambda _t, state: (-state[0], state[1]),
        initial_t=0,
        initial_state=(2, 1),
        step=0.5,
        steps=1,
    )
    assert points[-1] == (0.5, (1.0, 1.5))


def test_direction_field_and_equilibrium_helpers() -> None:
    samples = direction_field_values(lambda _x, y: y, [0], [1])
    assert len(samples) == 1
    assert samples[0][0:2] == (0.0, 1.0)

    y = sp.Symbol("y")
    assert equilibrium_points_1d("y*(3-y)") == (0, 3)
    assert equilibrium_points_1d(y * (3 - y)) == (0, 3)
    assert classify_equilibrium_1d("y*(1-y)", 1) == "stable"
    assert classify_equilibrium_1d("y*(1-y)", 0) == "unstable"


def test_validators_accept_correct_answers() -> None:
    assert validate_solution_satisfies_ode("exp(2*x)", "2*y").correct
    assert validate_initial_condition("3*exp(x)", x0=0, y0=3).correct
    assert validate_numeric_trajectory([(0, 1), (1, 2)], [(0, 1), (1, 2)]).correct
    assert validate_equilibrium(3, "y*(3-y)").correct


def test_exercise_builders_accept_expected_answers() -> None:
    exercises = (
        classify_ode_exercise(seed=1),
        separable_solution_exercise(seed=1),
        linear_integrating_factor_exercise(seed=1),
        euler_step_exercise(seed=1),
        equilibrium_exercise(seed=1),
        system_equilibrium_exercise(seed=1),
    )
    for exercise in exercises:
        assert exercise.check(exercise.expected).correct


def test_quiz_builders() -> None:
    quiz = differential_equations_diagnostic_quiz()
    assert quiz.total == 4
    assert quiz.questions[0].check("separable").correct


def test_plot_scenes_render() -> None:
    scenes = (
        slope_field_scene(lambda x, y: x - y, density=5),
        euler_method_scene(
            lambda _x, y: y, initial_x=0, initial_y=1, step=0.2, steps=2
        ),
        solution_family_scene(("exp(x)", "2*exp(x)"), y_min=-1, y_max=6),
        phase_line_scene(lambda _x, y: y * (1 - y), equilibria=(0, 1)),
        linear_system_phase_plane_scene(((0, 1), (-1, 0)), density=5),
    )
    for scene in scenes:
        figure, axis = scene.render()
        assert axis.get_title()
        plt.close(figure)
