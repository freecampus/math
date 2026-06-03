import matplotlib.pyplot as plt
import sympy as sp

from edumath.algebra import GuessingQuiz, SympyGuessGame
from edumath.algebra.quizes import expression_points, generate_options, plot_expression


def test_guessing_quiz_generates_distinct_options_with_answer() -> None:
    quiz = GuessingQuiz(seed=123)

    question = quiz.question()

    assert len(question.options) == 4
    assert question.expression in question.options
    assert len({sp.srepr(option) for option in question.options}) == 4
    assert question.is_correct(question.expression)


def test_generate_options_includes_correct_expression() -> None:
    expression = sp.sympify("x**2 + 1")

    options = generate_options(expression, count=4, seed=1)

    assert expression in options
    assert len(options) == 4


def test_expression_points_evaluates_scalar_expression() -> None:
    x_values, y_values = expression_points(sp.Integer(3), sample_count=5)

    assert x_values.shape == (5,)
    assert y_values.tolist() == [3, 3, 3, 3, 3]


def test_plot_expression_returns_matplotlib_objects() -> None:
    figure, axis = plot_expression(sp.sympify("x**2"), sample_count=20)

    assert figure is axis.figure
    assert axis.get_title() == "Which equation matches this graph?"

    plt.close(figure)


def test_legacy_widget_name_remains_available() -> None:
    widget = SympyGuessGame(total_questions=3, seed=1)

    assert widget.total_questions == 3
