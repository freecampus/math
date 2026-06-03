from edumath.core import check_expression_answer, check_numeric_answer


def test_check_numeric_answer_uses_tolerance() -> None:
    result = check_numeric_answer(1.0000000001, 1.0)

    assert result.correct


def test_check_expression_answer_accepts_equivalent_forms() -> None:
    result = check_expression_answer("2*x + x", "3*x")

    assert result.correct
