"""Shared building blocks used by math branch packages."""

from edumath.core.answers import (
    AnswerCheck,
    NumericTolerance,
    check_expression_answer,
    check_numeric_answer,
)
from edumath.core.exercises import Exercise
from edumath.core.expressions import (
    MathExpression,
    expression_equivalent,
    parse_expression,
)
from edumath.core.lessons import LearningObjective, Lesson, LessonSection, StudyPath
from edumath.core.plots import (
    ExplicitFunction2D,
    ParametricCurve2D,
    PlotRange,
    PlotScene2D,
    PlotStyle,
    Point2D,
    PolarCurve2D,
    SampledCurve2D,
    Segment2D,
    Viewport2D,
)
from edumath.core.quizzes import AnswerOption, Question, QuizResult, QuizSession
from edumath.core.widgets import NotebookDisplay

__all__ = [
    "AnswerCheck",
    "AnswerOption",
    "Exercise",
    "ExplicitFunction2D",
    "LearningObjective",
    "Lesson",
    "LessonSection",
    "MathExpression",
    "NotebookDisplay",
    "NumericTolerance",
    "ParametricCurve2D",
    "PlotRange",
    "PlotScene2D",
    "PlotStyle",
    "Point2D",
    "PolarCurve2D",
    "Question",
    "QuizResult",
    "QuizSession",
    "SampledCurve2D",
    "Segment2D",
    "StudyPath",
    "Viewport2D",
    "check_expression_answer",
    "check_numeric_answer",
    "expression_equivalent",
    "parse_expression",
]
