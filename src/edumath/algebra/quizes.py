"""Interactive algebra quizzes for notebook environments."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from random import Random
from typing import cast

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from IPython.display import clear_output as ipython_clear_output
from IPython.display import display as ipython_display
from matplotlib.axes import Axes
from matplotlib.figure import Figure

ExpressionBuilder = Callable[[sp.Symbol, Random], sp.Expr]


X = sp.symbols("x")


@dataclass(frozen=True)
class GuessQuestion:
    """A single graph-to-expression multiple-choice question."""

    expression: sp.Expr
    options: tuple[sp.Expr, ...]

    @property
    def answer_index(self) -> int:
        return self.options.index(self.expression)

    def is_correct(self, selected: sp.Expr) -> bool:
        return _same_expression(selected, self.expression)


@dataclass(frozen=True)
class GuessResult:
    """Result returned after a learner answers one question."""

    question: GuessQuestion
    selected: sp.Expr
    correct: bool


class GuessingQuiz:
    """Generate questions for guessing algebraic expressions from graphs."""

    def __init__(
        self,
        *,
        option_count: int = 4,
        seed: int | None = None,
        builders: tuple[ExpressionBuilder, ...] | None = None,
    ) -> None:
        if option_count < 2:
            msg = "option_count must be at least 2"
            raise ValueError(msg)

        self.option_count = option_count
        self.random = Random(seed)
        self.builders = builders or DEFAULT_BUILDERS

    def question(self) -> GuessQuestion:
        expression = self.expression()
        options = [expression]
        attempts = 0
        max_attempts = self.option_count * 50

        while len(options) < self.option_count and attempts < max_attempts:
            attempts += 1
            candidate = self.expression()
            if not any(_same_expression(candidate, option) for option in options):
                options.append(candidate)

        if len(options) != self.option_count:
            msg = "could not generate enough distinct answer options"
            raise RuntimeError(msg)

        self.random.shuffle(options)
        return GuessQuestion(expression=expression, options=tuple(options))

    def expression(self) -> sp.Expr:
        builder = self.random.choice(self.builders)
        return sp.expand(builder(X, self.random))


class GuessingQuizWidget:
    """Notebook widget for the algebra expression guessing quiz."""

    def __init__(
        self,
        *,
        total_questions: int = 5,
        option_count: int = 4,
        seed: int | None = None,
        x_min: float = -10,
        x_max: float = 10,
        sample_count: int = 400,
    ) -> None:
        self.quiz = GuessingQuiz(option_count=option_count, seed=seed)
        self.total_questions = total_questions
        self.x_min = x_min
        self.x_max = x_max
        self.sample_count = sample_count

        self.current_index = 0
        self.correct_count = 0
        self.results: list[GuessResult] = []
        self.current_question: GuessQuestion | None = None
        self.answer_buttons: list[widgets.Button] = []

        self.output = widgets.Output()
        self.num_input = widgets.IntSlider(
            value=total_questions,
            min=1,
            max=100,
            description="Questions:",
            continuous_update=False,
        )
        self.start_button = widgets.Button(
            description="Start",
            button_style="success",
        )
        self.start_button.on_click(self.start)

    @property
    def wrong_count(self) -> int:
        return len(self.results) - self.correct_count

    def display(self) -> widgets.Output:
        """Display the setup screen and return the widget output container."""

        self.show_setup()
        _display(self.output)
        return self.output

    def show_setup(self) -> None:
        with self.output:
            _clear_output()
            _display(
                widgets.VBox(
                    [
                        widgets.HTML("<h3>Algebra graph guessing quiz</h3>"),
                        widgets.HTML("Choose how many questions to answer."),
                        self.num_input,
                        self.start_button,
                    ]
                )
            )

    def start(self, _button: widgets.Button | None = None) -> None:
        self.total_questions = int(self.num_input.value)
        self.current_index = 0
        self.correct_count = 0
        self.results = []
        self.show_question()

    def show_question(self, _button: widgets.Button | None = None) -> None:
        self.current_question = self.quiz.question()
        self.answer_buttons = [
            self._answer_button(option) for option in self.current_question.options
        ]

        with self.output:
            _clear_output(wait=True)
            _display(self._status_html())
            figure, _axis = plot_expression(
                self.current_question.expression,
                title="Which expression matches this graph?",
                x_min=self.x_min,
                x_max=self.x_max,
                sample_count=self.sample_count,
            )
            _display(figure)
            plt.close(figure)
            _display(widgets.VBox(_button_rows(self.answer_buttons)))

    def answer(self, selected: sp.Expr) -> None:
        if self.current_question is None:
            return

        for button in self.answer_buttons:
            button.disabled = True

        correct = self.current_question.is_correct(selected)
        self.results.append(
            GuessResult(
                question=self.current_question,
                selected=selected,
                correct=correct,
            )
        )
        if correct:
            self.correct_count += 1

        self.current_index += 1
        with self.output:
            _display(self._feedback_html(selected, correct))
            if self.current_index < self.total_questions:
                next_button = widgets.Button(
                    description="Next",
                    button_style="info",
                )
                next_button.on_click(self.show_question)
                _display(next_button)
            else:
                _display(self._final_score_html())
                retry_button = widgets.Button(
                    description="Play again",
                    button_style="primary",
                )
                retry_button.on_click(self.show_setup)
                _display(retry_button)

    def _answer_button(self, option: sp.Expr) -> widgets.Button:
        button = widgets.Button(
            description=_expression_label(option),
            tooltip=sp.latex(option),
            layout=widgets.Layout(width="260px", min_height="44px"),
        )
        button.on_click(lambda _button, selected=option: self.answer(selected))
        return button

    def _status_html(self) -> widgets.HTML:
        return widgets.HTML(
            "<strong>"
            f"Question {self.current_index + 1} of {self.total_questions}"
            "</strong>"
            f" &nbsp; Score: {self.correct_count}/{len(self.results)}"
        )

    def _feedback_html(self, selected: sp.Expr, correct: bool) -> widgets.HTML:
        if correct:
            message = "Correct."
            color = "#137333"
        else:
            assert self.current_question is not None
            answer = _expression_label(self.current_question.expression)
            selected_label = _expression_label(selected)
            message = f"Not quite. You chose {selected_label}; the answer is {answer}."
            color = "#b3261e"

        return widgets.HTML(
            f'<p style="color: {color}; font-weight: 600;">{message}</p>'
        )

    def _final_score_html(self) -> widgets.HTML:
        return widgets.HTML(
            "<h3>Quiz complete</h3>"
            f"<p>Final score: {self.correct_count}/{self.total_questions}</p>"
        )


class SympyGuessGame(GuessingQuizWidget):
    """Backward-compatible name for the original notebook widget."""


def get_random_expression(seed: int | None = None) -> sp.Expr:
    """Return one random algebraic expression."""

    return GuessingQuiz(seed=seed).expression()


def generate_options(
    correct_expr: sp.Expr,
    count: int = 4,
    seed: int | None = None,
) -> list[sp.Expr]:
    """Return shuffled answer options containing ``correct_expr``."""

    quiz = GuessingQuiz(option_count=count, seed=seed)
    options = [correct_expr]
    while len(options) < count:
        candidate = quiz.expression()
        if not any(_same_expression(candidate, option) for option in options):
            options.append(candidate)
    quiz.random.shuffle(options)
    return options


def plot_expression(
    expr: sp.Expr,
    current: int | None = None,
    total: int | None = None,
    *,
    title: str | None = None,
    x_min: float = -10,
    x_max: float = 10,
    sample_count: int = 400,
    axis: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot an expression and return the Matplotlib figure and axis."""

    x_values, y_values = expression_points(
        expr,
        x_min=x_min,
        x_max=x_max,
        sample_count=sample_count,
    )

    if axis is None:
        figure, axis = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
    else:
        figure = cast(Figure, axis.figure)

    axis.plot(x_values, y_values, color="#1a73e8", linewidth=2.4)
    axis.axhline(0, color="#202124", linewidth=1)
    axis.axvline(0, color="#202124", linewidth=1)
    axis.grid(True, alpha=0.28)
    axis.set_xlabel("x")
    axis.set_ylabel("y")

    if title is None and current is not None and total is not None:
        title = f"Question {current} of {total}: Which equation matches this?"
    axis.set_title(title or "Which equation matches this graph?")

    finite_y = y_values[np.isfinite(y_values)]
    if finite_y.size:
        lower, upper = np.percentile(finite_y, [2, 98])
        padding = max((upper - lower) * 0.08, 1)
        axis.set_ylim(min(lower - padding, -5), max(upper + padding, 5))

    return figure, axis


def expression_points(
    expr: sp.Expr,
    *,
    x_min: float = -10,
    x_max: float = 10,
    sample_count: int = 400,
) -> tuple[np.ndarray, np.ndarray]:
    """Evaluate an expression on an evenly spaced domain."""

    x_values = np.linspace(x_min, x_max, sample_count)
    function = sp.lambdify(X, expr, "numpy")
    y_values = function(x_values)

    if np.isscalar(y_values):
        y_values = np.full_like(x_values, y_values, dtype=float)
    else:
        y_values = np.asarray(y_values, dtype=float)

    if y_values.shape != x_values.shape:
        y_values = np.broadcast_to(y_values, x_values.shape).astype(float)

    y_values = np.where(np.isfinite(y_values), y_values, np.nan)
    return x_values, y_values


def _linear_builder(x: sp.Symbol, rng: Random) -> sp.Expr:
    return _nonzero_int(rng, -4, 4) * x + rng.randint(-6, 6)


def _quadratic_builder(x: sp.Symbol, rng: Random) -> sp.Expr:
    return (
        _nonzero_int(rng, -3, 3) * x**2
        + rng.randint(-5, 5) * x
        + rng.randint(-6, 6)
    )


def _cubic_builder(x: sp.Symbol, rng: Random) -> sp.Expr:
    return (
        _nonzero_int(rng, -2, 2) * x**3
        + rng.randint(-3, 3) * x
        + rng.randint(-4, 4)
    )


def _sine_builder(x: sp.Symbol, rng: Random) -> sp.Expr:
    return _nonzero_int(rng, -4, 4) * sp.sin(_nonzero_int(rng, 1, 4) * x)


def _cosine_builder(x: sp.Symbol, rng: Random) -> sp.Expr:
    return _nonzero_int(rng, -4, 4) * sp.cos(_nonzero_int(rng, 1, 4) * x)


def _exponential_builder(x: sp.Symbol, rng: Random) -> sp.Expr:
    scale = rng.choice([sp.Rational(1, 5), sp.Rational(1, 4), sp.Rational(1, 3)])
    return _nonzero_int(rng, -3, 3) * sp.exp(scale * x) + rng.randint(-4, 4)


DEFAULT_BUILDERS: tuple[ExpressionBuilder, ...] = (
    _linear_builder,
    _quadratic_builder,
    _cubic_builder,
    _sine_builder,
    _cosine_builder,
    _exponential_builder,
)


def _button_rows(buttons: list[widgets.Button]) -> list[widgets.HBox]:
    return [
        widgets.HBox(buttons[index : index + 2])
        for index in range(0, len(buttons), 2)
    ]


def _expression_label(expr: sp.Expr) -> str:
    return str(expr).replace("**", "^")


def _nonzero_int(rng: Random, start: int, stop: int) -> int:
    value = 0
    while value == 0:
        value = rng.randint(start, stop)
    return value


def _same_expression(left: sp.Expr, right: sp.Expr) -> bool:
    return bool(sp.simplify(left - right) == 0)


def _display(value: object) -> None:
    ipython_display(value)  # type: ignore[no-untyped-call]


def _clear_output(*, wait: bool = False) -> None:
    ipython_clear_output(wait=wait)  # type: ignore[no-untyped-call]


__all__ = [
    "GuessQuestion",
    "GuessResult",
    "GuessingQuiz",
    "GuessingQuizWidget",
    "SympyGuessGame",
    "expression_points",
    "generate_options",
    "get_random_expression",
    "plot_expression",
]
