import json
from pathlib import Path

import pytest

from fcmath.quizzes import load_quiz, quiz_from_mapping

ROOT = Path(__file__).resolve().parents[2]


def test_diagnostic_bank_loads_and_checks_with_shared_model() -> None:
    bank = load_quiz(ROOT / "docs/quizzes/pathway/diagnostic.yml")

    assert bank.id == "quantitative-mathematics-diagnostic"
    assert len(bank.questions) == 18
    assert bank.check("diagnostic-algebra-equation", "6").correct
    assert bank.check("diagnostic-algebra-domain", ["b", "a"]).correct
    assert bank.check("diagnostic-calculus-derivative", "3*x*x - 4").correct


def test_schema_requires_explanations_and_learning_outcomes() -> None:
    data = json.loads((ROOT / "docs/quizzes/pathway/diagnostic.yml").read_text())
    del data["questions"][0]["explanation"]

    with pytest.raises(ValueError, match="explanation"):
        quiz_from_mapping(data)


def test_numeric_schema_requires_explicit_tolerances() -> None:
    data = json.loads((ROOT / "docs/quizzes/pathway/diagnostic.yml").read_text())
    del data["questions"][0]["validation"]["absolute_tolerance"]

    with pytest.raises(ValueError, match="both tolerances"):
        quiz_from_mapping(data)


def test_schema_rejects_duplicate_question_ids() -> None:
    data = json.loads((ROOT / "docs/quizzes/pathway/diagnostic.yml").read_text())
    data["questions"][1]["id"] = data["questions"][0]["id"]

    with pytest.raises(ValueError, match="unique"):
        quiz_from_mapping(data)


def test_schema_rejects_invalid_ids_modes_and_type_policy_pairs() -> None:
    source = (ROOT / "docs/quizzes/pathway/diagnostic.yml").read_text()

    invalid_id = json.loads(source)
    invalid_id["questions"][0]["id"] = "Not stable"
    with pytest.raises(ValueError, match="kebab-case"):
        quiz_from_mapping(invalid_id)

    invalid_skill = json.loads(source)
    invalid_skill["questions"][0]["skill_mode"] = "memorization"
    with pytest.raises(ValueError, match="skill mode"):
        quiz_from_mapping(invalid_skill)

    invalid_pair = json.loads(source)
    invalid_pair["questions"][0]["validation"] = {
        "mode": "exact",
        "absolute_tolerance": 0,
        "relative_tolerance": 0,
    }
    with pytest.raises(ValueError, match="incompatible"):
        quiz_from_mapping(invalid_pair)
