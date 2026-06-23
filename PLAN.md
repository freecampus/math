# PLAN: Differential Equations Lessons

Target directory: `docs/lessons/differential-equations/`

This plan describes how to turn the Differential Equations lesson sequence into
a complete, beginner-friendly preparation module. The current pages are short
starter lessons. The goal is to write self-contained study material for learners
who know basic algebra and calculus but may be seeing differential equations for
the first time.

The lessons should emphasize meaning before technique: a differential equation
is not just an equation to solve, but a rule that describes how a quantity
changes. Students should learn to interpret equations verbally, graphically,
numerically, and symbolically.

## Current lesson files

Current pages in `docs/lessons/differential-equations/`:

1. `first-order-equations.qmd`
2. `separable-equations.qmd`
3. `linear-equations.qmd`
4. `slope-fields.qmd`
5. `systems.qmd`

Also present:

- `slope-fields.quarto_ipynb` — likely a generated or old notebook-style file.
  Before implementing content, inspect whether it is tracked and still needed.
  If it is generated or obsolete, remove it from the lesson workflow. The site
  should primarily use `.qmd` pages.

Recommended additions:

1. `index.qmd` — Differential Equations study path overview and readiness
   checklist.
2. Optional later page: `modeling-review.qmd` or `applications.qmd` if the
   course needs a standalone applications lesson after the five core pages.

Update `docs/_quarto.yml` so the Differential Equations sidebar starts with the
new index page if `index.qmd` is added.

## Overall pedagogical goals

The Differential Equations module should help students move from calculus facts
to dynamic reasoning.

By the end of the path, a student should be able to say:

> A differential equation describes how a quantity changes. A solution is a
> function whose derivative follows that change rule. I can understand a
> differential equation from its formula, slope field, numerical approximation,
> symbolic solution, equilibrium behavior, and units.

Students should learn to answer these questions repeatedly:

- What is changing?
- What variable measures the input, usually time or position?
- What does the derivative mean in context?
- Does the equation give a growth rule, decay rule, forcing term, or
  interaction?
- Is the solution a single function or a family of functions?
- What initial condition selects one solution?
- Can the equation be solved exactly, approximated numerically, or studied
  qualitatively?
- What does the result mean in plain language?

## Prerequisites to reinforce throughout

The lessons should quietly review prerequisite skills instead of assuming
students remember everything perfectly:

- interpreting derivatives as rates of change;
- basic antiderivatives;
- separation of variables and integration constants;
- exponentials and logarithms;
- algebraic rearrangement;
- function notation;
- reading graphs;
- solving equations such as `Ce^{kt} = A`;
- interpreting units;
- basic matrix-vector multiplication for systems.

Whenever a prerequisite appears, include a short reminder box. For example, in a
separable equation lesson, remind students that `\int 1/y dy = ln|y| + C` and
explain why the absolute value appears.

## Global lesson standards

Each Differential Equations lesson should follow the repository lesson
standards.

Use this structure for every `.qmd` page:

1. YAML front matter with `title`, `description`, and usually:

   ```yaml
   execute:
     echo: false
   ```

2. A short introduction explaining why the topic matters.
3. Learning objectives written as student-facing action statements.
4. Concept sections with definitions, intuition, formulas, and common pitfalls.
5. Worked examples with step-by-step reasoning.
6. Practice exercises with answers or collapsed solutions.
7. A topic-specific interactive checkpoint or guessing game before the Python
   appendix.
8. A final section named exactly:

   ```text
   Using this lesson with edumath and SymPy
   ```

   This final section should use visible code blocks with `#| echo: true`.

Do not call the lesson pages notebooks in navigation or prose unless a page is
specifically about notebook usage.

## Code visibility guidelines

In the main lesson body:

- hide setup code with `execute: echo: false`;
- show mathematical outputs, plots, tables, and explanations;
- avoid raw implementation code unless the code itself is the lesson objective.

In the final `Using this lesson with edumath and SymPy` appendix:

- show visible Python examples with `#| echo: true`;
- include examples that students can copy into Quarto, Jupyter, Colab, or a
  local Python session;
- explain how to interpret symbolic and numerical results;
- show both exact SymPy workflows and reusable `edumath` helper functions when
  available.

## Shared interaction plan

Create a reusable static checkpoint include:

```text
docs/lessons/differential-equations/_includes/differential-equations-checkpoint.qmd
```

The include should use browser-native JavaScript, similar to the Algebra and
Calculus checkpoint patterns, so published HTML remains interactive without a
live Python kernel.

Potential topic keys:

- `first-order-equations`
- `separable-equations`
- `linear-equations`
- `slope-fields`
- `systems`
- `differential-equations-cumulative-review`

The include should support flexible question types:

- multiple choice;
- short numeric answer;
- expression matching by normalized text where possible;
- qualitative classification;
- guess a solution from a differential equation;
- guess an equation from a slope field description;
- match a model to a real situation;
- identify equilibrium points;
- choose the next Euler step.

Use one JSON configuration block per lesson, for example:

```html
<script type="application/json" class="edu-math-de-checkpoint-config">
  {
    "topic": "separable-equations",
    "title": "Separable equation checkpoint",
    "defaultTotal": 4
  }
</script>
```

Then include the shared fragment:

```qmd
{{< include _includes/differential-equations-checkpoint.qmd >}}
```

### Checkpoint game principles

Each guessing game should teach the lesson topic, not merely decorate the page.
Good differential-equation guessing games include:

- guess whether an equation is separable, linear, both, or neither;
- guess which symbolic solution matches an ODE and initial condition;
- guess the long-term behavior from the sign of `dy/dt`;
- guess the missing integration constant from an initial condition;
- guess the next Euler point;
- guess the equilibrium from a formula;
- guess whether a system spirals, grows, decays, or stays steady based on a
  simple coefficient matrix.

Each game should give supportive feedback, not just right/wrong scoring.
Feedback should explain the reasoning in one or two sentences.

## Online symbolic computation options

The main computational appendix should use SymPy because it is powerful,
open-source, and already familiar from other lessons.

Also mention, when useful, browser-side symbolic or numeric libraries that can
support online exercises:

- **PyScript/Pyodide + SymPy**: lets students run Python and SymPy in the
  browser. This is the closest web equivalent to using SymPy directly.
- **Math.js**: strong JavaScript library for numeric computation and expression
  parsing; useful for checking arithmetic, plotting data, and evaluating right-
  hand sides of differential equations.
- **Nerdamer**: JavaScript symbolic algebra library that can solve and simplify
  many expressions; useful for lightweight browser exercises.
- **Algebrite**: JavaScript computer algebra system inspired by symbolic
  manipulation systems; useful for some symbolic simplification and calculus.

Do not add a heavy dependency automatically. Prefer static JavaScript for simple
checkpoints. Propose PyScript/SymPy only for optional advanced interactive cells
or future enhancement pages.

## Proposed `edumath` package support

The current source package contains `src/edumath/differential_equations/`, but
most modules are empty except `solvers.py`, which currently includes Euler's
method. The lesson implementation should add small, reusable helpers only when
they directly improve pedagogy.

Recommended public helpers:

### `src/edumath/differential_equations/concepts.py`

Add concept metadata similar to other branches:

- `FIRST_ORDER_EQUATIONS`
- `SEPARABLE_EQUATIONS`
- `LINEAR_EQUATIONS`
- `SLOPE_FIELDS`
- `SYSTEMS`
- `DIFFERENTIAL_EQUATIONS_PATH`

Each concept should include:

- title;
- slug;
- short description;
- prerequisites;
- learning goals;
- common mistakes.

### `src/edumath/differential_equations/solvers.py`

Keep the existing `euler_method` and consider adding:

- `improved_euler_method` or `heun_method` for optional comparison;
- `rk4_method` only if needed for a later numerical methods lesson;
- `direction_field_values(f, x_values, y_values)` returning normalized slope
  segments or slope samples;
- `equilibrium_points_1d(expression, variable="y")` for simple autonomous
  equations;
- `classify_equilibrium_1d(expression, point, variable="y")` using sign changes
  on either side;
- `solve_separable_sympy(...)` as a guided wrapper only if it can stay simple;
- `solve_first_order_linear_sympy(...)` for integrating-factor examples, only if
  the API remains clear.

Avoid overpromising a general ODE solver. SymPy already provides `dsolve`; the
`edumath` layer should help students understand steps and examples.

### `src/edumath/differential_equations/plots.py`

Add plotting-scene helpers returning reusable scene data or Matplotlib axes:

- `slope_field_scene(...)`
- `euler_method_scene(...)`
- `solution_family_scene(...)`
- `phase_line_scene(...)`
- `linear_system_phase_plane_scene(...)` for simple two-dimensional systems.

Keep helpers lightweight and testable. If existing `edumath.core.plots` has
scene structures, reuse them.

### `src/edumath/differential_equations/exercises.py`

Add deterministic exercise builders:

- `classify_ode_exercise(seed=...)`;
- `separable_solution_exercise(seed=...)`;
- `linear_integrating_factor_exercise(seed=...)`;
- `euler_step_exercise(seed=...)`;
- `equilibrium_exercise(seed=...)`;
- `system_equilibrium_exercise(seed=...)`.

Each exercise should include prompt, answer, hints, and a short solution.

### `src/edumath/differential_equations/validators.py`

Add small checkers:

- `validate_solution_satisfies_ode(candidate, ode_rhs, variable="x", function_name="y")`;
- `validate_initial_condition(candidate, x0, y0, ...)`;
- `validate_numeric_trajectory(points, expected, tolerance=...)`;
- `validate_equilibrium(candidate, rhs, variable="y")`.

Use SymPy for symbolic checks where appropriate, but keep failure modes clear.

### `src/edumath/differential_equations/quizzes.py`

Add reusable quiz-question builders:

- classify ODE type;
- identify initial condition;
- match slope field behavior;
- compute an Euler step;
- select a correct separable solution;
- identify equilibrium and stability.

### Tests

Add `tests/test_differential_equations_helpers.py` covering:

- current and new solver behavior;
- deterministic exercise generation;
- validators for correct and incorrect answers;
- concept path slugs;
- plotting scene data shape;
- quiz question structure.

Keep API small. Do not add helpers merely because they are possible.

## Documentation implementation phases

### Phase 1 — Planning and structure

1. Replace `PLAN.md` with this plan.
2. Inspect all current differential-equation pages and source helpers.
3. Decide whether to add `index.qmd` immediately.
4. Decide whether to keep, remove, or ignore `slope-fields.quarto_ipynb`.
5. Create the shared checkpoint include.
6. Add sidebar entry for the new index page if created.

### Phase 2 — Source helper additions

1. Implement only the `edumath` helpers needed by the lesson content.
2. Export the small public API from
   `src/edumath/differential_equations/__init__.py`.
3. Add tests before relying on helpers in docs.
4. Run:

   ```bash
   poetry run pytest tests/test_differential_equations_helpers.py
   ```

5. Run broader tests if helpers touch shared modules:

   ```bash
   poetry run pytest
   ```

### Phase 3 — Lesson writing

Write the lessons in this order:

1. `index.qmd`
2. `first-order-equations.qmd`
3. `separable-equations.qmd`
4. `linear-equations.qmd`
5. `slope-fields.qmd`
6. `systems.qmd`

This order builds from meaning, to symbolic solving, to numerical/visual
reasoning, to multi-variable dynamics.

### Phase 4 — Validation

For docs-only changes, run scoped checks:

```bash
poetry run pre-commit run --files <changed files>
quarto render <changed .qmd files> --no-execute
```

For source changes, run:

```bash
poetry run pytest
```

If Quarto creates temporary files, remove generated scratch/session folders,
especially `docs/.quarto/quarto-session-temp*`.

## Lesson plan: `index.qmd`

### Purpose

Create a friendly overview page that explains what differential equations are,
why they matter, and how the lesson sequence fits together.

### Front matter

```yaml
---
title: Differential Equations Study Path
description:
  A guided path through first-order equations, slope fields, and systems.
execute:
  echo: false
---
```

### Content outline

1. **Opening intuition**

   - A regular equation asks for a number.
   - A differential equation asks for a function.
   - The equation gives a rule for the derivative.
   - A solution is a function that follows the rule.

2. **Why differential equations matter**

   - population growth;
   - cooling and heating;
   - motion;
   - medicine concentration;
   - finance and interest;
   - predator-prey models;
   - electrical circuits.

3. **Prerequisite checklist**

   - derivative meaning;
   - basic antiderivatives;
   - exponentials/logarithms;
   - graph reading;
   - algebraic rearrangement;
   - initial conditions.

4. **The study path**

   - first-order equations: language and meaning;
   - separable equations: exact symbolic solving by separating variables;
   - linear equations: integrating factors and forcing terms;
   - slope fields: visual and numerical reasoning;
   - systems: several changing quantities at once.

5. **How to study**

   - read equations aloud;
   - check units;
   - sketch direction before solving;
   - verify by differentiating;
   - use computation as a checker;
   - explain results in words.

6. **Readiness checkpoint game**

   - use topic key `differential-equations-cumulative-review`;
   - ask students to classify short prompts as derivative, solution, initial
     condition, equilibrium, or model.

7. **Using this lesson with edumath and SymPy**
   - visible imports from `edumath.differential_equations`;
   - show `euler_method` on `y' = y`;
   - show SymPy `dsolve` for `y' = y`;
   - explain that the exact solution and Euler approximation are different kinds
     of answers.

### Practice ideas

- Identify whether each sentence describes a derivative, a solution, or an
  initial condition.
- Match a real situation to a differential equation form.
- Explain in words what `dy/dt = 0.2y` means.

## Lesson plan: `first-order-equations.qmd`

### Purpose

Teach students what a first-order differential equation is and how to interpret
it before solving anything complicated.

### Main learning objectives

Students should be able to:

- recognize an equation involving a first derivative;
- distinguish the independent variable, dependent variable, derivative, and
  right-hand side;
- explain what a solution function means;
- understand an initial condition;
- verify a proposed solution by substitution;
- interpret units in a first-order model.

### Content outline

1. **Motivation: rules for change**

   - Compare `y = 3x + 2` with `dy/dx = 3`.
   - Explain that a differential equation often tells how a quantity changes,
     not the quantity directly.

2. **Definition**

   - A first-order ODE involves the first derivative of an unknown function.
   - General form:

     ```text
     dy/dx = f(x, y)
     ```

   - Define `x`, `y`, `dy/dx`, and `f(x, y)`.

3. **Solution functions**

   - A solution is a function `y(x)` that makes the equation true.
   - Demonstrate verification:

     ```text
     y = Ce^x solves dy/dx = y
     ```

   - Different constants give different curves.

4. **Initial conditions**

   - Explain `y(0) = 5` as a starting value.
   - Show how it selects one solution from a family.

5. **Units and meaning**

   - If `y` is population and `t` is years, `dy/dt` is people per year.
   - If `dy/dt = 0.1y`, then growth is proportional to current population.

6. **Common forms**

   - Constant rate: `dy/dt = k`.
   - Proportional growth/decay: `dy/dt = ky`.
   - Forced change: `dy/dt = input - output`.
   - Autonomous equation: `dy/dt = f(y)`.

7. **Worked examples**

   - Verify `y = 2e^{3t}` solves `dy/dt = 3y`.
   - Find the solution from a family `y = C e^{-2t}` using `y(0)=7`.
   - Interpret `dT/dt = -0.4(T - 20)` in words.

8. **Practice exercises**

   - Identify the order of several equations.
   - Verify or reject candidate solutions.
   - Interpret an initial condition.
   - Translate a sentence into a differential equation.

9. **Guessing game**

   - Topic key: `first-order-equations`.
   - Game: "Guess the missing piece." Given a model sentence, choose the
     derivative, initial condition, or solution interpretation.

10. **Using this lesson with edumath and SymPy**
    - Show SymPy `dsolve` for a simple equation.
    - Show substituting a candidate solution into the ODE.
    - Show `edumath` validator if implemented.

### Common pitfalls to address

- Thinking `dy/dx` is a fraction without context.
- Confusing a differential equation with its solution.
- Forgetting that a family of solutions needs an initial condition.
- Ignoring units.
- Treating `x` and `y` symmetrically when one is dependent on the other.

## Lesson plan: `separable-equations.qmd`

### Purpose

Teach the first exact symbolic solution method: separate variables, integrate
both sides, solve for the dependent variable when possible, and apply an initial
condition.

### Main learning objectives

Students should be able to:

- recognize separable equations;
- rearrange `dy/dx = g(x)h(y)` into separated form;
- integrate both sides;
- include and combine constants of integration;
- apply an initial condition;
- check the solution by differentiating;
- understand when constant solutions may be lost during division.

### Content outline

1. **Motivation: undoing a derivative rule**

   - Separable equations work because each side can be integrated with respect
     to its own variable.

2. **Definition**

   - A separable ODE can be written as:

     ```text
     dy/dx = g(x)h(y)
     ```

   - Rearranged as:

     ```text
     1/h(y) dy = g(x) dx
     ```

3. **The separation workflow**

   - Identify `g(x)` and `h(y)`.
   - Move all `y` terms with `dy`.
   - Move all `x` terms with `dx`.
   - Integrate both sides.
   - Add a constant.
   - Solve for `y` if useful.
   - Apply an initial condition.
   - Check by differentiating.

4. **Example 1: exponential growth**

   - Solve `dy/dt = ky`.
   - Explain `ln|y| = kt + C`.
   - Derive `y = Ce^{kt}`.
   - Apply `y(0)=y0`.

5. **Example 2: polynomial right side**

   - Solve `dy/dx = x y^2`.
   - Show why dividing by `y^2` can miss the constant solution `y=0`.

6. **Example 3: cooling-style equation**

   - Solve `dT/dt = -k(T - A)`.
   - Interpret equilibrium temperature `A`.

7. **Initial conditions**

   - Show how `C` changes based on starting value.
   - Emphasize that solving for `C` is algebra, not a new calculus idea.

8. **Practice exercises**

   - Classify equations as separable or not.
   - Solve a simple separable ODE.
   - Apply an initial condition.
   - Check a solution.
   - Identify a lost constant solution.

9. **Guessing game**

   - Topic key: `separable-equations`.
   - Game: "Can it separate?" Students see an ODE and guess `separable`,
     `not separable`, or `separable after algebra`.
   - Include feedback explaining how to move terms.

10. **Using this lesson with edumath and SymPy**
    - Show SymPy `dsolve` for separable equations.
    - Show manual verification by differentiating the solution.
    - Show any `edumath` separable exercise or validator helpers.

### Common pitfalls to address

- Forgetting the `dy` and `dx` differential notation is a guide to integration.
- Dividing by an expression that might be zero and losing equilibrium solutions.
- Writing two constants instead of combining them into one.
- Dropping absolute values in logarithms without explanation.
- Solving for `y` too early or making algebra errors after integration.

## Lesson plan: `linear-equations.qmd`

### Purpose

Teach first-order linear ODEs using integrating factors. Emphasize pattern
recognition, the meaning of decay/growth plus forcing, and careful algebra.

### Main learning objectives

Students should be able to:

- recognize standard linear form `dy/dx + p(x)y = q(x)`;
- identify `p(x)` and `q(x)`;
- compute an integrating factor;
- multiply the equation by the integrating factor;
- recognize the left side as a product derivative;
- integrate and solve;
- apply initial conditions;
- interpret forcing and proportional feedback.

### Content outline

1. **Motivation: not every equation separates**

   - Show `dy/dx + 2y = x`.
   - Explain why it is not separable in the basic way.
   - Introduce the linear structure.

2. **Standard form**

   - The equation must be written as:

     ```text
     dy/dx + p(x)y = q(x)
     ```

   - Define `p(x)` and `q(x)`.
   - Warn students to divide by the coefficient of `dy/dx` if needed.

3. **Intuition for the integrating factor**

   - We want the left side to become the derivative of a product:

     ```text
     d/dx [mu(x)y]
     ```

   - The integrating factor is:

     ```text
     mu(x) = e^(∫p(x) dx)
     ```

4. **Step-by-step algorithm**

   - Put in standard form.
   - Identify `p(x)` and `q(x)`.
   - Compute `mu(x)`.
   - Multiply every term by `mu(x)`.
   - Rewrite left side as `(mu y)'`.
   - Integrate both sides.
   - Solve for `y`.
   - Apply initial condition.

5. **Worked example 1: constant coefficient**

   - Solve `dy/dx + 2y = 6`.
   - Interpret stable equilibrium `y=3`.

6. **Worked example 2: variable coefficient**

   - Solve `dy/dx + (1/x)y = x` for `x > 0`.
   - Discuss domain restriction.

7. **Worked example 3: applied model**

   - Mixing tank or cooling with external forcing.
   - Keep arithmetic simple.

8. **Practice exercises**

   - Identify whether equations are linear.
   - Put equations into standard form.
   - Compute integrating factors.
   - Complete missing step in solution.
   - Solve one full equation with initial condition.

9. **Guessing game**

   - Topic key: `linear-equations`.
   - Game: "Find the integrating factor." Students identify `p(x)` and choose
     the correct `mu(x)`.

10. **Using this lesson with edumath and SymPy**
    - Show SymPy `dsolve` for linear equations.
    - Show how to verify the solution.
    - If an `edumath` helper exists, show a guided integrating-factor example.

### Common pitfalls to address

- Forgetting to put the equation in standard form first.
- Using `q(x)` instead of `p(x)` in the integrating factor.
- Multiplying only some terms by the integrating factor.
- Not recognizing the product derivative.
- Losing the constant of integration.
- Ignoring domain restrictions such as `x > 0`.

## Lesson plan: `slope-fields.qmd`

### Purpose

Teach qualitative and numerical understanding of ODEs without requiring exact
symbolic solutions. Students should learn that a slope field is a map of local
change directions.

### Main learning objectives

Students should be able to:

- interpret a slope field as local derivative information;
- sketch approximate solution curves through initial points;
- connect slope fields to the formula `dy/dx = f(x,y)`;
- identify equilibrium solutions in autonomous equations;
- use Euler's method for a simple numerical approximation;
- understand how step size affects approximation quality.

### Content outline

1. **Motivation: seeing change without solving**

   - Some equations are hard or impossible to solve exactly.
   - Slope fields let us understand behavior anyway.

2. **What each segment means**

   - At a point `(x,y)`, compute `f(x,y)`.
   - Draw a short line segment with that slope.
   - A solution curve follows the local directions.

3. **Reading slope fields**

   - horizontal segments mean derivative zero;
   - steep positive segments mean rapid increase;
   - steep negative segments mean rapid decrease;
   - repeated patterns reveal autonomous equations;
   - curves should not cross if the ODE has uniqueness.

4. **Equilibrium solutions**

   - In `dy/dt = f(y)`, equilibrium occurs where `f(y)=0`.
   - Explain stable, unstable, and semistable behavior using arrows.

5. **Euler's method**

   - Formula:

     ```text
     y_{n+1} = y_n + h f(x_n, y_n)
     x_{n+1} = x_n + h
     ```

   - Explain it as "use the current slope for one small step."

6. **Worked example 1: slope field interpretation**

   - For `dy/dx = x - y`, describe slopes in regions.

7. **Worked example 2: phase line**

   - For `dy/dt = y(1-y)`, find equilibria `0` and `1`.
   - Explain stability from signs.

8. **Worked example 3: Euler method**

   - Approximate `dy/dx = y`, `y(0)=1`, step `0.1`, for three steps.
   - Compare with exact `e^x` qualitatively.

9. **Practice exercises**

   - Match formulas to slope field descriptions.
   - Identify equilibrium levels.
   - Compute one or two Euler steps.
   - Explain whether a solution increases or decreases from an initial value.

10. **Guessing game**

    - Topic key: `slope-fields`.
    - Game: "Next Euler step." Given `(x_n, y_n)`, step size, and `f(x,y)`,
      students guess `(x_{n+1}, y_{n+1})`.
    - Alternate game: "Guess the equilibrium." Given `dy/dt = f(y)`, choose the
      equilibrium and stability.

11. **Using this lesson with edumath and SymPy**
    - Show `euler_method` from `edumath.differential_equations.solvers`.
    - Show a slope field plotting helper if implemented.
    - Show SymPy exact solution for comparison where possible.

### Common pitfalls to address

- Treating the line segments as the solution curves themselves.
- Thinking every ODE must be solved exactly.
- Forgetting Euler's method updates both `x` and `y`.
- Using the new slope too soon in basic Euler's method.
- Thinking smaller step size makes the method exact.
- Confusing equilibrium points with intercepts of a solution graph.

## Lesson plan: `systems.qmd`

### Purpose

Introduce systems of differential equations as models for multiple quantities
that change together. Keep the scope introductory and visual, with connections
to linear algebra.

### Main learning objectives

Students should be able to:

- recognize a system of first-order ODEs;
- explain what coupled variables mean;
- write a simple linear system in matrix form;
- find equilibrium points by setting all derivatives equal to zero;
- interpret phase-plane arrows and trajectories;
- connect eigenvalue signs to basic growth/decay behavior in simple cases;
- use numerical approximation for systems conceptually.

### Content outline

1. **Motivation: one variable is not always enough**

   - predator and prey;
   - position and velocity;
   - competing populations;
   - interacting chemical concentrations.

2. **General form**

   - Present:

     ```text
     dx/dt = f(x,y)
     dy/dt = g(x,y)
     ```

   - Explain that the state is now a point `(x,y)` moving through the plane.

3. **Coupling**

   - `dx/dt` may depend on `y`.
   - `dy/dt` may depend on `x`.
   - Coupling means variables influence each other's rates.

4. **Equilibria**

   - Set every derivative to zero:

     ```text
     f(x,y)=0
     g(x,y)=0
     ```

   - Solve the simultaneous equations.
   - Interpret an equilibrium as a state with no movement.

5. **Linear systems and matrices**

   - Introduce:

     ```text
     x' = A x
     ```

   - Use `x` as a vector carefully; distinguish from scalar variable.
   - Show simple diagonal matrix example:

     ```text
     u' = -2u
     v' = 3v
     ```

   - Explain one component decays and the other grows.

6. **Phase plane intuition**

   - Arrows show velocity vector `(dx/dt, dy/dt)`.
   - A trajectory follows the arrows.
   - Equilibria are places where the arrow has zero length.

7. **Worked example 1: independent equations**

   - `x' = -x`, `y' = -2y`.
   - Equilibrium `(0,0)`.
   - Both components decay.

8. **Worked example 2: coupled linear system**

   - Use a simple matrix such as:

     ```text
     x' = y
     y' = -x
     ```

   - Explain rotating behavior qualitatively.

9. **Worked example 3: predator-prey interpretation**

   - Keep formulas simple.
   - Focus on signs and interactions, not full solution.

10. **Practice exercises**

    - Identify coupled vs uncoupled systems.
    - Find equilibria for simple systems.
    - Convert a linear system to matrix form.
    - Interpret phase-plane arrows at selected points.
    - Match real scenarios to system structures.

11. **Guessing game**

    - Topic key: `systems`.
    - Game: "Guess the equilibrium." Given two derivative formulas, choose the
      point where both rates are zero.
    - Alternate game: "Guess the motion." Given a simple matrix, choose decay,
      growth, rotation, or saddle-like behavior.

12. **Using this lesson with edumath and SymPy**
    - Show SymPy solving equilibrium equations.
    - Show matrix form with `sympy.Matrix`.
    - Show simple numerical stepping if an `edumath` system solver is added.

### Common pitfalls to address

- Setting only one derivative equal to zero when finding an equilibrium.
- Confusing a state point `(x,y)` with a graph of `y` versus `x`.
- Thinking every system has an easy formula solution.
- Forgetting that vectors in the phase plane represent rates of change.
- Overusing eigenvalues before students understand qualitative behavior.

## Optional future lesson: `applications.qmd`

If the module needs a final applications page, add it after `systems.qmd`.

Possible topics:

- exponential growth and decay;
- Newton's law of cooling;
- logistic growth;
- mixing tanks;
- falling objects with resistance;
- predator-prey models;
- RC circuits.

The applications lesson should teach a modeling workflow:

1. Define variables and units.
2. Translate rate language into an equation.
3. Identify initial conditions.
4. Solve exactly if reasonable.
5. Approximate numerically if needed.
6. Interpret the result.
7. Check whether the answer is realistic.

## Suggested references for lesson authors

Use these as conceptual references while writing. Avoid copying text.

- OpenStax, _Calculus Volume 2_, differential equations chapters.
- Paul Dawkins, Paul's Online Math Notes, Differential Equations.
- MIT OpenCourseWare, Differential Equations materials.
- Boyce and DiPrima, _Elementary Differential Equations and Boundary Value
  Problems_.
- Blanchard, Devaney, and Hall, _Differential Equations_.

## Acceptance checklist

Before considering the plan implemented, verify the following:

### Content completeness

- [ ] `index.qmd` exists and is linked in `docs/_quarto.yml`.
- [ ] Every lesson has YAML front matter with title, description, and execution
      settings.
- [ ] Every lesson begins with motivation and learning objectives.
- [ ] Every lesson contains definitions, intuition, formulas, and common
      pitfalls.
- [ ] Every lesson has at least two worked examples.
- [ ] Every lesson has practice exercises with answers or collapsed solutions.
- [ ] Every lesson has a topic-specific checkpoint or guessing game.
- [ ] Every lesson ends with `Using this lesson with edumath and SymPy`.
- [ ] SymPy examples show how to solve or verify the relevant ODEs.
- [ ] Visible code appears primarily in the final appendix.

### Pedagogy

- [ ] Lessons are written for students with low confidence and limited prior
      exposure.
- [ ] Each symbolic step is explained in words.
- [ ] Important algebra and calculus prerequisites are reviewed in context.
- [ ] Examples include units or real interpretation where useful.
- [ ] Common mistakes are explicitly named.
- [ ] Guessing games provide explanatory feedback.

### Package support

- [ ] Any new `edumath` helper has tests.
- [ ] Public API additions are exported intentionally.
- [ ] Helpers are reusable across lessons.
- [ ] General-purpose symbolic solving is delegated to SymPy rather than
      reimplemented poorly.

### Validation

- [ ] `poetry run pre-commit run --files <changed files>` passes.
- [ ] `poetry run pytest` passes if source files changed.
- [ ] `quarto render <changed qmd files> --no-execute` passes.
- [ ] Generated Quarto scratch/session files are removed before finishing.
