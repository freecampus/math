import json
from typing import Any

import sympy as sp

from edumath.solvers import (
    EquationSolution,
    OpenAIEquationExplanationClient,
    extract_openai_response_text,
    parse_equation,
    solve_equation_steps,
)


class FakeExplanationClient:
    def __init__(self) -> None:
        self.seen: EquationSolution | None = None

    def explain_equation_solution(self, solution: EquationSolution) -> str:
        self.seen = solution
        return "First simplify, then isolate the variable."


class FailingExplanationClient:
    def explain_equation_solution(self, solution: EquationSolution) -> str:
        raise RuntimeError("service unavailable")


def test_parse_equation_accepts_implicit_multiplication() -> None:
    equation = parse_equation("2x + 3 = 7")

    assert str(equation.lhs) == "2*x + 3"
    assert str(equation.rhs) == "7"


def test_solve_linear_equation_without_api_key_has_steps_and_no_explanation() -> None:
    solution = solve_equation_steps("2(x - 3) + 4 = 10")

    assert solution.answer == "x = 6"
    assert solution.explanation is None
    assert solution.explanation_error is None
    assert [step.operation for step in solution.steps] == [
        "Original equation",
        "Expand both sides",
        "Move everything to one side",
        "Move the constant term",
        "Divide by the coefficient of the variable",
    ]
    assert solution.checks[0].value == 6
    assert solution.checks[0].valid is True


def test_solve_quadratic_by_factoring() -> None:
    solution = solve_equation_steps("x^2 - 5x + 6 = 0")

    assert solution.answer == "x ∈ {2, 3}"
    assert any(step.operation == "Factor" for step in solution.steps)
    assert all(check.valid is True for check in solution.checks)


def test_solve_equation_uses_mock_explanation_client() -> None:
    client = FakeExplanationClient()

    solution = solve_equation_steps("x + 3 = 7", explanation_client=client)

    assert client.seen is not None
    assert solution.answer == "x = 4"
    assert solution.explanation == "First simplify, then isolate the variable."


def test_explain_false_skips_explanation_even_with_client() -> None:
    client = FakeExplanationClient()

    solution = solve_equation_steps(
        "x + 3 = 7", explain=False, explanation_client=client
    )

    assert client.seen is None
    assert solution.explanation is None


def test_explanation_errors_do_not_break_symbolic_solution_by_default() -> None:
    solution = solve_equation_steps(
        "x + 3 = 7",
        explanation_client=FailingExplanationClient(),
    )

    assert solution.answer == "x = 4"
    assert solution.explanation is None
    assert solution.explanation_error == "service unavailable"


def test_extract_openai_response_text_from_nested_output() -> None:
    data: dict[str, Any] = {
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": "Use inverse operations.",
                        "annotations": [],
                    }
                ],
            }
        ]
    }

    assert extract_openai_response_text(data) == "Use inverse operations."


def test_openai_client_builds_responses_api_request(monkeypatch: Any) -> None:
    captured: dict[str, Any] = {}

    class FakeHTTPResponse:
        def __enter__(self) -> "FakeHTTPResponse":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps({"output_text": "AI explanation."}).encode()

    def fake_urlopen(request: Any, timeout: float) -> FakeHTTPResponse:
        captured["timeout"] = timeout
        captured["headers"] = dict(request.header_items())
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeHTTPResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    client = OpenAIEquationExplanationClient(api_key="test-key", model="test-model")
    solution = solve_equation_steps("x + 1 = 2")

    explanation = client.explain_equation_solution(solution)

    assert explanation == "AI explanation."
    assert captured["payload"]["model"] == "test-model"
    assert "input" in captured["payload"]
    assert captured["headers"]["Authorization"] == "Bearer test-key"


def test_generic_solver_handles_trigonometric_equation() -> None:
    solution = solve_equation_steps("sin(x) = 0", domain=sp.Interval(0, sp.pi))

    assert "0" in solution.answer
    assert "pi" in solution.answer
    assert solution.method == "SymPy solveset"
