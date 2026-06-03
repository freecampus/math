# edu-math

![CI](https://img.shields.io/github/actions/workflow/status/osl-incubator/edu-math/ci.yml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/edu-math)](https://pypi.org/project/edu-math/)
[![Package Version](https://img.shields.io/pypi/v/edu-math?color=blue)](https://pypi.org/project/edu-math/)
![License](https://img.shields.io/pypi/l/edu-math?color=blue)

`edu-math` is a Python package for math education workflows.

The project is in its initial scaffold stage. The repository includes packaging,
testing, linting, documentation, release automation, and GitHub workflow
infrastructure adapted from the Open Science Labs Incubator Python package
template used by `prisma-flow`.

## Installation

```bash
pip install edu-math
```

## Development

```bash
conda env create -f conda/dev.yaml
conda activate edumath
poetry config virtualenvs.create false
poetry install --extras "dev"
```

Run checks through Makim:

```bash
makim tests.linter
makim tests.unit
makim package.build
makim docs.build
```

## Project layout

- `src/edumath/`: Python package source
- `tests/`: pytest test suite
- `docs/`: Quarto documentation website
- `conda/`: development and release environment files
- `.github/`: issue templates and GitHub Actions workflows
