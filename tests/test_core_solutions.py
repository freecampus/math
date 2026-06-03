from edumath.core import (
    Exercise,
    SolutionStep,
    WorkedSolution,
    render_practice_set,
    render_solution_callout,
    render_solution_details,
)


def test_worked_solution_renders_answer_steps_and_check() -> None:
    solution = WorkedSolution(
        answer="x = 4",
        hint="Undo the addition first.",
        steps=(SolutionStep("Subtract 3", "`x + 3 = 7` becomes `x = 4`."),),
        check="Substitute: `4 + 3 = 7`.",
    )

    rendered = solution.render_markdown()

    assert "Hint: Undo the addition first." in rendered
    assert "Answer: x = 4" in rendered
    assert "**Subtract 3.**" in rendered
    assert "Check: Substitute" in rendered


def test_solution_callout_uses_collapsed_quarto_markup() -> None:
    rendered = render_solution_callout(WorkedSolution(answer="12"))

    assert 'collapse="true"' in rendered
    assert "## Solution" in rendered
    assert "Answer: 12" in rendered


def test_solution_details_uses_native_html_reveal() -> None:
    rendered = render_solution_details(WorkedSolution(answer="12"))

    assert '<details class="solution-reveal">' in rendered
    assert "<summary>Show solution</summary>" in rendered
    assert "Answer: 12" in rendered


def test_practice_set_renders_exercises_with_solution_reveals() -> None:
    exercise = Exercise(
        "Compute `2 + 2`.",
        expected=4,
        solution=WorkedSolution(answer="4"),
    )

    rendered = render_practice_set((exercise,))

    assert "::: {.practice-box}" in rendered
    assert "1. Compute `2 + 2`." in rendered
    assert "Answer: 4" in rendered
