#!/usr/bin/env python3
"""Create a safe draft scaffold from one Advanced Algebra coverage entry."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fcmath.validation import load_structured_data

DEFAULT_COVERAGE = ROOT / "docs/courses/advanced-algebra/_coverage.yml"


def build_chapter_scaffold(
    coverage: Mapping[str, Any],
    chapter_id: str,
    *,
    lesson_id: str,
    estimated_minutes: int,
) -> str:
    """Return a draft QMD scaffold for ``chapter_id``."""

    unit, chapter = _find_chapter(coverage, chapter_id)
    title = str(chapter["title"])
    description = str(chapter["scope"])
    unit_id = str(unit["id"])
    outcomes = ", ".join(str(value) for value in chapter["outcome_ids"])
    problem_prefix = _problem_prefix(str(chapter["number"]))
    prerequisite = next(
        iter(chapter["prerequisite_chapter_ids"]), "the prerequisite chapter"
    )
    return f'''---
title: "{title}"
description: "{description}"
execute:
  echo: false
  warning: false
id: {lesson_id}
course_id: advanced-algebra
unit_id: {unit_id}
page_type: lesson
status: draft
estimated_time: "{estimated_minutes} minutes"
skill_modes:
  [conceptual, manual-calculation, symbolic-reasoning, computational, interpretation]
outcome_ids: [{outcomes}]
---

## Why this matters

Write the organizing problem and explain the capability this chapter develops.

::: {{.learning-objectives}}
### What you should be able to do

- State the first measurable capability.
- Carry out and justify the principal method.
- Diagnose a boundary case or invalid argument.
:::

::: {{.prerequisites}}
### Prerequisites

Retrieve the exact ideas from `{prerequisite}` that this chapter uses.
:::

## Five-minute retrieval warm-up

Give three to five prerequisite questions, followed by a collapsed answer block.

## 1. Definitions, conditions, and notation

State definitions, hypotheses, examples, nonexamples, and boundary cases.

::: {{.worked-example}}
### Example 1: foundational reasoning

Show the plan, justified steps, conclusion, and independent check.
:::

## 2. Derivation and connected representations

Derive the main result and connect symbolic, graphical, numerical, or verbal
representations where appropriate.

::: {{.checkpoint data-problem-id="{problem_prefix}-checkpoint-01" data-level="A"}}
### Concept checkpoint

Pose one focused decision question.

::: {{.callout-tip collapse="true" title="Answer and explanation"}}
Supply the answer, decisive idea, and misconception repair.
:::
:::

## 3. Guided practice and verification

::: {{.practice-box data-problem-id="{problem_prefix}-guided-01" data-level="B"}}
### Guided exercise

Pose a transfer problem with a graduated hint.

::: {{.callout-note collapse="true" title="Hint"}}
Name a representation or first step without giving the answer.
:::

::: {{.callout-tip collapse="true" title="Step-by-step solution"}}
State conditions, justify each step, verify the result, and interpret it.
:::
:::

## 4. Common mistakes and limitations

Show realistic invalid solutions, the first invalid step, counterexamples, and
repairs.

## 5. Examination strategy clinic

Give one supported Level D problem with strategy selection, complete solution,
and final audit.

## 6. Exercises by purpose and difficulty

Add substantial Level A, B, C, and D sets with stable IDs, concise answers to
all items, and selected full solutions.

## 7. Cumulative retrieval

Add at least two problems that retrieve earlier chapters without naming the
needed method in the prompt.

## 8. Topic checkpoint

Add a topic-specific interaction. Preserve a static question and collapsed
solution so the generated notebook remains complete without JavaScript.

## 9. Summary and next step

Summarize definitions, decisions, validity conditions, and the next dependency.

## References and further study

List only sources actually consulted, with rights-aware descriptive links.

## Using this lesson with fcmath and SymPy

Show visible, runnable code that reproduces and checks the manual mathematics.

```{{python}}
#| echo: true
import sympy as sp

from fcmath import parse_expression

x = sp.symbols("x", real=True)
expression = parse_expression("x^2 - 1", variables=(x,))
sp.factor(expression)
```
'''


def write_chapter_scaffold(
    coverage_path: Path,
    chapter_id: str,
    output: Path,
    *,
    lesson_id: str,
    estimated_minutes: int,
    force: bool = False,
) -> None:
    """Write a chapter scaffold without overwriting by default."""

    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite {output}")
    coverage = load_structured_data(coverage_path)
    text = build_chapter_scaffold(
        coverage,
        chapter_id,
        lesson_id=lesson_id,
        estimated_minutes=estimated_minutes,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def _find_chapter(
    coverage: Mapping[str, Any], chapter_id: str
) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    for raw_unit in coverage.get("units", []):
        if not isinstance(raw_unit, Mapping):
            continue
        unit = cast(Mapping[str, Any], raw_unit)
        for raw_chapter in unit.get("chapters", []):
            if isinstance(raw_chapter, Mapping) and raw_chapter.get("id") == chapter_id:
                return unit, cast(Mapping[str, Any], raw_chapter)
    raise KeyError(f"unknown chapter ID {chapter_id!r}")


def _problem_prefix(number: str) -> str:
    if not re.fullmatch(r"\d+\.\d+", number):
        raise ValueError(f"unsupported chapter number {number!r}")
    return "aa-" + number.replace(".", "-")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("chapter_id")
    parser.add_argument("output", type=Path)
    parser.add_argument("--coverage", type=Path, default=DEFAULT_COVERAGE)
    parser.add_argument("--lesson-id", required=True)
    parser.add_argument("--estimated-minutes", type=int, default=480)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.estimated_minutes < 1:
        parser.error("--estimated-minutes must be positive")
    try:
        write_chapter_scaffold(
            args.coverage,
            args.chapter_id,
            args.output,
            lesson_id=args.lesson_id,
            estimated_minutes=args.estimated_minutes,
            force=args.force,
        )
    except (FileExistsError, KeyError, ValueError) as error:
        parser.error(str(error))
    print(f"Created draft chapter scaffold: {args.output}")
    print("Next: add it to the catalog and coverage matrix before review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
