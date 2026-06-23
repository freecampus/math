# PLAN: Calculus Lessons

Target directory: `docs/lessons/calculus/`

This plan describes how to rebuild the current Calculus lesson sequence into a
complete, beginner-friendly preparation module. The current pages exist, but
they are short starter lessons. The goal is to turn them into self-contained
study material for learners who may know algebra but need careful explanations,
visual intuition, worked examples, practice, interactive checkpoints, and
visible `edumath`/SymPy appendices.

## Current lesson files

Current pages in `docs/lessons/calculus/`:

1. `limits.qmd`
2. `derivatives.qmd`
3. `derivative-rules.qmd`
4. `optimization.qmd`
5. `integrals.qmd`
6. `integration-techniques.qmd`
7. `applications.qmd`

Recommended addition:

8. `index.qmd` — Calculus study path overview and diagnostic checklist

The sidebar currently lists the seven lesson pages directly. Add the index page
at the beginning of the Calculus section when implemented.

## Overall pedagogical goals

The Calculus module should help students move from algebraic manipulation to
reasoning about change and accumulation.

By the end of the path, a student should be able to say:

> Calculus studies how quantities change and accumulate. Limits describe nearby
> behavior, derivatives measure instantaneous change, and integrals add up small
> pieces. I can use formulas, graphs, tables, units, and computation together to
> solve and check problems.

## Global lesson standards

Every calculus lesson should follow the project lesson standards:

1. YAML front matter with a clear `title`, `description`, and usually:

   ```yaml
   execute:
     echo: false
   ```

2. A short introduction explaining why the topic matters.
3. Learning objectives.
4. Concept sections with definitions, intuition, formulas, and common pitfalls.
5. Worked examples with step-by-step reasoning.
6. Practice exercises with answers or collapsed solutions.
7. A topic-relevant interactive checkpoint or guessing game before the Python
   appendix.
8. A final section named `Using this lesson with edumath and SymPy` with visible
   code examples using `#| echo: true`.

Use hidden code for plots and setup in the main explanatory flow. Show visible
code only when code is itself part of the learning objective or in the final
appendix.

## Shared calculus interaction plan

Create or update a reusable static checkpoint include under something like:

```text
docs/lessons/calculus/_includes/calculus-checkpoint.qmd
```

The include should be browser-native JavaScript, similar in spirit to the
Algebra guessing game, so published HTML remains interactive without a live
Python kernel.

Potential topic keys:

- `limits`
- `derivatives`
- `derivative-rules`
- `optimization`
- `integrals`
- `integration-techniques`
- `calculus-applications`
- `calculus-cumulative-review`

Question types should be topic-specific, not generic decoration. Examples:

- guess a limit from a table or graph;
- choose the derivative meaning from a context;
- select the rule needed for a derivative;
- classify critical points;
- estimate area from rectangles;
- choose substitution, parts, or numeric approximation;
- decide whether a context asks for a derivative or an integral.

## Shared `edumath` support plan

Current calculus helpers:

- `src/edumath/calculus/derivatives.py`
  - `derivative`
  - `tangent_line`
  - `finite_difference`
- `src/edumath/calculus/integrals.py`
  - `antiderivative`
  - `definite_integral`
  - `midpoint_riemann_sum`

Current empty or placeholder modules:

- `src/edumath/calculus/concepts.py`
- `src/edumath/calculus/exercises.py`
- `src/edumath/calculus/plots.py`
- `src/edumath/calculus/quizzes.py`
- `src/edumath/calculus/validators.py`
- `src/edumath/calculus/__init__.py`

Proposed reusable helpers are listed per lesson below. Keep the public API small
and add tests for each new helper.

## Proposed Calculus study path metadata

Add lesson metadata in `src/edumath/calculus/concepts.py`:

- `CALCULUS_PATH`
- `LIMITS`
- `DERIVATIVES`
- `DERIVATIVE_RULES`
- `OPTIMIZATION`
- `INTEGRALS`
- `INTEGRATION_TECHNIQUES`
- `CALCULUS_APPLICATIONS`

Suggested `CALCULUS_PATH.slugs()`:

```python
[
    "limits",
    "derivatives",
    "derivative-rules",
    "optimization",
    "integrals",
    "integration-techniques",
    "applications",
]
```

## Lesson 0: Calculus Study Path (`index.qmd`)

### Purpose

Create a welcoming overview page for the calculus sequence.

### Learning goals

Students should understand:

- what calculus studies;
- how limits, derivatives, and integrals fit together;
- what algebra skills should be reviewed first;
- how to use the module and diagnostic checklist.

### Suggested sections

1. **What is calculus?**
   - Change and accumulation.
   - Local behavior versus total behavior.
2. **Prerequisites**
   - Algebra, functions, graphs, trigonometry basics, exponentials/logs.
3. **Recommended sequence**
   - Brief description of each lesson.
4. **Diagnostic checklist**
   - Function evaluation, slope, graph reading, factoring, exponentials/logs,
     area of rectangles, units.
5. **How to study calculus**
   - Predict from graph, compute by hand, check with SymPy, explain in words.
6. **Using this path with edumath and SymPy**
   - Visible code showing derivative, tangent line, definite integral, and
     Riemann sum helpers.

### Interactive checkpoint

A diagnostic guessing game that asks students whether a prompt is about:

- a limit;
- a derivative;
- an integral;
- an optimization problem;
- an algebra prerequisite.

## Lesson 1: Limits (`limits.qmd`)

### Current state

The page defines limits briefly and includes three short practice questions. It
needs tables, one-sided limits, graphical intuition, algebraic simplification,
common pitfalls, and a final SymPy appendix.

### Pedagogical promise

By the end, a student should be able to say:

> A limit describes what function values approach as inputs get close to a
> point. The function value at the point may be different, missing, or
> undefined.

### Learning objectives

Students should be able to:

1. explain a limit in words;
2. estimate limits from tables and graphs;
3. distinguish `f(a)` from `lim f(x)` as `x -> a`;
4. recognize left-hand and right-hand limits;
5. identify when a two-sided limit does not exist;
6. use algebraic simplification to evaluate removable-hole limits;
7. understand infinite limits and vertical asymptotes informally;
8. use SymPy to compute and check simple limits.

### Detailed structure

1. **Motivation**
   - Average speed approaching instantaneous speed.
   - Zooming in on a graph near a point.
2. **What a limit asks**
   - Plain-language definition.
   - Notation: `lim_{x -> a} f(x) = L`.
3. **Tables near a point**
   - Inputs approaching from the left and right.
   - Example: `(x^2 - 1)/(x - 1)` near `x = 1`.
4. **Graph intuition**
   - Holes, jumps, and vertical asymptotes.
   - The value at the point can differ from the limit.
5. **One-sided limits**
   - Left-hand and right-hand notation.
   - Two-sided limit exists only if both agree.
6. **Algebraic limit techniques**
   - Direct substitution when continuous.
   - Factor and cancel for removable holes.
   - Rationalize simple radical expressions.
7. **Limits that do not exist**
   - Left/right disagreement.
   - Infinite behavior.
   - Oscillation as a preview only.
8. **Common mistakes**
   - Substituting into a formula and stopping when denominator is zero.
   - Confusing undefined function value with no limit.
   - Ignoring one-sided behavior.
9. **Practice with solutions**
   - Direct substitution limits.
   - Hole limits.
   - One-sided table questions.
   - Graph interpretation questions.
10. **Guessing game checkpoint**
11. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Guess the limit from a table.
- Decide whether a two-sided limit exists.
- Match a graph feature with removable, jump, infinite, or continuous behavior.

### Suggested edumath helpers

- `limit_table(expression, point, offsets, variable="x")`
- `limit_scene(expression, point, ...)`
- `one_sided_limit_question(...)`
- `validate_limit_estimate(...)`

### SymPy appendix examples

```python
#| echo: true
import sympy as sp
x = sp.symbols("x")
sp.limit((x**2 - 1)/(x - 1), x, 1)
```

```python
#| echo: true
sp.limit(1/x, x, 0, dir="+")
sp.limit(1/x, x, 0, dir="-")
```

## Lesson 2: Derivatives (`derivatives.qmd`)

### Current state

The page explains derivative as slope/rate and shows existing helpers. It needs
limit definition, secant-to-tangent intuition, units, examples, and more
practice.

### Pedagogical promise

By the end, a student should be able to say:

> A derivative measures instantaneous rate of change. It is the limiting slope
> of secant lines and the slope of the tangent line at a point.

### Learning objectives

Students should be able to:

1. interpret average rate of change;
2. explain secant slopes approaching tangent slope;
3. connect derivative notation to rate of change;
4. estimate derivatives from graphs and tables;
5. compute simple derivatives from power rules or SymPy checks;
6. write tangent line equations;
7. interpret derivative units in context;
8. identify where derivatives may fail to exist.

### Detailed structure

1. **Motivation**
   - Speedometer vs average speed.
   - Marginal cost and slope.
2. **Average rate of change**
   - Secant slope formula.
3. **Instantaneous rate of change**
   - Shrinking interval idea.
   - Informal derivative definition.
4. **Derivative notation**
   - `f'(x)`, `dy/dx`, `d/dx[f(x)]`.
5. **Tangent lines**
   - Point-slope form.
   - Worked example for `x^2` at `x = 2`.
6. **Units**
   - If `s(t)` is meters and `t` is seconds, `s'(t)` is meters/second.
7. **Where derivatives fail**
   - Corners, cusps, vertical tangents, discontinuities.
8. **Common mistakes**
   - Treating derivative as a fraction without context.
   - Forgetting derivative is a function and also can be evaluated.
   - Thinking zero derivative always means maximum.
9. **Practice with solutions**
10. **Guessing game checkpoint**
11. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Guess the tangent slope from a graph.
- Match a context to derivative units.
- Choose whether derivative is positive, negative, or zero at a point.

### Suggested edumath helpers

- `average_rate_of_change(expression, a, b, variable="x")`
- `secant_slope_table(expression, point, steps, variable="x")`
- `tangent_line_scene(expression, point, ...)`
- `derivative_sign_question(...)`

### SymPy appendix examples

```python
#| echo: true
from edumath.calculus.derivatives import derivative, tangent_line, finite_difference

derivative("x**2 + 3*x")
tangent_line("x**2", 2)
finite_difference("x**2", 2)
```

## Lesson 3: Derivative Rules (`derivative-rules.qmd`)

### Current state

The page lists the power rule and mentions product, quotient, and chain rules.
It needs conceptual rule selection, detailed worked examples, practice, and
common mistakes.

### Pedagogical promise

By the end, a student should be able to say:

> Derivative rules are patterns that let me compute rates without starting from
> the limit definition every time. The hard part is often choosing the correct
> rule and applying it in the right order.

### Learning objectives

Students should be able to:

1. use constant, constant-multiple, sum, and difference rules;
2. use the power rule;
3. differentiate exponentials and logarithms at an introductory level;
4. apply product and quotient rules;
5. apply the chain rule;
6. combine rules in multi-step examples;
7. check derivatives with SymPy;
8. identify common rule-selection errors.

### Detailed structure

1. **Why rules matter**
2. **Linearity rules**
   - Constants, multiples, sums, differences.
3. **Power rule**
   - Positive, zero, negative, and fractional powers if appropriate.
4. **Basic exponential/log derivatives**
   - `d/dx e^x = e^x`.
   - `d/dx ln(x) = 1/x` for `x > 0`.
5. **Product rule**
   - Formula and worked examples.
6. **Quotient rule**
   - Formula and when to rewrite instead.
7. **Chain rule**
   - Outside/inside language.
8. **Combining rules**
   - Example: `(x^2 + 1)^3 * exp(x)`.
9. **Common mistakes**
   - Distributing derivatives over products.
   - Forgetting the inner derivative.
   - Sign errors in quotient rule.
10. **Practice with solutions**
11. **Guessing game checkpoint**
12. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Given an expression, choose the first derivative rule to apply.
- Predict the missing factor in a chain-rule derivative.
- Match an incorrect derivative with its mistake.

### Suggested edumath helpers

- `derivative_rule_hint(expression, variable="x")`
- `derivative_rule_question(seed=None)`
- `check_derivative_answer(received, expected)`
- `derivative_steps_basic(expression, variable="x")` as a conservative helper
  for simple patterns only.

### SymPy appendix examples

```python
#| echo: true
from edumath.calculus.derivatives import derivative

derivative("(x**2 + 1)**3")
derivative("(x**2 + 1) * (x - 3)")
```

## Lesson 4: Optimization (`optimization.qmd`)

### Current state

The page introduces critical points and a parabola. It needs a full workflow,
first/second derivative tests, endpoints, word problems, and interpretation.

### Pedagogical promise

By the end, a student should be able to say:

> Optimization uses derivatives to find candidate best values, but the final
> answer comes from checking candidates, endpoints, and the problem context.

### Learning objectives

Students should be able to:

1. define local and absolute maxima/minima;
2. find critical points where `f'(x) = 0` or `f'` is undefined;
3. use sign charts or first derivative test;
4. use second derivative test for simple cases;
5. check endpoints on closed intervals;
6. solve basic applied optimization problems;
7. interpret units and feasibility constraints;
8. use SymPy to compute candidates and compare values.

### Detailed structure

1. **Motivation**
   - Maximum profit, minimum cost, shortest distance.
2. **What is an optimum?**
   - Local vs absolute.
3. **Critical points**
4. **First derivative test**
   - Increasing/decreasing sign changes.
5. **Second derivative test**
   - Concavity at critical points.
6. **Closed intervals and endpoints**
   - Candidate list method.
7. **Worked example: quadratic minimum**
8. **Worked example: rectangle/area or revenue model**
9. **Common mistakes**
   - Ignoring endpoints.
   - Reporting `x` but not the optimized value.
   - Accepting infeasible negative dimensions.
10. **Practice with solutions**
11. **Guessing game checkpoint**
12. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Classify a critical point from derivative signs.
- Choose the feasible domain from a word problem.
- Pick the absolute maximum from a candidate table.

### Suggested edumath helpers

- `critical_points(expression, variable="x")`
- `candidate_values(expression, candidates, variable="x")`
- `classify_critical_point(expression, point, variable="x")`
- `optimization_candidate_table(expression, interval, variable="x")`

### SymPy appendix examples

```python
#| echo: true
import sympy as sp
x = sp.symbols("x")
f = x**2 - 6*x + 10
critical = sp.solve(sp.Eq(sp.diff(f, x), 0), x)
[(c, f.subs(x, c)) for c in critical]
```

## Lesson 5: Integrals (`integrals.qmd`)

### Current state

The page introduces accumulation and area and shows antiderivative and definite
integral helpers. It needs Riemann sums, signed area, Fundamental Theorem of
Calculus, units, and more practice.

### Pedagogical promise

By the end, a student should be able to say:

> A definite integral accumulates small contributions over an interval. It can
> represent signed area, total change, distance from velocity, probability from
> a density, and many other totals.

### Learning objectives

Students should be able to:

1. interpret definite integrals as accumulation;
2. distinguish antiderivatives from definite integrals;
3. approximate area with rectangles;
4. understand signed area;
5. use the Fundamental Theorem of Calculus in simple examples;
6. compute basic antiderivatives;
7. interpret integral units;
8. use SymPy and `edumath` to compute and approximate integrals.

### Detailed structure

1. **Motivation**
   - Total distance from velocity.
   - Total cost from marginal cost.
2. **Area as accumulation**
3. **Riemann sums**
   - Left, right, midpoint rectangles.
4. **Definite integral notation**
5. **Antiderivatives and `+ C`**
6. **Fundamental Theorem of Calculus**
   - If `F' = f`, then integral from `a` to `b` is `F(b)-F(a)`.
7. **Signed area and total area**
8. **Units**
9. **Common mistakes**
   - Forgetting `+ C` for indefinite integrals.
   - Confusing signed area with geometric area.
   - Losing bounds when using substitution later.
10. **Practice with solutions**
11. **Guessing game checkpoint**
12. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Estimate area from a rectangle diagram.
- Decide whether an integral is positive, negative, or zero from a graph.
- Match a context with integral units.

### Suggested edumath helpers

- `left_riemann_sum`
- `right_riemann_sum`
- `trapezoid_rule`
- `riemann_sum_scene`
- `accumulation_table`
- `integral_units_prompt`

Current `midpoint_riemann_sum` exists and should be kept.

### SymPy appendix examples

```python
#| echo: true
from edumath.calculus.integrals import antiderivative, definite_integral, midpoint_riemann_sum

antiderivative("3*x**2")
definite_integral("2*x", 0, 3)
midpoint_riemann_sum("x**2", 0, 1, 10)
```

## Lesson 6: Integration Techniques (`integration-techniques.qmd`)

### Current state

The page mentions substitution, parts, and numerical approximation. It needs a
method-selection focus, detailed worked examples, and a clear boundary around
what beginners should master.

### Pedagogical promise

By the end, a student should be able to say:

> Integration techniques are pattern-recognition tools. I choose a technique by
> looking for composition, products, algebraic simplification, or when symbolic
> methods are not practical.

### Learning objectives

Students should be able to:

1. recognize when substitution is useful;
2. carry out simple `u`-substitution;
3. recognize when integration by parts is useful;
4. apply integration by parts in simple examples;
5. use algebraic simplification before integrating;
6. approximate integrals numerically when exact integration is hard;
7. check results by differentiating antiderivatives;
8. use SymPy responsibly for verification.

### Detailed structure

1. **Why integration is harder than differentiation**
2. **Technique-selection map**
   - Simplify first.
   - Substitution for chain-rule patterns.
   - Parts for products where one factor simplifies when differentiated.
   - Numeric approximation when symbolic methods are not needed or not feasible.
3. **Substitution**
   - `∫ 2x cos(x^2) dx`.
   - Definite integral bounds transformation.
4. **Integration by parts**
   - Formula and intuition from product rule.
   - `∫ x e^x dx`.
5. **Algebraic simplification**
   - Expand, split fractions, rewrite powers.
6. **Numerical approximation**
   - Midpoint, trapezoid, and error intuition.
7. **Checking antiderivatives by differentiating**
8. **Common mistakes**
   - Forgetting `dx` transformation.
   - Not changing bounds in definite substitution.
   - Choosing parts when substitution is simpler.
9. **Practice with solutions**
10. **Guessing game checkpoint**
11. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Choose the best technique for a given integral.
- Identify a good `u` substitution.
- Choose which factor should be `u` in integration by parts.

### Suggested edumath helpers

- `integration_technique_hint(expression, variable="x")`
- `substitution_candidate_question(seed=None)`
- `parts_choice_question(seed=None)`
- `trapezoid_rule` if not already added with integrals.

### SymPy appendix examples

```python
#| echo: true
import sympy as sp
x = sp.symbols("x")
sp.integrate(2*x*sp.cos(x**2), x)
sp.integrate(x*sp.exp(x), x)
```

## Lesson 7: Calculus Applications (`applications.qmd`)

### Current state

The page contrasts derivatives and integrals. It needs full application
categories, units, modeling workflow, worked examples, and cumulative practice.

### Pedagogical promise

By the end, a student should be able to say:

> I can decide whether a real problem asks for local change, accumulated change,
> or an optimum, then translate the context into calculus and interpret the
> answer with units.

### Learning objectives

Students should be able to:

1. choose derivatives for instantaneous rate and marginal analysis;
2. choose integrals for accumulation;
3. choose optimization workflows for best-value questions;
4. use units to verify setup;
5. interpret position, velocity, and acceleration;
6. connect total change to integrating a rate;
7. set up simple marginal cost/revenue/profit problems;
8. use SymPy and `edumath` helpers for checking.

### Detailed structure

1. **Calculus decision guide**
   - Derivative: local rate.
   - Integral: accumulated total.
   - Optimization: best value.
2. **Motion**
   - Position, velocity, acceleration.
   - Total distance vs displacement.
3. **Marginal analysis**
   - Cost, revenue, profit.
4. **Accumulation from rates**
   - Water filling tank, total emissions, distance from velocity.
5. **Optimization applications**
   - Revenue/profit, area/volume, constrained resources.
6. **Probability density preview**
   - Integral as probability over interval.
7. **Modeling workflow**
   - Variables, units, assumptions, solve, interpret.
8. **Common mistakes**
   - Using derivative when a total is requested.
   - Ignoring units.
   - Confusing displacement and total distance.
   - Reporting candidate point without checking endpoints/context.
9. **Practice with solutions**
10. **Cumulative guessing game checkpoint**
11. **Using this lesson with edumath and SymPy**

### Interactive checkpoint ideas

- Choose derivative/integral/optimization from a context.
- Match units to calculus operation.
- Classify motion statements.

### Suggested edumath helpers

- `calculus_tool_classifier(prompt_or_tags)` as a data-backed quiz helper, not
  an AI classifier.
- `motion_summary(position_expression, variable="t")`
- `marginal_to_total_change(rate_expression, lower, upper, variable="x")`
- `application_question(seed=None)`

### SymPy appendix examples

```python
#| echo: true
from edumath.calculus.derivatives import derivative
from edumath.calculus.integrals import definite_integral

derivative("100 + 5*x + 0.2*x**2")
definite_integral("3*t**2", 0, 2, variable="t")
```

## Source package implementation plan

### `src/edumath/calculus/concepts.py`

Implement path metadata for the Calculus lessons.

### `src/edumath/calculus/plots.py`

Add reusable plotting scene builders:

- `secant_tangent_scene`
- `derivative_sign_scene`
- `riemann_sum_scene`
- `accumulation_scene`
- `optimization_scene`

Use existing `edumath.core` plot primitives when possible.

### `src/edumath/calculus/exercises.py`

Add deterministic exercise builders:

- `limit_estimate_exercise`
- `tangent_line_exercise`
- `derivative_rule_exercise`
- `critical_point_exercise`
- `riemann_sum_exercise`
- `tool_choice_exercise`

### `src/edumath/calculus/quizzes.py`

Add question builders compatible with `edumath.core.Question` and `QuizSession`:

- `derivative_question`
- `antiderivative_question`
- `definite_integral_question`
- `optimization_question`
- `calculus_tool_question`

### `src/edumath/calculus/validators.py`

Add reusable checkers:

- `validate_derivative_equivalence`
- `validate_antiderivative_equivalence`
- `validate_limit_value`
- `validate_numeric_approximation`
- `validate_critical_point`

### `src/edumath/calculus/__init__.py`

Export only the stable, tested public API. Avoid exporting every internal
helper.

## Tests to add

Create or extend `tests/test_calculus_helpers.py`.

Minimum tests:

1. `CALCULUS_PATH.slugs()` returns the expected order.
2. Existing derivative helpers still pass.
3. Existing integral helpers still pass.
4. New Riemann/trapezoid helpers approximate known integrals.
5. Tangent/secant plot scenes render without image comparison.
6. Exercise builders accept their expected answers.
7. Validators accept equivalent symbolic answers and reject incorrect answers.
8. Quiz question builders produce internally consistent answers.

## Documentation implementation phases

### Phase 1: structure and metadata

- Add `docs/lessons/calculus/index.qmd`.
- Add `execute: echo: false` to all calculus lesson front matter.
- Add `CALCULUS_PATH` metadata.
- Update sidebar with the new index page.

### Phase 2: conceptual lesson expansion

- Expand `limits.qmd`.
- Expand `derivatives.qmd`.
- Expand `derivative-rules.qmd`.

### Phase 3: applications of derivatives and integrals

- Expand `optimization.qmd`.
- Expand `integrals.qmd`.
- Expand `integration-techniques.qmd`.

### Phase 4: cumulative applications

- Expand `applications.qmd`.
- Add a cumulative checkpoint.
- Ensure cross-links among calculus pages.

### Phase 5: package support and tests

- Add helpers only when lesson content actually uses them.
- Add tests in the same change as helper additions.
- Keep README/API docs in sync if public API changes.

## Quarto and validation commands

For a single docs-only lesson change:

```bash
poetry run pre-commit run --files docs/lessons/calculus/<lesson>.qmd
quarto render docs/lessons/calculus/<lesson>.qmd --no-execute
```

For multiple calculus pages:

```bash
poetry run pre-commit run --files docs/lessons/calculus/*.qmd
quarto render docs/lessons/calculus/limits.qmd docs/lessons/calculus/derivatives.qmd --no-execute
```

If Quarto needs writable temp/cache directories in this environment, use local
scratch paths and remove them before finishing:

```bash
mkdir -p .quarto-tmp .cache
TMPDIR="$PWD/.quarto-tmp" XDG_CACHE_HOME="$PWD/.cache" DENO_DIR="$PWD/.cache/deno" \
  quarto render docs/lessons/calculus/<lesson>.qmd --no-execute
```

Then remove `.quarto-tmp` and `.cache`.

For package changes:

```bash
poetry run pre-commit run --files src/edumath/calculus/*.py tests/test_calculus_helpers.py
poetry run pytest tests/test_calculus_helpers.py
```

For broad confidence:

```bash
makim docs.build
makim all.ci
```

## Open questions before implementation

1. Should calculus get a dedicated static checkpoint include, or should the
   Algebra guessing-game include be generalized across lesson branches?
   Recommendation: create a small calculus-specific include first, then refactor
   shared patterns later if duplication becomes significant.
2. Should trigonometric derivatives and integrals be included now?
   Recommendation: mention only basic sine/cosine examples unless the
   Trigonometry path is expanded first.
3. Should epsilon-delta rigor be covered in Calculus or Analysis?
   Recommendation: Calculus should give intuition and simple limit laws;
   rigorous epsilon-delta work belongs in a future Analysis path.
4. Should PyScript be embedded in every lesson? Recommendation: no. Use visible
   SymPy code blocks in the appendix and plan a single optional sandbox page
   later if needed.
5. Should generated build artifacts be committed? Recommendation: no. Do not
   commit `build/`, Quarto session temp folders, or local cache directories.
