# edu-math

![CI](https://img.shields.io/github/actions/workflow/status/osl-incubator/edu-math/ci.yml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/osl-edu-math)](https://pypi.org/project/osl-edu-math/)
[![Package Version](https://img.shields.io/pypi/v/osl-edu-math?color=blue)](https://pypi.org/project/osl-edu-math/)
![License](https://img.shields.io/pypi/l/osl-edu-math?color=blue)

`edu-math` is a Python package for math education workflows.

The PyPI distribution is `osl-edu-math`; the import package remains `edumath`.

The project is in its initial scaffold stage. The repository includes packaging,
testing, linting, documentation, release automation, and GitHub workflow
infrastructure adapted from the Open Science Labs Incubator Python package
template used by `prisma-flow`.

## Installation

```bash
pip install osl-edu-math
```

## Symbolic equation solving

`edumath.solvers` provides SymPy-backed equation solving with structured
solution steps. The math is computed locally and can be used without any API
key:

```python
from edumath.core import parse_equation
from edumath.solvers import solve_equation_steps

equation = parse_equation("2(x - 3) + 4 = 10")
solution = solve_equation_steps(equation)
print(solution.answer)
print(solution.render_text())
```

Optional AI tutor explanations can be enabled through `edumath.settings`. The AI
text is added after SymPy/edumath has solved and checked the equation, so the
symbolic result remains the source of truth:

```python
from edumath.core import parse_equation
from edumath.settings import configure
from edumath.solvers import solve_equation_steps

configure(openai_api_key="YOUR_OPENAI_API_KEY")
equation = parse_equation("2(x - 3) + 4 = 10")
solution = solve_equation_steps(equation, explain=True)
print(solution.explanation)
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
