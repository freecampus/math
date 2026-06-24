import json
from collections.abc import Iterator
from typing import Any

import pytest
import sympy as sp

from edumath.core import parse_equation
from edumath.settings import configure, get_settings, reset_settings
from edumath.solvers import (
    EquationSolution,
    OpenAIEquationExplanationClient,
    extract_openai_response_text,
    solve_equation_steps,
)


@pytest.fixture(autouse=True)
def reset_edumath_settings() -> Iterator[None]:
    reset_settings()
    yield
    reset_settings()


class FakeExplanationClient:
    def __init__(self) -> None:
        self.seen: EquationSolution | None = None

    def explain_equation_solution(self, solution: EquationSolution) -> str:
        self.seen = solution
        return "First simplify, then isolate the variable."


class FailingExplanationClient:
    def explain_equation_solution(self, solution: EquationSolution) -> str:
        raise RuntimeError("service unavailable")


def test_solve_linear_equation_from_parsed_sympy_object() -> None:
    equation = parse_equation("2(x - 3) + 4 = 10")

    solution = solve_equation_steps(equation)

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


def test_solve_equation_accepts_expression_as_equal_to_zero() -> None:
    z = sp.Symbol("z")

    solution = solve_equation_steps(z - 4)

    assert solution.answer == "z = 4"
    assert solution.variable == z


def test_solver_infers_non_x_variable_from_parsed_equation() -> None:
    equation = parse_equation("2y + 3 = 7")

    solution = solve_equation_steps(equation)

    assert solution.answer == "y = 2"
    assert solution.variable == sp.Symbol("y")


def test_solver_requires_variable_for_multiple_symbol_equation() -> None:
    x, y = sp.symbols("x y")
    equation = sp.Eq(x + y, 5, evaluate=False)

    with pytest.raises(ValueError, match="Pass variable"):
        solve_equation_steps(equation)

    solution = solve_equation_steps(equation, variable=x)

    assert "5 - y" in solution.answer


def test_solver_rejects_raw_strings() -> None:
    with pytest.raises(TypeError, match="parse_equation"):
        solve_equation_steps("x + 3 = 7")  # type: ignore[arg-type]


def test_solve_quadratic_by_factoring() -> None:
    x = sp.Symbol("x")
    equation = sp.Eq(x**2 - 5 * x + 6, 0, evaluate=False)

    solution = solve_equation_steps(equation)

    assert solution.answer == "x ∈ {2, 3}"
    assert any(step.operation == "Factor" for step in solution.steps)
    assert all(check.valid is True for check in solution.checks)


def test_generic_solver_handles_rational_equation() -> None:
    t = sp.Symbol("t")
    equation = sp.Eq((t + 1) / (t - 2), 3, evaluate=False)

    solution = solve_equation_steps(equation)

    assert solution.answer == "t = 7/2"
    assert solution.method == "SymPy solveset"
    assert solution.checks[0].valid is True


def test_generic_solver_handles_exponential_equation() -> None:
    u = sp.Symbol("u")
    equation = sp.Eq(sp.exp(u), 5, evaluate=False)

    solution = solve_equation_steps(equation)

    assert solution.answer == "u = log(5)"
    assert solution.method == "SymPy solveset"


def test_solve_equation_uses_mock_explanation_client_when_explain_true() -> None:
    x = sp.Symbol("x")
    client = FakeExplanationClient()

    solution = solve_equation_steps(
        sp.Eq(x + 3, 7, evaluate=False),
        explain=True,
        explanation_client=client,
    )

    assert client.seen is not None
    assert solution.answer == "x = 4"
    assert solution.explanation == "First simplify, then isolate the variable."


def test_explain_false_skips_explanation_even_with_client() -> None:
    x = sp.Symbol("x")
    client = FakeExplanationClient()

    solution = solve_equation_steps(
        sp.Eq(x + 3, 7, evaluate=False),
        explain=False,
        explanation_client=client,
    )

    assert client.seen is None
    assert solution.explanation is None


def test_explain_true_without_configured_key_still_solves_locally() -> None:
    x = sp.Symbol("x")

    solution = solve_equation_steps(sp.Eq(x + 3, 7, evaluate=False), explain=True)

    assert solution.answer == "x = 4"
    assert solution.explanation is None
    assert solution.explanation_error is None


def test_explanation_errors_do_not_break_symbolic_solution_by_default() -> None:
    x = sp.Symbol("x")

    solution = solve_equation_steps(
        sp.Eq(x + 3, 7, evaluate=False),
        explain=True,
        explanation_client=FailingExplanationClient(),
    )

    assert solution.answer == "x = 4"
    assert solution.explanation is None
    assert solution.explanation_error == "service unavailable"


def test_settings_configure_can_set_clear_and_reset_values() -> None:
    configured = configure(
        openai_api_key="configured-key",
        openai_model="configured-model",
    )

    assert configured.openai_api_key == "configured-key"
    assert configured.openai_model == "configured-model"

    configure(openai_api_key=None)
    assert get_settings().openai_api_key is None
    assert get_settings().openai_model == "configured-model"

    reset_settings()
    assert get_settings().openai_api_key is None
    assert get_settings().openai_model != "configured-model"


def test_solver_uses_configured_openai_settings(monkeypatch: Any) -> None:
    x = sp.Symbol("x")
    captured: dict[str, Any] = {}

    class FakeHTTPResponse:
        def __enter__(self) -> "FakeHTTPResponse":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps({"output_text": "Configured explanation."}).encode()

    def fake_urlopen(request: Any, timeout: float) -> FakeHTTPResponse:
        captured["timeout"] = timeout
        captured["headers"] = dict(request.header_items())
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeHTTPResponse()

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    configure(openai_api_key="configured-key", openai_model="configured-model")

    solution = solve_equation_steps(sp.Eq(x + 1, 2, evaluate=False), explain=True)

    assert solution.explanation == "Configured explanation."
    assert captured["payload"]["model"] == "configured-model"
    assert captured["headers"]["Authorization"] == "Bearer configured-key"


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
    x = sp.Symbol("x")
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
    solution = solve_equation_steps(sp.Eq(x + 1, 2, evaluate=False))

    explanation = client.explain_equation_solution(solution)

    assert explanation == "AI explanation."
    assert captured["payload"]["model"] == "test-model"
    assert "input" in captured["payload"]
    assert captured["headers"]["Authorization"] == "Bearer test-key"


def test_generic_solver_handles_trigonometric_equation() -> None:
    theta = sp.Symbol("theta")
    equation = parse_equation("sin(theta) = 0")

    solution = solve_equation_steps(equation, domain=sp.Interval(0, sp.pi))

    assert "0" in solution.answer
    assert "pi" in solution.answer
    assert solution.variable == theta
    assert solution.method == "SymPy solveset"
