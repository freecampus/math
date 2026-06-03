# edu-math Contributor Guide

This file is the shared operating manual for AI contributors working in
`edu-math`.

## Project identity

- PyPI package: `edu-math`
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
