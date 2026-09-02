# Contributing

Thank you for improving FreeCampus Math.

## Development setup

```bash
conda env create -f conda/dev.yaml
conda activate fcmath
poetry config virtualenvs.create false
poetry install --extras "dev"
```

## Curriculum source of truth

`docs/courses/_catalog.yml` owns stable pathway, course, unit, lesson,
assessment, and outcome IDs. QMD files are canonical lesson sources. Do not edit
`docs/_quarto.yml`, generated manifests, or `notebooks/` by hand; update the
catalog or QMD and run the generators.

A lesson should expose prerequisites and measurable outcomes, build intuition
without weakening definitions, state hypotheses and failure cases, show complete
manual solutions, include guided and checkpoint practice, and make computation
reproducible and interpretable. See `AGENTS.md` for the complete lesson
standard.

## Add or revise curriculum material

1. Start from the appropriate file in `docs/_templates/`. Reusable mathematical
   component patterns are documented in `docs/_includes/math-components.qmd`.
2. Add the course, unit, lesson, challenge, or assessment record to
   `docs/courses/_catalog.yml`. Keep existing IDs stable; IDs are used by links,
   generated notebooks, quizzes, and local progress.
3. Declare measurable outcomes, estimated time, skill modes, prerequisites, and
   computational dependencies in the catalog and QMD metadata. Course outcomes
   live in each course's `_outcomes.yml`.
4. Put reusable quiz banks in `docs/quizzes/`. Every question needs a unique ID,
   outcome ID, explanation, hint, and explicit answer-validation policy. Never
   evaluate learner input as Python.
5. Write theory and manual reasoning first. State hypotheses and domains, show
   complete transformations, distinguish exact from approximate results, and
   verify conclusions independently. Computation should illuminate or check the
   mathematics rather than replace it.
6. Regenerate catalog-derived navigation and notebooks:

   ```bash
   makim curriculum.generate
   makim notebooks.build
   ```

7. Review the HTML, generated notebook, mobile layout, keyboard flow, dark mode,
   and print view. Generated notebooks are committed to provide stable Colab
   URLs, but must never be edited directly.

The catalog uses JSON-compatible YAML so the standard library can validate it in
minimal environments. Quiz banks may use regular YAML and therefore require
PyYAML. Do not publish an empty course shell: use the candid `planned` or
`in-development` status until learners have substantive material.

## Generated and transient files

The following files are generated and should be changed only through their
sources:

- `docs/_quarto.yml`, `docs/_sidebar.yml`, course cards, course outcome files,
  and unit metadata files;
- `docs/assets/curriculum-map.json`, navigation, and prerequisite manifests;
- every file under `notebooks/`.

Quarto output belongs in `build/`. Do not commit `docs/_freeze`,
`docs/.quarto/quarto-session-temp*`, caches, executed notebook output, or local
progress exports.

## Checks

```bash
makim curriculum.validate
makim tests.linter
makim tests.unit
makim notebooks.check
makim package.build
makim docs.build
```

For docs-only changes, run pre-commit on changed files and render the affected
QMD with `--no-execute`. Remove `docs/.quarto/quarto-session-temp*` directories
before finishing.

The full CI pipeline also executes a representative generated notebook from each
course in a clean environment. The scheduled/main suite may execute all
notebooks; learner-exercise cells remain unexecuted.

## Pull requests

Keep stable IDs unchanged unless a catalog migration is included. Add tests for
behavior changes, regenerate derived files, document public API changes, and
state which accessibility and rendering checks were run.
