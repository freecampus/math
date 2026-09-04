# FreeCampus Math

![CI](https://img.shields.io/github/actions/workflow/status/freecampus/math/ci.yml?logo=github&label=CI)
[![Python Versions](https://img.shields.io/pypi/pyversions/freecampus-math)](https://pypi.org/project/freecampus-math/)
[![Package Version](https://img.shields.io/pypi/v/freecampus-math?color=blue)](https://pypi.org/project/freecampus-math/)
![License](https://img.shields.io/pypi/l/freecampus-math?color=blue)

FreeCampus Math is an open, institution-independent catalog of rigorous courses
for advanced quantitative and computational study. Learners can enter the
subject they need directly: algebra, proof, linear algebra, calculus,
differential equations, probability, statistics, or mathematical computing.

The learning standard is proof-aware and computationally reproducible:

- state definitions, domains, hypotheses, and limitations;
- show complete manual reasoning rather than answer-only procedures;
- distinguish exact, approximate, simulated, and estimated results;
- use computation to verify and extend mathematics, not replace it;
- interpret results and audit edge cases;
- retrieve and synthesize ideas through checkpoints and cumulative practice.

QMD files are the canonical lessons. The website and executable Colab notebooks
are generated formats. Browser-local completion needs no account and stores no
raw answers or behavioral history.

## Start learning

Visit <https://freecampus.github.io/math/> and choose a course by topic, study
goal, or recommended background. Each course publishes its own outcomes,
prerequisites, readiness guidance, and current status.

## Install the lesson-support package

The PyPI distribution is `freecampus-math`; the import is `fcmath`.

```bash
python -m pip install freecampus-math
```

```python
from fcmath import ValidationPolicy, check_answer, parse_equation
from fcmath.solvers import solve_equation_steps

solution = solve_equation_steps(parse_equation("2(x - 3) + 4 = 10"))
print(solution.answer)

policy = ValidationPolicy(mode="symbolic-equivalence", variables=("x",))
assert check_answer("(x + 1)^2", "x^2 + 2*x + 1", policy).correct
```

The public API is deliberately small: safe expression handling, mathematical
answer validation, shared quizzes, proof-audit helpers, plotting primitives, and
selected solvers. Unreviewed subject helpers are experimental.

## Development

```bash
conda env create -f conda/dev.yaml
conda activate fcmath
poetry config virtualenvs.create false
poetry install --extras "dev"
makim all.ci
```

Important focused commands:

```bash
makim curriculum.validate
makim curriculum.generate
makim notebooks.build
makim tests.unit
makim docs.build
```

See `AGENTS.md` and `CONTRIBUTING.md` for lesson, accessibility, and catalog
requirements.
