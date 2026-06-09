# edu-math Contributor Guide

This file is the shared operating manual for AI contributors working in
`edu-math`.

## Project identity

- PyPI package: `osl-edu-math`
- Python import package: `edumath`
- Repository: `osl-incubator/edu-math`
- Build backend: Poetry
- Environment/workflow: conda + Poetry + Makim
- Runtime: Python 3.10+

## Repository layout

- `src/edumath/`: package source
- `tests/`: pytest coverage
- `docs/`: Quarto documentation website
- `conda/`: conda environment files

## Development commands

```bash
conda env create -f conda/dev.yaml
conda activate edumath
poetry config virtualenvs.create false
poetry install --extras "dev"
```

Makim workflow:

```bash
makim tests.linter
makim tests.unit
makim package.build
makim docs.build
makim all.ci
```

## Implementation rules

1. Keep the public API small and documented.
2. Prefer standard-library implementations until a dependency is clearly
   justified.
3. Add tests for behavior changes.
4. Keep README, docs, and examples in sync with public API changes.

## Documentation and lesson standards

The documentation is a Quarto website. Student-facing course material belongs
under `docs/lessons/`; avoid calling these pages "notebooks" in navigation or
lesson text unless the page is specifically about notebook usage.

Lessons should be complete, pedagogical study material for university-level math
preparation. They should not be minimal API demos. Prefer self-contained
explanations, worked examples, visual intuition, exercises with answers, and
references to reputable textbooks or open educational resources. Do not mention
one specific university or program as the reason for the curriculum; write for a
general audience of learners preparing for advanced quantitative study.

### Lesson structure

Use this general flow for each lesson:

1. YAML front matter with a clear `title`, `description`, and usually:

   ```yaml
   execute:
     echo: false
   ```

   This keeps helper code hidden by default.

2. A short introduction explaining why the topic matters.
3. Learning goals or "what you should be able to do" bullets.
4. Concept sections with definitions, intuition, formulas, and common pitfalls.
5. Worked examples with step-by-step reasoning. If Python/SymPy is used to
   compute or verify results in the middle of the lesson, hide the code and show
   the mathematical result/explanation.
6. Practice exercises. When possible, solve them directly on the page. If an
   answer would interrupt the flow, place it in a collapsed answer/solution
   block so students can try first.
7. A topic-relevant interactive checkpoint or guessing game before the Python
   appendix.
8. A final section named `Using this lesson with edumath and SymPy` that shows
   visible code examples (`#| echo: true`) for students who want to reproduce or
   extend the ideas computationally.

### Code visibility in lessons

- Hide implementation code in the main explanatory flow unless the code itself
  is the lesson objective.
- Show mathematical expressions, plots, tables, and step-by-step outcomes rather
  than raw setup code.
- Put visible Python examples at the end of the lesson in the edumath/SymPy
  appendix.
- Keep examples runnable in Quarto and reusable in Jupyter/Colab when practical.

### Interactive pedagogy

Interactive elements should support the lesson topic, not be generic decoration.
Good examples include sliders for parameters, plots that reveal behavior across
inputs, quizzes, and guessing games.

Guessing games should be flexible and topic-specific. Depending on the lesson,
the prompt might ask students to guess:

- an expression from a graph;
- a value from an expression;
- an equivalent form after expansion, factoring, or simplification;
- an equation solution;
- an inequality solution set or interval;
- a transformation, inverse, or composition result;
- roots, multiplicities, end behavior, or factorization;
- a system's intersection point or classification.

When a pattern is reusable across lessons, create or update shared code/includes
instead of duplicating large blocks. For Algebra lesson pages, shared Quarto
fragments may live in `docs/lessons/algebra/_includes/`.

### Source package support for lessons

Reusable lesson functionality belongs in `src/edumath/` and should be organized
by math branch. Add or update package modules when they improve the pedagogy,
for example:

- plotting helpers;
- symbolic-question generators;
- quiz/answer checking utilities;
- step-by-step solution helpers;
- reusable data structures for expressions, equations, and functions.

Add tests in `tests/` for behavior changes in `src/edumath/`. Keep the public
API intentionally small and documented.

### Documentation validation

For docs-only changes, run scoped checks when possible:

```bash
poetry run pre-commit run --files <changed files>
quarto render <changed .qmd files> --no-execute
```

For broader changes, use:

```bash
makim docs.build
makim all.ci
```

Do not commit generated scratch/session files. If Quarto creates temporary
`docs/.quarto/quarto-session-temp*` folders during local rendering, remove them
before finishing.
