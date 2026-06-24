# PLAN: Improve Calculus Lessons with Step-by-Step Problem Solving

Target directory: `docs/lessons/calculus/`

This plan describes how to revise the Calculus study path so it teaches students
how to **solve calculus problems step by step**, not merely recognize formulas.
The current lessons already provide a solid overview, checkpoint games, and
SymPy appendices. The next improvement should make each lesson more like a
patient tutor: every major subtopic should include a clear workflow, a fully
worked walkthrough, guided practice, checkpoint exercises, and a topic-specific
guessing game.

The target learner is a student with weak preparation who needs to know what to
do first, why each step is legal, how to avoid common mistakes, and how to check
the result by hand and with software.

## Current calculus lesson files

Current source pages in `docs/lessons/calculus/`:

1. `index.qmd`
2. `limits.qmd`
3. `derivatives.qmd`
4. `derivative-rules.qmd`
5. `optimization.qmd`
6. `integrals.qmd`
7. `integration-techniques.qmd`
8. `applications.qmd`
9. `_includes/calculus-checkpoint.qmd`

The navigation already points to `lessons/calculus/index.qmd` first in
`docs/_quarto.yml`, and the lessons index already links to the calculus index.
No new navigation page is required.

Generated-looking Quarto artifacts are also present, such as `*.quarto_ipynb`
and `*.quarto_ipynb_1`. During implementation, verify whether these files are
tracked before removing or modifying them. Do not commit new scratch/session
artifacts.

## Core pedagogical goal

Each calculus lesson should train a reusable problem-solving habit:

> Understand the question, translate it into calculus language, choose a method,
> execute the method one step at a time, check the answer, and interpret the
> result in words and units.

Every worked problem should make this thinking visible. A student should be able
to copy the workflow for a similar exercise.

Use a recurring six-step template where appropriate:

1. **Read the problem.** Identify what is given and what is being asked.
2. **Classify the task.** Limit, derivative, rule selection, optimization,
   integral, technique choice, or application.
3. **Choose a strategy.** Explain why the method fits.
4. **Solve step by step.** Show algebra, calculus rules, substitutions, and
   simplification.
5. **Check.** Substitute, differentiate, estimate, inspect units, compare
   endpoints, or verify with SymPy.
6. **Interpret.** Write the answer in a sentence, including units when relevant.

## Global lesson standards to preserve

Each `.qmd` page should continue to follow repository lesson standards:

1. YAML front matter with `title`, `description`, and:

   ```yaml
   execute:
     echo: false
   ```

2. Short introduction explaining why the topic matters.
3. Learning goals written as student-facing action statements.
4. Concept sections with definitions, intuition, formulas, and common pitfalls.
5. Worked examples with step-by-step reasoning.
6. Practice exercises with answers or collapsed solutions.
7. A topic-relevant interactive checkpoint or guessing game before the Python
   appendix.
8. A final section named exactly:

   ```text
   Using this lesson with edumath and SymPy
   ```

The main explanatory flow should hide helper code unless the code itself is the
lesson objective. The final edumath/SymPy section should show visible code with
`#| echo: true`.

## Proposed page-level structure

Use this structure for each content lesson, adapting section names as needed:

1. **Why this topic matters**
2. **Learning goals**
3. **Vocabulary and notation**
4. **Problem-solving roadmap**
5. **Subtopic 1**
   - concept explanation;
   - guided walkthrough;
   - guided exercise with partial hints;
   - checkpoint exercise with collapsed answer.
6. **Subtopic 2**
   - same pattern.
7. **Common mistakes and how to repair them**
8. **Mixed practice set**
9. **Guessing game checkpoint**
10. **Using this lesson with edumath and SymPy**
11. **Further reading**

A lesson does not need every subtopic to be equally long. Use the most detailed
walkthroughs where students usually struggle.

## Guided exercise pattern

For guided exercises, use a consistent design:

```markdown
::: {.practice-box}

### Guided exercise

Problem: ...

1. What type of problem is this?
2. What method should you try first?
3. Complete the first algebra/calculus step.
4. Finish the calculation.
5. Check or interpret the answer. :::

::: {.callout-tip collapse="true"}

## Guided solution

Step-by-step solution with reasoning. :::
```

Use collapsed answers so students can try first without losing access to help.

## Checkpoint exercise pattern

Checkpoint exercises should be shorter than guided exercises. They test one
specific decision or skill:

- choose a method;
- identify a missing step;
- compute one derivative or limit;
- classify a graph behavior;
- check a candidate answer;
- interpret units.

Each checkpoint answer should explain **why** the answer is right, not only give
the final value.

## Guessing game plan

The existing shared include
`docs/lessons/calculus/_includes/calculus-checkpoint.qmd` already supports
topic-based browser-native checkpoints. Improve it only if needed, keeping it
dependency-free.

Potential improvements:

- add more question types for each lesson;
- add feedback that names the exact method used;
- add "What should you try first?" prompts;
- add step-order questions, such as "Which step comes next?";
- add mistake-diagnosis prompts, such as "What went wrong in this solution?";
- keep the game lightweight and static so it works in published HTML.

Potential topic keys already present:

- `limits`
- `derivatives`
- `derivative-rules`
- `optimization`
- `integrals`
- `integration-techniques`
- `calculus-applications`
- `calculus-cumulative-review`

## Online computation options

Use the final section of each lesson to show students how to check results with
`edumath`, SymPy, and sometimes NumPy. Do not add heavy JavaScript dependencies
unless there is a clear benefit.

Recommended approach:

- Keep primary examples in visible Python code blocks.
- Mention that the same SymPy code can run in Jupyter, Colab, or a PyScript /
  Pyodide page if SymPy is available.
- Use SymPy for exact limits, derivatives, integrals, equation solving,
  simplification, and critical points.
- Use `edumath.calculus` helpers for student-friendly wrappers and reusable
  exercises.
- Use plots in the main flow only when they clarify the concept.

Optional future online enhancements:

- PyScript cells for browser-based symbolic checking;
- Math.js for lightweight numeric previews;
- Plotly or SVG-only widgets for sliders and dynamic graphs.

Do not add these dependencies automatically in the content revision.

## Proposed `edumath.calculus` improvements

The current package already provides useful helpers for derivatives, integrals,
plots, validators, exercises, and quizzes. During implementation, add or propose
small reusable features only when they directly improve pedagogy.

Potential source additions:

### Step-by-step helpers

- `limit_factor_cancel_steps(expression, point)` for simple removable-hole
  examples.
- `tangent_line_steps(expression, point)` returning ordered explanation steps.
- `derivative_rule_trace(expression)` for beginner-friendly rule selection.
- `optimization_candidate_table(expression, domain=None)` returning candidates,
  values, and classification notes.
- `riemann_sum_table(expression, lower, upper, rectangles, method=...)` showing
  subintervals, sample points, heights, widths, and areas.
- `u_substitution_steps(expression, substitution)` for basic chain-rule reverse
  examples.

### Exercise builders

- `limit_factor_cancel_exercise(seed=...)`.
- `one_sided_limit_exercise(seed=...)`.
- `tangent_line_walkthrough_exercise(seed=...)`.
- `rule_selection_exercise(seed=...)`.
- `optimization_word_problem_exercise(seed=...)`.
- `riemann_sum_table_exercise(seed=...)`.
- `substitution_exercise(seed=...)`.
- `integration_by_parts_exercise(seed=...)`.
- `calculus_application_tool_choice_exercise(seed=...)` with units.

### Validators

- `validate_limit_answer(received, expression, point, direction=None)`.
- `validate_tangent_line(received, expression, point)`.
- `validate_critical_points(received, expression)`.
- `validate_antiderivative_with_constant(received, expected)`; current
  antiderivative validator already compares up to constant, but docs can make
  this behavior explicit.
- `validate_units_answer(received, expected_units)` for applied problems.

### Plotting and visual support

- mark secant points and tangent point labels more clearly;
- add an area-vs-signed-area plot helper;
- add endpoint and critical-point labels for optimization scenes;
- add a simple accumulation-from-rate plot.

Keep the public API small. Add tests for any package changes.

## Tests and validation for implementation

For docs-only edits:

```bash
poetry run pre-commit run --files <changed files>
mkdir -p .quarto-tmp .cache/deno
TMPDIR="$PWD/.quarto-tmp" \
XDG_CACHE_HOME="$PWD/.cache" \
DENO_DIR="$PWD/.cache/deno" \
quarto render <changed calculus .qmd files> --no-execute
```

For source changes:

```bash
poetry run pytest tests/test_calculus_helpers.py
poetry run pytest
```

After rendering, remove generated scratch files:

```bash
rm -rf .quarto-tmp .cache docs/.quarto/quarto-session-temp*
```

If Quarto creates new `*.quarto_ipynb*` files or `_freeze` updates, inspect
whether they are expected. Do not keep accidental scratch artifacts.

---

# Lesson-specific implementation plan

## 1. `index.qmd` — Calculus Study Path

### Goal

Turn the index into a detailed orientation page that teaches students how to
study calculus and how to decide which tool a problem needs.

### Add or expand sections

1. **What calculus is really about**

   - Change, accumulation, approximation, and modeling.
   - Relationship between algebra and calculus.
   - Why "nearby behavior" matters.

2. **The core problem-solving loop**

   - Read the question.
   - Classify the problem.
   - Choose a calculus tool.
   - Solve step by step.
   - Check.
   - Interpret.

3. **Calculus tool map**

   | If the problem asks for... | Think...              | Tool         |
   | -------------------------- | --------------------- | ------------ |
   | nearby value               | approach              | limit        |
   | instantaneous rate         | slope now             | derivative   |
   | best value                 | turn-around/candidate | optimization |
   | total change               | accumulation          | integral     |
   | reverse derivative         | antiderivative        | integration  |

4. **Readiness checklist with mini-solutions**

   - slope;
   - factoring;
   - function notation;
   - graph interpretation;
   - units;
   - basic exponentials/logarithms.

5. **How to use SymPy responsibly**

   - compute by hand first for small examples;
   - use SymPy to check;
   - compare exact and approximate answers;
   - do not paste output without interpretation.

6. **Diagnostic checkpoint**
   - keep cumulative checkpoint;
   - add questions about tool selection and study habits if needed.

### Suggested guided exercises

- Given 6 short problem statements, classify each as limit, derivative,
  optimization, integral, or algebra review.
- Given a solved problem with missing labels, identify which step is the
  strategy, calculation, check, and interpretation.

### SymPy section

Show how to load `edumath.calculus`, compute one derivative, one tangent line,
one integral, and one diagnostic quiz question.

---

## 2. `limits.qmd` — Limits

### Goal

Teach limits as a decision process: try direct substitution, inspect the result,
then choose a repair method if needed.

### Subtopics to expand

#### A. What a limit asks

Explain in words:

- input approaches a point;
- output approaches a value;
- function value at the point may differ;
- limits are about nearby behavior.

Add a table-based walkthrough:

1. Choose values near the target from the left and right.
2. Evaluate the function.
3. Look for the value the outputs approach.
4. State the limit cautiously.

#### B. Direct substitution

Workflow:

1. Substitute the approached value.
2. If the expression is defined and continuous, that value is the limit.
3. If the result is undefined or indeterminate, choose another method.

Worked example:

```text
lim as x -> 2 of x^2 + 3x
```

Show each substitution step.

#### C. Removable holes: factor and cancel

Workflow:

1. Substitute and notice `0/0`.
2. Factor numerator and denominator.
3. Cancel the common factor only for `x != a`.
4. Substitute into the simplified expression.
5. Explain that the original function may still be undefined at the point.

Worked examples:

- `(x^2 - 9)/(x - 3)` at `x = 3`.
- `(x^2 - 5x + 6)/(x - 2)` at `x = 2`.

#### D. Rationalizing radical expressions

Workflow:

1. Substitute and identify `0/0`.
2. Multiply by the conjugate.
3. Simplify using difference of squares.
4. Cancel and substitute.

Beginner example:

```text
lim as x -> 0 of (sqrt(x+1)-1)/x
```

#### E. One-sided limits

Workflow:

1. Compute or reason from the left.
2. Compute or reason from the right.
3. Compare the two values.
4. State whether the two-sided limit exists.

Include piecewise-function examples and vertical-asymptote examples.

#### F. Infinite limits and asymptotes

Explain:

- grows without bound vs equals infinity;
- left/right behavior may differ;
- vertical asymptotes.

Use `1/x` and `1/x^2` as contrasting examples.

### Common mistakes to emphasize

- Thinking `0/0` means the limit is 0.
- Forgetting to compare both sides for two-sided limits.
- Confusing `f(a)` with `lim_{x->a} f(x)`.
- Cancelling factors that are not common factors.
- Saying "equals infinity" without describing one-sided behavior.

### Guided exercises

- Direct substitution drill with explanation.
- Factor-and-cancel drill.
- Rationalization drill with a partially completed conjugate step.
- One-sided limit classification from a table or piecewise rule.

### Guessing game additions

- Guess the first method: substitute, factor, rationalize, or one-sided check.
- Guess whether `0/0` means hole, asymptote, or more work needed.
- Guess the limit after cancellation.

### SymPy section

Include visible examples for:

```python
sp.limit(expression, x, point)
sp.limit(expression, x, point, dir="+")
sp.limit(expression, x, point, dir="-")
```

Also show that SymPy output should be translated into a sentence.

---

## 3. `derivatives.qmd` — Derivatives

### Goal

Teach derivatives as a sequence from average rate to instantaneous rate to
usable tangent-line calculations.

### Subtopics to expand

#### A. Average rate of change

Workflow:

1. Identify interval endpoints.
2. Evaluate the function at both endpoints.
3. Compute change in output divided by change in input.
4. Interpret the slope with units.

Worked example:

```text
f(x)=x^2 from x=1 to x=3
```

#### B. From secant slope to tangent slope

Explain:

- secant line uses two points;
- tangent line is limiting position of secant lines;
- derivative is the limiting slope.

Use a table of smaller `h` values:

```text
[f(a+h)-f(a)]/h
```

#### C. Derivative definition

Use the limit definition carefully:

```text
f'(a) = lim_{h -> 0} [f(a+h)-f(a)]/h
```

Guided walkthrough for `f(x)=x^2` at `a=2`:

1. Substitute into the difference quotient.
2. Expand `(2+h)^2`.
3. Simplify numerator.
4. Cancel `h`.
5. Take the limit.
6. Interpret slope.

#### D. Derivative function

Show how the point-specific derivative becomes a function:

```text
f'(x) = lim_{h -> 0} [f(x+h)-f(x)]/h
```

Use `x^2` to get `2x`.

#### E. Tangent lines

Workflow:

1. Find the point `(a, f(a))`.
2. Find the slope `f'(a)`.
3. Use point-slope form.
4. Simplify only after the structure is correct.
5. Check that the line goes through the point.

Worked examples:

- tangent to `x^2` at `x=3`;
- tangent to `x^2 + 3x` at `x=1`.

#### F. Units and meaning

Examples:

- position/time -> velocity;
- cost/items -> marginal cost;
- temperature/time -> rate of warming/cooling.

#### G. Where derivatives fail

Explain with intuitive examples:

- corner: `abs(x)` at 0;
- cusp;
- vertical tangent;
- discontinuity.

### Common mistakes to emphasize

- Treating average rate as instantaneous rate.
- Forgetting to evaluate the derivative at the point for tangent slope.
- Writing tangent line slope but not the full line.
- Losing units.
- Assuming every continuous function is differentiable.

### Guided exercises

- Average rate with units.
- Difference quotient for a quadratic.
- Tangent line with point-slope form.
- Determine whether derivative is positive, negative, or zero from a graph.

### Guessing game additions

- Guess tangent slope from `f'(x)` and `x=a`.
- Guess whether graph is increasing/decreasing from derivative sign.
- Guess which graph feature prevents differentiability.

### SymPy section

Show:

```python
average_rate_of_change("x**2", 1, 3)
derivative("x**2")
tangent_line("x**2", 3)
finite_difference("x**2", 3)
```

Also show the raw SymPy version with `sp.diff`.

---

## 4. `derivative-rules.qmd` — Derivative Rules

### Goal

Teach derivative rules as a decision tree. Students should learn how to choose a
rule before computing.

### Subtopics to expand

#### A. Rule selection roadmap

Ask:

1. Is it a constant?
2. Is it a sum or difference?
3. Is it a constant multiple?
4. Is it a power of `x`?
5. Is it a product of changing factors?
6. Is it a quotient?
7. Is it a composition requiring the chain rule?
8. Are multiple rules needed?

#### B. Linearity rules

Walkthrough examples:

- derivative of a constant;
- derivative of `5x^3`;
- derivative of `4x^3 - 2x + 9`.

Explain why each term can be treated separately.

#### C. Power rule

Include integer, negative, and fractional powers:

- `x^5`;
- `1/x = x^-1`;
- `sqrt(x)=x^(1/2)`.

Give step-by-step exponent manipulation.

#### D. Product rule

Workflow:

1. Identify first factor `f` and second factor `g`.
2. Compute `f'` and `g'` separately.
3. Substitute into `f'g + fg'`.
4. Simplify if useful.

Worked example:

```text
(x^2+1)(x-3)
```

#### E. Quotient rule

Workflow:

1. Identify numerator and denominator.
2. Compute both derivatives.
3. Use `(low*dhigh - high*dlow)/low^2` or a clearly named formula.
4. Simplify carefully.
5. Check whether rewriting is easier.

Worked example:

```text
(x^2+1)/(x-1)
```

#### F. Chain rule

Workflow:

1. Identify the outside function.
2. Identify the inside function.
3. Differentiate the outside, leaving the inside unchanged.
4. Multiply by the derivative of the inside.

Examples:

- `(x^2+1)^3`;
- `sin(x^2)`;
- `e^(3x)`.

#### G. Combining rules

Use a rule tree for examples like:

```text
(x^2+1)^3 * e^x
sin(x^2)/(x+1)
```

The first rule is determined by the outermost operation.

### Common mistakes to emphasize

- Forgetting the inside derivative in the chain rule.
- Using product rule when a constant multiple rule is enough.
- Applying quotient rule sign in the wrong order.
- Simplifying too early and making algebra mistakes.
- Forgetting derivative of a constant is zero.

### Guided exercises

- Rule selection only: no computation.
- Complete missing derivative-rule step.
- Differentiate and then check by SymPy.
- Diagnose a wrong derivative.

### Guessing game additions

- Guess the first rule to apply.
- Guess the missing chain-rule factor.
- Guess whether a proposed derivative is correct.

### SymPy section

Show:

```python
derivative("(x**2 + 1)**3")
validate_derivative_equivalence("6*x*(x**2+1)**2", expected)
```

Also show `sp.diff` and `sp.simplify` for checking equivalent forms.

---

## 5. `optimization.qmd` — Optimization

### Goal

Teach optimization as an organized workflow with candidate generation,
classification, endpoint checking, and interpretation.

### Subtopics to expand

#### A. What optimization asks

Explain local vs absolute maximum/minimum using graphs and plain language.

#### B. Critical points

Workflow:

1. Find the domain.
2. Compute `f'(x)`.
3. Solve `f'(x)=0`.
4. Include points where `f'` is undefined but `f` is defined.
5. Keep only candidates in the domain.

Worked example:

```text
f(x)=x^2-6x+10
```

#### C. First derivative test

Workflow:

1. Put critical points on a number line.
2. Choose test points in each interval.
3. Evaluate sign of `f'`.
4. Translate signs into increasing/decreasing.
5. Classify max/min.

#### D. Second derivative test

Workflow:

1. Compute `f''(x)`.
2. Evaluate at a critical point.
3. Interpret positive as concave up/min, negative as concave down/max.
4. If zero, use another method.

#### E. Absolute extrema on closed intervals

Workflow:

1. Find interior critical points.
2. Add endpoints.
3. Evaluate original function at every candidate.
4. Compare values.
5. State absolute max/min with both input and output.

Worked example:

```text
f(x)=x^3-3x on [-2,2]
```

#### F. Applied optimization word problems

Use a consistent modeling template:

1. Draw or describe the situation.
2. Define variables and units.
3. Write the objective quantity.
4. Use constraints to get one-variable function.
5. State feasible domain.
6. Differentiate.
7. Find candidates.
8. Check endpoints and context.
9. Interpret in a sentence.

Begin with accessible examples:

- maximum area rectangle with fixed perimeter;
- maximum revenue for a quadratic revenue model;
- minimum cost with a simple quadratic.

### Common mistakes to emphasize

- Optimizing the wrong quantity.
- Forgetting the domain.
- Finding critical points but not checking endpoints.
- Comparing derivative values instead of original function values.
- Reporting only `x` when the problem asks for maximum value or dimensions.

### Guided exercises

- Candidate table completion.
- First derivative sign chart.
- Closed interval endpoint comparison.
- Word problem setup only.
- Full word problem solution.

### Guessing game additions

- Guess whether a critical point is max/min/neither from derivative signs.
- Guess which candidates must be checked.
- Guess what the objective function is in a word problem.

### SymPy section

Show:

```python
sp.diff(f, x)
sp.solve(sp.Eq(sp.diff(f, x), 0), x)
[(c, f.subs(x, c)) for c in candidates]
```

Use `edumath.calculus.critical_point_exercise` and any new candidate-table
helper if implemented.

---

## 6. `integrals.qmd` — Integrals

### Goal

Teach integrals as accumulation first, then area, then antiderivatives and the
Fundamental Theorem of Calculus.

### Subtopics to expand

#### A. Accumulation from small pieces

Explain:

- rate times small input change gives small accumulated amount;
- add many small pieces;
- integral is the limit of these sums.

Use a rate example before formal notation.

#### B. Signed area

Explain:

- area above the x-axis counts positive;
- area below counts negative;
- signed area differs from total geometric area.

Include a guided example with a piecewise or simple line crossing the x-axis.

#### C. Riemann sums

Workflow:

1. Split interval into `n` equal widths.
2. Compute `Delta x`.
3. Choose sample points: left, right, or midpoint.
4. Evaluate heights.
5. Multiply height by width.
6. Add rectangles.
7. Interpret approximation.

Worked example:

```text
Approximate integral of x^2 on [0,1] with 4 midpoint rectangles.
```

Show a table of intervals, midpoints, heights, and areas.

#### D. Indefinite integrals and antiderivatives

Workflow:

1. Ask what function has the given derivative.
2. Reverse a derivative rule.
3. Add `+ C` for indefinite integrals.
4. Check by differentiating.

Examples:

- `∫ 4x^3 dx`;
- `∫ (3x^2 - 2) dx`.

#### E. Definite integrals with the Fundamental Theorem

Workflow:

1. Find an antiderivative `F`.
2. Evaluate `F(b)` and `F(a)`.
3. Subtract `F(b)-F(a)`.
4. Interpret units.

Worked example:

```text
∫_0^3 2x dx
```

#### F. Units

Explain integral units as output units times input units.

Examples:

- velocity `(meters/second)` integrated over seconds gives meters;
- rate `(liters/minute)` integrated over minutes gives liters.

### Common mistakes to emphasize

- Forgetting `+ C` for indefinite integrals.
- Adding `+ C` to definite integrals.
- Confusing signed area and total area.
- Forgetting `Delta x` in a Riemann sum.
- Evaluating the derivative instead of the antiderivative at bounds.

### Guided exercises

- Complete a Riemann-sum table.
- Find and check an antiderivative.
- Use FTC on a simple polynomial.
- Interpret units from a rate problem.

### Guessing game additions

- Guess left/right/midpoint rectangle height.
- Guess whether an integral is signed area, total area, or displacement.
- Guess the missing `+ C` or bound evaluation step.

### SymPy section

Show:

```python
antiderivative("3*x**2")
definite_integral("2*x", 0, 3)
midpoint_riemann_sum("x**2", 0, 1, 4)
```

Also show `sp.integrate` and how to differentiate an antiderivative to check it.

---

## 7. `integration-techniques.qmd` — Integration Techniques

### Goal

Teach integration techniques as method selection. Students should ask: "What
derivative rule might this integral be reversing?"

### Subtopics to expand

#### A. Technique selection map

Use a decision table:

| Pattern                                                 | Try                                 |
| ------------------------------------------------------- | ----------------------------------- |
| algebra can simplify                                    | simplify first                      |
| composition with inside derivative nearby               | substitution                        |
| product where one factor simplifies when differentiated | integration by parts                |
| rational function                                       | algebra / partial fractions preview |
| exact form is hard or unnecessary                       | numerical approximation             |

#### B. Simplify first

Examples:

- expand before integrating;
- split fractions;
- rewrite radicals and reciprocals as powers.

Workflow:

1. Rewrite the integrand.
2. Integrate term by term.
3. Check by differentiating.

#### C. Substitution

Workflow:

1. Identify inside function `u=g(x)`.
2. Compute `du=g'(x) dx`.
3. Match the remaining factor.
4. Rewrite integral in `u`.
5. Integrate.
6. Substitute back.
7. Add `+ C` for indefinite integrals.
8. Check by differentiating.

Worked examples:

- `∫ 2x cos(x^2) dx`;
- `∫ 3x^2 sin(x^3) dx`.

#### D. Definite integrals with substitution

Show two options:

1. change bounds to `u` bounds;
2. substitute back into `x`, then evaluate old bounds.

Use a beginner-friendly example.

#### E. Integration by parts

Workflow:

1. Choose `u` and `dv`.
2. Compute `du` and `v`.
3. Substitute into `∫u dv = uv - ∫v du`.
4. Integrate the remaining integral.
5. Add `+ C` if indefinite.
6. Check by differentiating.

Examples:

- `∫ x e^x dx`;
- `∫ x cos(x) dx`.

Include a simple LIATE-style guideline but emphasize judgment over memorization.

#### F. Numerical approximation

Explain when numerical methods are appropriate:

- no elementary antiderivative;
- data table instead of formula;
- approximate answer is enough.

Use midpoint and trapezoid examples already available in `edumath`.

### Common mistakes to emphasize

- Choosing substitution without the inside derivative.
- Forgetting to substitute back.
- Forgetting changed bounds in definite substitution.
- Choosing `u` poorly for integration by parts.
- Forgetting the minus sign in integration by parts.
- Not checking antiderivatives by differentiating.

### Guided exercises

- Choose the technique only.
- Fill in missing `u`, `du`, and rewritten integral.
- Complete integration by parts table.
- Decide whether numerical approximation is appropriate.

### Guessing game additions

- Guess the best technique.
- Guess the correct `u`.
- Guess the missing `du` factor.
- Guess which factor should be `u` in integration by parts.

### SymPy section

Show:

```python
sp.integrate(2*x*sp.cos(x**2), x)
sp.integrate(x*sp.exp(x), x)
sp.diff(answer, x)
```

Add a note that SymPy may return equivalent forms or special functions, so the
student must still interpret the result.

---

## 8. `applications.qmd` — Calculus Applications

### Goal

Teach students to translate word problems into calculus decisions. The page
should become a modeling guide, not only a list of contexts.

### Subtopics to expand

#### A. Tool selection in applications

Use a decision workflow:

1. Does the question ask for a value nearby or at a point? Limit.
2. Does it ask for instantaneous rate, slope, or marginal change? Derivative.
3. Does it ask for total change, accumulated amount, or area? Integral.
4. Does it ask for largest/smallest/best? Optimization.
5. Does it involve a changing relationship between variables? Possibly related
   rates.

#### B. Motion

Explain:

- position `s(t)`;
- velocity `v(t)=s'(t)`;
- acceleration `a(t)=v'(t)=s''(t)`;
- displacement `∫v(t)dt`;
- total distance `∫|v(t)|dt`.

Guided walkthrough:

- Given `s(t)=t^2+3t`, find velocity at `t=2`.
- Given `v(t)=3t^2`, find displacement on `[0,2]`.

#### C. Marginal analysis

Workflow:

1. Identify cost/revenue/profit function.
2. Differentiate for marginal function.
3. Evaluate at production level.
4. Interpret units as dollars per item.

Worked example with `C(x)=100+5x+0.2x^2`.

#### D. Accumulation from rates

Workflow:

1. Identify rate and units.
2. Identify time/input interval.
3. Integrate rate over interval.
4. Interpret accumulated units.

Examples:

- water flow rate;
- infection rate or population change rate;
- energy/power relation.

#### E. Related rates introduction

Add a gentle introduction if appropriate:

1. Draw or describe related quantities.
2. Write an equation connecting variables.
3. Differentiate both sides with respect to time.
4. Substitute known values after differentiating.
5. Solve for requested rate.

Begin with a very simple area example:

```text
A = s^2, ds/dt known, find dA/dt
```

Keep this introductory; do not turn the page into a full related-rates unit
unless desired.

#### F. Optimization applications

Link back to optimization workflow and include one full word problem with
variables, units, domain, derivative, candidates, and interpretation.

#### G. Probability density preview

Keep a short preview:

- probability density integrates to probability;
- area under density over interval is probability;
- connect to future probability/statistics lessons.

### Common mistakes to emphasize

- Ignoring units.
- Using derivative for total or integral for instantaneous rate.
- Confusing velocity and speed.
- Confusing displacement and total distance.
- Substituting numbers too early in related rates.
- Reporting a number without context.

### Guided exercises

- Tool-choice classification from word prompts.
- Motion derivative/integral problem.
- Marginal cost interpretation.
- Accumulation from a rate.
- Simple related rates walkthrough.
- Optimization setup from a word problem.

### Guessing game additions

- Guess the calculus tool from problem wording.
- Guess units of an answer.
- Guess whether a motion question asks for velocity, acceleration, displacement,
  or distance.

### SymPy section

Show:

```python
derivative("100 + 5*x + 0.2*x**2")
definite_integral("3*t**2", 0, 2, variable="t")
sp.solve(...)
```

Add examples using `calculus_tool_question()` and any new application exercise
builders if implemented.

---

# Shared checkpoint include improvements

The current calculus checkpoint include already works. Implementation should
only modify it if lesson content needs richer questions.

Potential additions by topic:

## Limits

- first method to try;
- direct substitution result;
- factor-and-cancel answer;
- one-sided agreement;
- vertical asymptote behavior.

## Derivatives

- average vs instantaneous rate;
- tangent slope;
- derivative sign;
- differentiability obstacle;
- tangent-line missing step.

## Derivative rules

- first rule selection;
- power rule exponent;
- chain-rule inside derivative;
- product vs chain distinction;
- diagnose incorrect derivative.

## Optimization

- candidate source;
- derivative sign classification;
- endpoint checking;
- objective function identification;
- max/min interpretation.

## Integrals

- signed area vs total area;
- Riemann-sum rectangle height;
- antiderivative check;
- FTC evaluation;
- units of integral.

## Integration techniques

- technique selection;
- choose `u`;
- identify `du`;
- by-parts `u` and `dv`;
- numerical approximation reason.

## Applications

- tool choice;
- units;
- motion relationships;
- marginal meaning;
- accumulation from rates;
- related rates first step.

---

# Implementation phases

## Phase 1 — Content planning and preservation

1. Keep this `PLAN.md` as the implementation guide.
2. Inspect the current working tree carefully before editing because other files
   may already be modified.
3. Do not overwrite unrelated user changes.
4. Confirm whether generated `*.quarto_ipynb*` files are tracked or untracked
   before deleting them.

## Phase 2 — Shared pattern updates

1. Decide whether to update `_includes/calculus-checkpoint.qmd` now or after
   lesson rewrites.
2. If updating, keep the implementation browser-native and dependency-free.
3. Add question types that support step-order, method-choice, and mistake
   diagnosis.

## Phase 3 — Lesson rewrites

Recommended order:

1. `index.qmd`
2. `limits.qmd`
3. `derivatives.qmd`
4. `derivative-rules.qmd`
5. `optimization.qmd`
6. `integrals.qmd`
7. `integration-techniques.qmd`
8. `applications.qmd`

This order follows conceptual dependence: limits support derivatives;
derivatives support rules and optimization; integrals support techniques and
applications.

## Phase 4 — Optional `edumath.calculus` additions

1. Add only helpers that are reused in lessons or tests.
2. Keep public API small and documented.
3. Add tests for every behavior change.
4. Update `src/edumath/calculus/__init__.py` exports deliberately.

## Phase 5 — Validation and cleanup

1. Run scoped pre-commit on changed files.
2. Run tests if source code changed.
3. Render changed calculus pages with `--no-execute` and local temp/cache env.
4. Clean Quarto temp/cache/session artifacts.
5. Run `git diff --check`.
6. Summarize changed lesson files and validation commands.
