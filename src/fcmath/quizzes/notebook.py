"""Optional ipywidgets renderer for the shared quiz model."""

from __future__ import annotations

from dataclasses import dataclass, field

import ipywidgets as widgets
from IPython.display import Markdown, display

from fcmath.quizzes.models import QuizBank, QuizQuestion


@dataclass
class NotebookQuiz:
    """Accessible one-question-at-a-time notebook quiz.

    Importing :mod:`fcmath.quizzes` does not import Jupyter.  This optional
    renderer is loaded only when a notebook explicitly requests it.
    """

    bank: QuizBank
    current: int = 0
    answers: dict[str, object] = field(default_factory=dict)
    results: dict[str, bool] = field(default_factory=dict)

    def display(self) -> widgets.VBox:
        """Display and return the quiz widget container."""

        container = widgets.VBox()
        self._render(container)
        display(container)  # type: ignore[no-untyped-call]
        return container

    def static_markdown(self) -> str:
        """Return readable questions and collapsed-solution-friendly text."""

        parts = [f"## {self.bank.title}"]
        for index, question in enumerate(self.bank.questions, start=1):
            parts.extend(
                (
                    f"### {index}. {question.prompt}",
                    _option_markdown(question),
                    "<details><summary>Solution</summary>\n\n"
                    f"{question.explanation}\n\n</details>",
                )
            )
        return "\n\n".join(part for part in parts if part)

    def _render(self, container: widgets.VBox) -> None:
        question = self.bank.questions[self.current]
        question_number = self.current + 1
        question_total = len(self.bank.questions)
        progress = widgets.HTML(
            f"<strong>Question {question_number} of {question_total}</strong><br>"
            f"Answered {len(self.results)}; correct {sum(self.results.values())}."
        )
        prompt = widgets.HTMLMath(value=question.prompt)
        control = _answer_control(question)
        hint = widgets.HTMLMath(
            value=(
                f"<details><summary>Hint</summary>{question.hint}</details>"
                if question.hint
                else ""
            )
        )
        feedback = widgets.HTMLMath()
        check = widgets.Button(description="Check answer", button_style="primary")
        previous = widgets.Button(description="Previous", disabled=self.current == 0)
        following = widgets.Button(
            description="Next",
            disabled=self.current == len(self.bank.questions) - 1,
        )
        reset = widgets.Button(description="Reset quiz")

        def check_answer(_button: widgets.Button) -> None:
            answer = _control_value(control, question)
            if answer in (None, "", ()):
                feedback.value = "Choose or enter an answer first."
                return
            self.answers[question.id] = answer
            result = question.check(answer)
            self.results[question.id] = result.correct
            label = "Correct." if result.correct else "Not yet."
            feedback.value = (
                f"<strong>{label}</strong> {result.message} {question.explanation}"
            )
            progress.value = (
                f"<strong>Question {question_number} of {question_total}</strong><br>"
                f"Answered {len(self.results)}; correct {sum(self.results.values())}."
            )

        def move(offset: int) -> None:
            self.current += offset
            self._render(container)

        check.on_click(check_answer)
        previous.on_click(lambda _button: move(-1))
        following.on_click(lambda _button: move(1))

        def reset_quiz(_button: widgets.Button) -> None:
            self.current = 0
            self.answers.clear()
            self.results.clear()
            self._render(container)

        reset.on_click(reset_quiz)
        container.children = (
            progress,
            prompt,
            control,
            hint,
            widgets.HBox((check, previous, following, reset)),
            feedback,
        )


def _answer_control(question: QuizQuestion) -> widgets.Widget:
    options = [(option.text, option.id) for option in question.options]
    if question.type == "single-choice":
        return widgets.RadioButtons(options=options, value=None, description="Answer:")
    if question.type == "multiple-select":
        return widgets.SelectMultiple(options=options, description="Answers:")
    return widgets.Text(description="Answer:", continuous_update=False)


def _control_value(control: widgets.Widget, question: QuizQuestion) -> object:
    value = getattr(control, "value", "")
    if question.type == "multiple-select":
        return list(value)
    return value


def _option_markdown(question: QuizQuestion) -> str:
    if not question.options:
        return "Write your answer before revealing the solution."
    return "\n".join(f"- [ ] {option.text}" for option in question.options)


__all__ = ["Markdown", "NotebookQuiz"]
