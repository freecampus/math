# FreeCampus Math Contributor Guide

This file is the shared operating manual for AI contributors working in
`FreeCampus Math`.

## Project identity

- PyPI package: `freecampus-math`
- Python import package: `fcmath`
- Repository: `freecampus/math`
- Build backend: Poetry
- Environment/workflow: conda + Poetry + Makim
- Runtime: Python 3.10+

## Repository layout

- `src/fcmath/`: package source
- `tests/`: pytest coverage
- `docs/`: Quarto documentation website
- `conda/`: conda environment files

## Development commands

```bash
conda env create -f conda/dev.yaml
conda activate fcmath
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
under `docs/courses/<course-id>/units/<unit-id>/`; avoid calling these pages
"notebooks" in navigation or lesson text unless the page is specifically about
notebook usage.

Courses must be designed as coherent, book-scale treatments suitable for
demanding university-level mathematics preparation. Lessons are chapters in that
book, not minimal API demonstrations or short topic summaries. They must be
self-contained enough for serious independent study and should combine precise
theory, derivations or proofs, visual intuition, step-by-step worked examples,
varied exercises with verified answers, selected complete solutions, cumulative
practice, and references to reputable textbooks or open educational resources.

The quality target is demonstrated rigor and learner capability, not prestige
language. Do not claim that material is rigorous merely because it resembles a
named institution, and do not mention one university or program as the reason
for the curriculum. Write for a general audience preparing for difficult
quantitative study and examinations.

### Book-scale rigor and examination readiness

Treat each active course as a complete textbook and assessed learning route. A
course plan must define:

- the learner profile and explicit prerequisite knowledge;
- course outcomes stated as observable mathematical performances;
- a coherent unit and chapter sequence with prerequisite links;
- a notation and terminology policy;
- where each outcome is introduced, practiced, synthesized, and assessed;
- a balanced problem bank, cumulative assessments, and grading criteria;
- the role of manual work, proof, visualization, numerical work, and symbolic
  computation;
- authoritative references and an attribution/licensing record;
- a definition of mastery and a definition of course completion.

Do not mark a course complete when it is only a survey. A learner should not
need an unspecified external textbook to supply missing explanations, examples,
proofs, or practice for the advertised outcomes.

#### Chapter depth

A substantive core lesson should read like a strong textbook chapter. Depending
on the topic, it will usually need:

- a motivating problem or phenomenon that organizes the chapter;
- a prerequisite retrieval check;
- precise definitions with examples and non-examples;
- several representations of the same idea when appropriate;
- derivations, theorem statements, and proofs at the learner's level;
- explicit treatment of domains, assumptions, parameters, signs, units, and
  exceptional cases;
- approximately 12–25 worked examples spanning routine through unfamiliar work;
- guided exercises after each important conceptual step;
- realistic incorrect solutions with diagnosis of the first invalid step;
- 3–6 distributed checkpoints for longer chapters;
- a substantial independent exercise set;
- concise answers for all exercises and complete solutions for a useful
  selection, including difficult problems;
- cumulative problems requiring earlier material;
- an examination clinic that demonstrates method selection and solution audit;
- a computational appendix and reputable references.

These figures are planning benchmarks, not padding quotas. A narrow lesson may
be shorter, while a foundational lesson may require more depth or a coherent
split. Never inflate prose to reach a number, but do not accept a few
definitions and examples as complete coverage of a major topic.

#### Mathematical rigor

Every mathematical contribution must:

- distinguish expressions, equations, identities, implications, biconditionals,
  and approximations;
- state the domain and assumptions needed for each transformation;
- explain whether a step is reversible and whether it can add or remove
  solutions;
- preserve excluded values when simplifying rational or radical expressions;
- distinguish a theorem from an observed pattern or computational conjecture;
- include boundary cases, degeneracies, equality cases, and counterexamples;
- derive important formulas when the derivation is accessible at this level;
- verify final results by substitution, an independent method, estimation, or
  interpretation;
- use notation consistently across prose, formulas, figures, exercises, and
  solutions.

Proofs should teach proof construction rather than present polished conclusions
without guidance. Introduce the strategic idea, identify the definition or
invariant being used, justify each logical step, and discuss why tempting
alternatives fail. When a full proof depends on later mathematics, state that
boundary honestly and prove the strongest appropriate result now.

#### Problem progression and difficult-exam preparation

Every unit needs a deliberate progression:

1. **Fluency:** one clearly identified skill with exact notation and arithmetic.
2. **Connected reasoning:** method choice, explanation, multiple
   representations, and routine proof.
3. **Synthesis:** unfamiliar multi-step work combining multiple lessons.
4. **Honors/examination:** proof, construction, counterexample, parameter
   classification, sharp bounds, functional relationships, or modeling where the
   method is not signaled.

Hard problems must be supported by earlier habits and examples. Do not create
difficulty through missing definitions, trivia, ambiguous wording, or enormous
arithmetic. Prefer structural difficulty: choosing a representation, finding an
invariant, separating parameter cases, controlling a domain, proving
completeness, or connecting several ideas.

Exercise sets must vary the reasoning, not merely the coefficients. Include
“find all,” “prove,” “disprove,” “construct,” “classify,” “compare,” and
“interpret” tasks; finite, empty, infinite, and parameter-dependent solution
sets; exact and approximate results; error analysis; and translation among
formula, graph, table, and context.

Every high-stakes practice examination must:

- map questions to published outcomes;
- sample both breadth and deep synthesis;
- contain unseen problems rather than copies of worked examples;
- include realistic time expectations and permitted-tool rules;
- provide a point-by-point rubric and complete checked solutions;
- reward valid reasoning and communication, not answer-only pattern matching;
- require corrections or targeted reassessment after review.

#### Solution standard

A complete solution should normally show:

1. interpretation of the question and definition of variables;
2. relevant domain, assumptions, and units;
3. a justified method and step-by-step argument;
4. correct algebra, logic, notation, and computation;
5. treatment of rejected, exceptional, or parameter-dependent cases;
6. verification or reasonableness analysis;
7. the final result in the form requested;
8. interpretation in context when applicable.

Answers and solutions must be independently checked. For difficult or
high-stakes problems, verify by a second method or reviewer when practical.
Never alter an expected answer merely to make an implementation test pass.

#### Computation serves mathematics

Use `fcmath`, SymPy, and numerical tools to explore, visualize, reproduce,
verify, and extend mathematical reasoning. Learners must still understand the
underlying mathematics. In particular:

- show the manual reasoning before or alongside solver output;
- distinguish exact symbolic results from floating-point approximations;
- inspect conditions and solution-set types returned by solvers;
- substitute candidates into the original problem;
- choose plot windows and sampling resolutions deliberately;
- discuss discontinuities, branches, asymptotes, numerical error, and missed
  roots where relevant;
- label computational evidence as evidence, not proof;
- make plots accessible with descriptive `fig-alt` text and meaningful axis
  labels.

The final computational appendix should empower reproduction and extension; it
must not be the first place where the mathematics is explained.

#### Course and chapter review gates

Before accepting a chapter, reviewers must be able to answer yes to all of the
following:

- Does it enable a clearly stated mathematical capability?
- Are its prerequisites already taught or explicitly reviewed?
- Are definitions, results, domains, and edge cases correct?
- Does it explain why the main methods work?
- Are examples sufficiently varied for transfer?
- Does practice move from guidance to independent synthesis?
- Can self-directed learners check every answer and study representative full
  solutions?
- Does at least one supported problem require unfamiliar reasoning?
- Does computation illuminate rather than conceal the mathematics?
- Is the chapter connected to earlier and later material?
- Are figures, tables, interactions, and generated notebooks accessible?
- Have the hardest claims and solutions been independently verified?

Before marking a course complete, audit the entire outcome map, prerequisite
graph, notation, cross-references, cumulative practice, examination coverage,
solution correctness, notebook execution, site accessibility, and references.

### Lesson structure

Use this general flow for each core lesson. Closely related items may be
combined when that improves the mathematical narrative, but do not omit the
learning function represented by a step:

1. YAML front matter with a clear `title`, `description`, and usually:

   ```yaml
   execute:
     echo: false
   ```

   This keeps helper code hidden by default.

2. Explicit prerequisites and a short retrieval warm-up.
3. An introduction organized around a meaningful mathematical problem or
   phenomenon.
4. Learning goals or "what you should be able to do" bullets, including a
   reasoning or explanation goal.
5. Notation, definitions, examples, and non-examples.
6. Intuition and connections among symbolic, graphical, numerical, geometric,
   and verbal representations as appropriate.
7. Important results with derivations or proofs and clearly stated conditions.
8. Worked examples with step-by-step reasoning, escalating from foundational
   cases through parameter, boundary, and synthesis cases. If Python/SymPy is
   used to compute or verify results in the main flow, hide the code and show
   the mathematical result and explanation.
9. Guided exercises and short checkpoints inside every major concept group.
10. Common mistakes, counterexamples, and repair of the first invalid step.
11. A difficult examination-style problem with strategy selection, a complete
    solution, and a final audit.
12. Independent practice grouped by fluency, connected reasoning, synthesis, and
    honors/examination difficulty.
13. Concise answers to every exercise plus collapsed full solutions for a
    representative selection. Include full solutions to enough difficult
    problems for self-directed study.
14. Cumulative retrieval using material from earlier lessons or units.
15. A topic-relevant interactive checkpoint, exploration, or guessing game.
16. A concise summary of key definitions, results, strategies, and unresolved
    future connections.
17. References and descriptive links to authoritative follow-up material.
18. A final section named `Using this lesson with fcmath and SymPy` that shows
    visible code examples (`#| echo: true`) for students who want to reproduce,
    verify, or extend the ideas computationally.

### Code visibility in lessons

- Hide implementation code in the main explanatory flow unless the code itself
  is the lesson objective.
- Show mathematical expressions, plots, tables, and step-by-step outcomes rather
  than raw setup code.
- Put visible Python examples at the end of the lesson in the fcmath/SymPy
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
instead of duplicating large blocks. Shared Quarto fragments live in
`docs/_includes/`; reusable mathematical behavior belongs in `src/fcmath/`.

### Source package support for lessons

Reusable lesson functionality belongs in `src/fcmath/` and should be organized
by math branch. Add or update package modules when they improve the pedagogy,
for example:

- plotting helpers;
- symbolic-question generators;
- quiz/answer checking utilities;
- step-by-step solution helpers;
- reusable data structures for expressions, equations, and functions.

Add tests in `tests/` for behavior changes in `src/fcmath/`. Keep the public API
intentionally small and documented.

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

## General Guidelines

When a lesson involves solving equations, add a dedicated section that
demonstrates how to solve the equations using SymPy. This section should
include:

- a clear explanation of the mathematical steps;
- the equivalent SymPy code;
- any important notes about interpreting the result;
- examples that help students connect the symbolic solution with the underlying
  math.

Also, whenever you notice an opportunity to improve the `fcmath` library,
suggest new reusable features, helper functions, visualizations, or utilities
that could support student learning. Prioritize proposals that are pedagogically
useful, reusable across lessons, and easy to integrate into the existing
library.

Ensure explanations include a step-by-step walkthrough that helps the learner
understand how to solve equations and work with formulas.

Each lesson subtopic may include guided exercises, checkpoint exercises, and a
topic-specific guessing game.
