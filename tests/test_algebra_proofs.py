import pytest

from fcmath.algebra import (
    ProofStep,
    find_implication_counterexample,
    proof_steps_markdown,
)


def test_proof_steps_render_as_markdown_audit_table() -> None:
    rendered = proof_steps_markdown(
        [
            ProofStep("n = 2k + 1", "definition of odd"),
            ProofStep("n² = 4k² + 4k + 1", "expansion"),
        ]
    )

    assert rendered.startswith("| Step | Statement | Justification |")
    assert "| 1 | n = 2k + 1 | definition of odd |" in rendered
    assert "| 2 | n² = 4k² + 4k + 1 | expansion |" in rendered


def test_proof_steps_reject_missing_content() -> None:
    with pytest.raises(ValueError, match="statement"):
        ProofStep(" ", "reason")
    with pytest.raises(ValueError, match="justification"):
        ProofStep("claim", "")
    with pytest.raises(ValueError, match="at least one"):
        proof_steps_markdown([])


def test_proof_renderer_escapes_table_syntax_and_line_breaks() -> None:
    rendered = proof_steps_markdown(
        [ProofStep("a | b\nand b | c", "definition | substitution")]
    )

    assert "a \\| b<br>and b \\| c" in rendered
    assert "definition \\| substitution" in rendered


def test_counterexample_search_requires_true_hypothesis_and_false_conclusion() -> None:
    counterexample = find_implication_counterexample(
        range(-5, 6),
        hypothesis=lambda value: value**2 > 4,
        conclusion=lambda value: value > 2,
    )

    assert counterexample == -5


def test_counterexample_search_returns_none_when_sample_supports_claim() -> None:
    counterexample = find_implication_counterexample(
        range(-10, 11),
        hypothesis=lambda value: value % 2 == 0,
        conclusion=lambda value: value**2 % 2 == 0,
    )

    assert counterexample is None
