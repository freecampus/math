# Contributing

Thank you for your interest in contributing to `edu-math`.

## Development setup

```bash
conda env create -f conda/dev.yaml
conda activate edumath
poetry config virtualenvs.create false
poetry install --extras "dev"
```

## Checks

```bash
makim tests.linter
makim tests.unit
makim package.build
makim docs.build
```

## Pull requests

Keep changes focused, add tests for behavior changes, and update documentation
when public APIs or user-facing workflows change.
