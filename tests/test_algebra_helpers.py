import matplotlib.pyplot as plt

from edumath.algebra import (
    COLLEGE_ALGEBRA_PATH,
    QuadraticModel,
    expand_expression_exercise,
    expand_question,
    expression_table,
    function_scene,
    input_output_scene,
    line_from_points,
    linear_equation_exercise,
    polynomial_from_roots,
    polynomial_root_scene,
    polynomial_summary,
    quadratic_from_vertex,
    transformation_scene,
    transformed_expression,
    validate_expression_equivalence,
)


def test_college_algebra_path_has_lessons() -> None:
    assert COLLEGE_ALGEBRA_PATH.slugs() == [
        "expressions-and-equations",
        "inequalities-and-absolute-value",
        "functions-and-graphs",
        "transformations-composition-inverses",
        "linear-and-quadratic-functions",
        "polynomials",
        "rational-and-radical-functions",
        "exponentials-and-logarithms",
        "systems-of-equations",
        "algebraic-modeling",
        "symbolic-computation-with-sympy",
        "cumulative-review",
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


def test_expression_table_evaluates_selected_inputs() -> None:
    table = expression_table("x**2 + 1", (-2, 0, 3))

    assert table == ((-2.0, 5.0), (0.0, 1.0), (3.0, 10.0))


def test_input_output_scene_highlights_selected_point() -> None:
    scene = input_output_scene("x**2", x_value=2, x_min=-3, x_max=3, y_min=-1, y_max=5)

    figure, axis = scene.render()

    assert "Input-output" in axis.get_title()

    plt.close(figure)


def test_transformation_scene_uses_transformed_expression() -> None:
    transformed = transformed_expression(
        "x**2",
        vertical_scale=2,
        horizontal_shift=3,
        vertical_shift=1,
    )

    assert str(transformed) == "2*x**2 - 12*x + 19"

    scene = transformation_scene("x**2", horizontal_shift=1)
    figure, axis = scene.render()

    assert axis.get_title() == "Function transformation"

    plt.close(figure)


def test_expand_question_checks_symbolic_equivalence() -> None:
    question = expand_question("(x + 1)**2")

    assert question.check("x**2 + 2*x + 1").correct


def test_line_from_points_creates_slope_intercept_model() -> None:
    model = line_from_points((0, 1), (2, 5))

    assert str(model.expression) == "2*x + 1"
    assert model.evaluate(3) == 7


def test_quadratic_model_reports_vertex_and_discriminant() -> None:
    model = QuadraticModel(1, -4, 3)

    assert model.discriminant == 4
    assert model.vertex == (2, -1)
    assert model.roots == (1, 3)


def test_quadratic_from_vertex_returns_expanded_expression() -> None:
    expression = quadratic_from_vertex(a=2, h=3, k=1)

    assert str(expression) == "2*x**2 - 12*x + 19"


def test_polynomial_summary_reports_roots_and_multiplicity() -> None:
    summary = polynomial_summary("(x - 2)**2*(x + 1)")

    assert summary.degree == 3
    assert summary.leading_coefficient == 1
    assert str(summary.factored) == "(x - 2)**2*(x + 1)"
    assert summary.root_multiplicities == ((-1, 1), (2, 2))


def test_polynomial_from_roots_builds_expanded_polynomial() -> None:
    expression = polynomial_from_roots((-1, 2, 2))

    assert str(expression) == "x**3 - 3*x**2 + 4"


def test_polynomial_root_scene_renders_roots() -> None:
    scene = polynomial_root_scene("(x - 2)*(x + 1)", x_min=-3, x_max=3)

    figure, axis = scene.render()

    assert "Polynomial roots" in axis.get_title()

    plt.close(figure)
