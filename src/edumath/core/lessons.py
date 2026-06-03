"""Pedagogical structures for lessons and study paths."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LearningObjective:
    """A measurable goal for a lesson."""

    description: str


@dataclass(frozen=True)
class LessonSection:
    """One section in a lesson."""

    title: str
    body: str
    examples: tuple[str, ...] = ()


@dataclass(frozen=True)
class Lesson:
    """A structured lesson outline."""

    title: str
    slug: str
    objectives: tuple[LearningObjective, ...]
    sections: tuple[LessonSection, ...]
    prerequisites: tuple[str, ...] = ()
    summary: str = ""
    tags: tuple[str, ...] = ()

    def objective_text(self) -> list[str]:
        """Return objectives as plain strings."""

        return [objective.description for objective in self.objectives]


@dataclass(frozen=True)
class StudyPath:
    """Ordered collection of lessons."""

    title: str
    lessons: tuple[Lesson, ...] = field(default_factory=tuple)

    def slugs(self) -> list[str]:
        """Return lesson slugs in order."""

        return [lesson.slug for lesson in self.lessons]
