"""Optional AI explanation clients for solved math problems."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from edumath.solvers.models import EquationSolution

DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"
DEFAULT_OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


class EquationExplanationClient(Protocol):
    """Protocol for services that explain a verified equation solution."""

    def explain_equation_solution(self, solution: EquationSolution) -> str:
        """Return a short tutor explanation for an equation solution."""


@dataclass(frozen=True)
class OpenAIEquationExplanationClient:
    """Minimal OpenAI Responses API client for optional tutor explanations.

    The math is still produced and verified locally by SymPy/edumath. This
    client only turns the already-computed steps into student-friendly prose.
    """

    api_key: str
    model: str = DEFAULT_OPENAI_MODEL
    endpoint: str = DEFAULT_OPENAI_RESPONSES_URL
    timeout: float = 30.0
    max_output_tokens: int = 600

    def explain_equation_solution(self, solution: EquationSolution) -> str:
        """Ask OpenAI for a concise explanation of a solved equation."""

        if not self.api_key.strip():
            msg = "api_key must not be empty"
            raise ValueError(msg)

        payload = {
            "model": self.model,
            "instructions": _instruction_text(),
            "input": _equation_solution_prompt(solution),
            "max_output_tokens": self.max_output_tokens,
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            msg = f"OpenAI request failed with HTTP {error.code}: {detail}"
            raise RuntimeError(msg) from error
        except urllib.error.URLError as error:
            msg = f"OpenAI request failed: {error.reason}"
            raise RuntimeError(msg) from error

        data = json.loads(body)
        return extract_openai_response_text(data)


def extract_openai_response_text(data: dict[str, Any]) -> str:
    """Extract text from an OpenAI Responses API JSON object."""

    direct = data.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()

    fragments: list[str] = []
    for output_item in data.get("output", []):
        if not isinstance(output_item, dict):
            continue
        for content_item in output_item.get("content", []):
            if not isinstance(content_item, dict):
                continue
            if content_item.get("type") == "output_text":
                text = content_item.get("text")
                if isinstance(text, str) and text.strip():
                    fragments.append(text.strip())

    if fragments:
        return "\n\n".join(fragments)

    msg = "OpenAI response did not contain output text"
    raise RuntimeError(msg)


def _instruction_text() -> str:
    return (
        "You are a patient math tutor. Explain only the verified solution steps "
        "provided by the software. Do not invent a different method, do not add "
        "new algebraic steps, and do not change the final answer. Use clear, "
        "brief language suitable for a beginner."
    )


def _equation_solution_prompt(solution: EquationSolution) -> str:
    step_lines = "\n".join(
        f"{index}. {step.operation}: {step.result_text()}"
        for index, step in enumerate(solution.steps, start=1)
    )
    check_lines = "\n".join(
        check.render_text(solution.variable) for check in solution.checks
    )
    if solution.steps:
        original = solution.steps[0].result_text()
    else:
        original = str(solution.original)
    return (
        "Explain this solved equation to a student.\n\n"
        f"Original equation: {original}\n"
        f"Variable: {solution.variable}\n"
        f"Answer: {solution.answer}\n\n"
        "Verified solving steps:\n"
        f"{step_lines or '(no intermediate steps)'}\n\n"
        "Verification results:\n"
        f"{check_lines or '(not available)'}"
    )


__all__ = [
    "DEFAULT_OPENAI_MODEL",
    "DEFAULT_OPENAI_RESPONSES_URL",
    "EquationExplanationClient",
    "OpenAIEquationExplanationClient",
    "extract_openai_response_text",
]
