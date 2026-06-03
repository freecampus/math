import matplotlib.pyplot as plt

from edumath.algebra import (
    COLLEGE_ALGEBRA_PATH,
    expand_expression_exercise,
    function_scene,
    linear_equation_exercise,
    validate_expression_equivalence,
)


def test_college_algebra_path_has_lessons() -> None:
    assert COLLEGE_ALGEBRA_PATH.slugs() == [
        "expressions-and-equations",
        "functions-and-graphs",
        "polynomials",
        "exponentials-and-logarithms",
        "systems-of-equations",
    ]


def test_linear_equation_exercise_has_valid_expected_answer() -> None:
    exercise = linear_equation_exercise(seed=1)

    assert exercise.check(exercise.expected).correct


def test_expand_expression_exercise_checks_equivalent_answer() -> None:
    exercise = expand_expression_exercise(seed=1)

    assert exercise.check(exercise.expected).correct


def test_validate_expression_equivalence_accepts_expanded_form() -> None:
    result = validate_expression_equivalence("(x + 1)**2", "x**2 + 2*x + 1")

    assert result.correct


def test_function_scene_renders() -> None:
    scene = function_scene("x**2", x_min=-2, x_max=2, y_min=-1, y_max=5)

    figure, axis = scene.render()

    assert axis.get_title() == "y = x**2"

    plt.close(figure)
