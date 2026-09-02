"""Structured models for symbolic step-by-step solving."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

import sympy as sp


@dataclass(frozen=True)
class EquationStep:
    """One algebraic transformation in an equation solution."""

    operation: str
    result: Any
    note: str = ""

    def result_text(self) -> str:
        """Return a readable representation of the step result."""

        if isinstance(self.result, str):
            return self.result
        return cast(str, sp.sstr(self.result))

    def render_text(self) -> str:
        """Render the step as plain text."""

        text = f"{self.operation}:\n{self.result_text()}"
        if self.note:
            text = f"{text}\n{self.note}"
        return text

    def render_markdown(self) -> str:
        """Render the step as Markdown."""

        parts = [f"**{self.operation}.**", f"`{self.result_text()}`"]
        if self.note:
            parts.append(self.note)
        return " ".join(parts)


@dataclass(frozen=True)
class EquationSolutionCheck:
    """Verification result for one candidate solution."""

    value: sp.Expr
    valid: bool | None

    def render_text(self, variable: sp.Symbol) -> str:
        """Render the verification result as plain text."""

        if self.valid is True:
            status = "valid"
        elif self.valid is False:
            status = "invalid"
        else:
            status = "unknown"
        return f"{variable} = {sp.sstr(self.value)}: {status}"


@dataclass(frozen=True)
class EquationSolution:
    """A SymPy-backed equation solution with optional tutor explanation."""

    original: sp.Basic
    variable: sp.Symbol
    solution_set: sp.Set
    steps: tuple[EquationStep, ...]
    checks: tuple[EquationSolutionCheck, ...] = ()
    method: str = "sympy"
    explanation: str | None = None
    explanation_error: str | None = None

    @property
    def solutions(self) -> tuple[sp.Expr, ...]:
        """Return finite solutions when the solution set is finite."""

        if isinstance(self.solution_set, sp.FiniteSet):
            return tuple(sp.sympify(value) for value in self.solution_set)
        return ()

    @property
    def answer(self) -> str:
        """Return a concise student-facing answer."""

        if self.solution_set == sp.S.EmptySet:
            return "No solution"
        if self.solution_set == sp.S.Reals:
            return "All real numbers"
        if isinstance(self.solution_set, sp.FiniteSet):
            values = sorted(self.solution_set, key=sp.default_sort_key)
            if len(values) == 1:
                return f"{self.variable} = {sp.sstr(values[0])}"
            joined = ", ".join(sp.sstr(value) for value in values)
            return f"{self.variable} ∈ {{{joined}}}"
        return f"{self.variable} ∈ {sp.sstr(self.solution_set)}"

    def render_text(self, *, include_explanation: bool = True) -> str:
        """Render the solution as plain text."""

        lines = [f"Answer: {self.answer}", f"Method: {self.method}"]
        if self.steps:
            lines.append("Steps:")
            lines.extend(
                f"{index}. {step.render_text()}"
                for index, step in enumerate(self.steps, start=1)
            )
        if self.checks:
            lines.append("Check:")
            lines.extend(check.render_text(self.variable) for check in self.checks)
        if include_explanation and self.explanation:
            lines.append("Explanation:")
            lines.append(self.explanation)
        if include_explanation and self.explanation_error:
            lines.append(f"Explanation skipped: {self.explanation_error}")
        return "\n\n".join(lines)

    def render_markdown(self, *, include_explanation: bool = True) -> str:
        """Render the solution as Markdown."""

        lines = [f"**Answer:** `{self.answer}`", f"**Method:** {self.method}"]
        if self.steps:
            lines.append("\n**Steps**")
            lines.extend(
                f"{index}. {step.render_markdown()}"
                for index, step in enumerate(self.steps, start=1)
            )
        if self.checks:
            lines.append("\n**Check**")
            lines.extend(
                f"- `{check.render_text(self.variable)}`" for check in self.checks
            )
        if include_explanation and self.explanation:
            lines.append("\n**Tutor explanation**")
            lines.append(self.explanation)
        if include_explanation and self.explanation_error:
            lines.append(f"\n_Explanation skipped: {self.explanation_error}_")
        return "\n".join(lines)


__all__ = ["EquationSolution", "EquationSolutionCheck", "EquationStep"]
