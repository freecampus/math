"""Calculus concept metadata."""

from __future__ import annotations

from edumath.core import LearningObjective, Lesson, LessonSection, StudyPath

LIMITS = Lesson(
    title="Limits",
    slug="limits",
    objectives=(
        LearningObjective("Explain limits as approached values."),
        LearningObjective("Estimate limits from tables and graphs."),
        LearningObjective("Distinguish function values from limiting values."),
    ),
    sections=(
        LessonSection(
            title="Nearby behavior",
            body="A limit describes what function values approach near a point.",
        ),
    ),
    tags=("calculus", "limits"),
)

DERIVATIVES = Lesson(
    title="Derivatives",
    slug="derivatives",
    objectives=(
        LearningObjective("Interpret derivatives as instantaneous rates."),
        LearningObjective("Connect secant slopes to tangent slopes."),
        LearningObjective("Write tangent line equations."),
    ),
    sections=(
        LessonSection(
            title="Instantaneous change",
            body="A derivative is the limiting slope of secant lines.",
        ),
    ),
    tags=("calculus", "derivatives"),
)

DERIVATIVE_RULES = Lesson(
    title="Derivative rules",
    slug="derivative-rules",
    objectives=(
        LearningObjective("Use power, product, quotient, and chain rules."),
        LearningObjective("Choose an appropriate derivative rule."),
        LearningObjective("Check symbolic derivatives."),
    ),
    sections=(
        LessonSection(
            title="Rule selection",
            body="Derivative rules turn common patterns into reusable shortcuts.",
        ),
    ),
    tags=("calculus", "derivatives", "rules"),
)

OPTIMIZATION = Lesson(
    title="Optimization",
    slug="optimization",
    objectives=(
        LearningObjective("Find critical points."),
        LearningObjective("Classify candidate maxima and minima."),
        LearningObjective("Check endpoints and context in applications."),
    ),
    sections=(
        LessonSection(
            title="Best values",
            body=(
                "Optimization uses derivatives to find and test candidate best values."
            ),
        ),
    ),
    tags=("calculus", "optimization"),
)

INTEGRALS = Lesson(
    title="Integrals",
    slug="integrals",
    objectives=(
        LearningObjective("Interpret definite integrals as accumulation."),
        LearningObjective("Compute basic antiderivatives."),
        LearningObjective("Approximate areas with Riemann sums."),
    ),
    sections=(
        LessonSection(
            title="Accumulation",
            body="An integral adds small pieces over an interval.",
        ),
    ),
    tags=("calculus", "integrals"),
)

INTEGRATION_TECHNIQUES = Lesson(
    title="Integration techniques",
    slug="integration-techniques",
    objectives=(
        LearningObjective("Recognize substitution patterns."),
        LearningObjective("Recognize integration by parts patterns."),
        LearningObjective("Use numerical approximations when needed."),
    ),
    sections=(
        LessonSection(
            title="Choosing techniques",
            body=(
                "Integration techniques are pattern-recognition tools for accumulation."
            ),
        ),
    ),
    tags=("calculus", "integrals", "techniques"),
)

CALCULUS_APPLICATIONS = Lesson(
    title="Calculus applications",
    slug="applications",
    objectives=(
        LearningObjective("Choose derivatives for local rate problems."),
        LearningObjective("Choose integrals for accumulation problems."),
        LearningObjective("Interpret calculus answers with units."),
    ),
    sections=(
        LessonSection(
            title="Modeling with calculus",
            body=(
                "Applications connect derivatives, integrals, optimization, and units."
            ),
        ),
    ),
    tags=("calculus", "applications", "modeling"),
)

CALCULUS_PATH = StudyPath(
    title="Calculus",
    lessons=(
        LIMITS,
        DERIVATIVES,
        DERIVATIVE_RULES,
        OPTIMIZATION,
        INTEGRALS,
        INTEGRATION_TECHNIQUES,
        CALCULUS_APPLICATIONS,
    ),
)

__all__ = [
    "CALCULUS_APPLICATIONS",
    "CALCULUS_PATH",
    "DERIVATIVES",
    "DERIVATIVE_RULES",
    "INTEGRALS",
    "INTEGRATION_TECHNIQUES",
    "LIMITS",
    "OPTIMIZATION",
]
