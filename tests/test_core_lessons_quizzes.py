import sympy as sp

from edumath.core import (
    AnswerCheck,
    AnswerOption,
    Exercise,
    LearningObjective,
    Lesson,
    LessonSection,
    Question,
    QuizSession,
    StudyPath,
    SympyResolver,
)


def test_lesson_and_study_path_store_ordered_metadata() -> None:
    lesson = Lesson(
        title="Example",
        slug="example",
        objectives=(LearningObjective("Understand the example."),),
        sections=(LessonSection("Idea", "Body"),),
    )
    path = StudyPath("Path", lessons=(lesson,))

    assert lesson.objective_text() == ["Understand the example."]
    assert path.slugs() == ["example"]


def test_exercise_checks_exact_answer_when_no_validator_is_provided() -> None:
    exercise = Exercise("What is 2 + 2?", expected=4)

    assert exercise.check(4).correct
    assert not exercise.check(5).correct


def test_quiz_session_scores_answered_questions() -> None:
    question = Question(
        prompt="Choose 1.",
        expected=1,
        options=(AnswerOption("1", 1), AnswerOption("2", 2)),
    )
    session = QuizSession((question,))

    result = session.answer(0, 1)

    assert result.check.correct
    assert session.score == 1
    assert session.complete


def test_question_checks_symbolic_expected_answers() -> None:
    x = sp.Symbol("x")
    question = Question(
        prompt="Expand (x + 1)^2.",
        expected=x**2 + 2 * x + 1,
        answer_type="symbolic",
    )

    assert question.check("(x + 1)**2").correct


def test_question_resolves_expected_answer_from_expression() -> None:
    x = sp.Symbol("x")
    question = Question(
        prompt="Expand the expression.",
        expression=(x + 1) ** 2,
        resolver="expand",
        answer_type="symbolic",
    )

    assert question.resolve_expected() == x**2 + 2 * x + 1
    assert question.check("x**2 + 2*x + 1").correct


def test_question_resolver_accepts_operation_settings() -> None:
    x = sp.Symbol("x")
    question = Question(
        prompt="Differentiate sin(x^2).",
        expression=sp.sin(x**2),
        resolver=SympyResolver("differentiate", variable=x),
        answer_type="symbolic",
    )

    assert question.check("2*x*cos(x**2)").correct


def test_question_uses_custom_validator_first() -> None:
    question = Question(
        prompt="Enter any even integer.",
        validator=lambda received: AnswerCheck(
            correct=int(received) % 2 == 0,
            received=received,
            expected="an even integer",
        ),
    )

    assert question.check(4).correct
    assert not question.check(5).correct


def test_question_without_expected_answer_is_not_auto_checkable() -> None:
    question = Question(prompt="Explain why the graph is increasing.")

    result = question.check("It has positive slope.")

    assert not result.correct
    assert result.expected is None
