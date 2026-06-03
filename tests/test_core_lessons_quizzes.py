from edumath.core import (
    AnswerOption,
    Exercise,
    LearningObjective,
    Lesson,
    LessonSection,
    Question,
    QuizSession,
    StudyPath,
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
