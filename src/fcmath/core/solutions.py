"""Reusable solution models and Markdown rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionStep:
    """One explanatory step in a worked solution."""

    title: str
    body: str

    def render_markdown(self) -> str:
        """Render the step as Markdown."""

        if self.title:
            return f"**{self.title}.** {self.body}"
        return self.body


@dataclass(frozen=True)
class WorkedSolution:
    """A worked solution for an exercise or quiz question."""

    answer: str
    hint: str = ""
    explanation: str = ""
    steps: tuple[SolutionStep, ...] = ()
    check: str = ""

    def render_markdown(self) -> str:
        """Render the solution body as Markdown."""

        parts: list[str] = []
        if self.hint:
            parts.append(f"Hint: {self.hint}")

        parts.append(f"Answer: {self.answer}")

        if self.explanation:
            parts.append(self.explanation)

        if self.steps:
            step_lines = [
                f"{index}. {step.render_markdown()}"
                for index, step in enumerate(self.steps, start=1)
            ]
            parts.append("\n".join(step_lines))

        if self.check:
            parts.append(f"Check: {self.check}")

        return "\n\n".join(parts)


@dataclass(frozen=True)
class ExerciseSolution:
    """A solution attached to a stable exercise identifier."""

    exercise_id: str
    solution: WorkedSolution


@dataclass(frozen=True)
class SolutionReveal:
    """Rendering preferences for a revealable solution block."""

    summary: str = "Show solution"
    collapsed: bool = True
    callout: str = "tip"


def render_solution_callout(
    solution: WorkedSolution,
    *,
    title: str = "Solution",
    reveal: SolutionReveal | None = None,
) -> str:
    """Render a Quarto collapsed callout for a worked solution."""

    reveal = reveal or SolutionReveal()
    collapse = ' collapse="true"' if reveal.collapsed else ""
    return (
        f"::: {{.callout-{reveal.callout}{collapse}}}\n"
        f"## {title}\n\n"
        f"{solution.render_markdown()}\n"
        ":::\n"
    )


def render_solution_details(
    solution: WorkedSolution,
    *,
    summary: str = "Show solution",
) -> str:
    """Render a native HTML details block for a worked solution."""

    return (
        '<details class="solution-reveal">\n'
        f"<summary>{summary}</summary>\n\n"
        f"{solution.render_markdown()}\n\n"
        "</details>\n"
    )
