# PLAN: Linear Algebra Lessons

Target directory: `docs/lessons/linear-algebra/`

This plan describes how to turn the Linear Algebra lesson sequence into a
complete, beginner-friendly preparation module. The current pages are useful
starters, but they are short. The goal is to write self-contained study material
for learners who may know algebra and coordinates but are new to vectors,
matrices, systems, transformations, and eigenvectors.

Linear algebra should be taught as a language for organizing numbers and
understanding movement in space. Students should see every idea in multiple
forms: words, coordinates, geometry, tables, equations, and code.

## Current lesson files

Current pages in `docs/lessons/linear-algebra/`:

1. `vectors.qmd`
2. `matrices.qmd`
3. `matrix-operations.qmd`
4. `systems-and-elimination.qmd`
5. `linear-transformations.qmd`
6. `eigenvalues-eigenvectors.qmd`

Also present during inspection:

- `vectors.quarto_ipynb`
- `matrices.quarto_ipynb`
- `matrix-operations.quarto_ipynb`
- `systems-and-elimination.quarto_ipynb`

These appear to be generated Quarto notebook artifacts rather than intended
source pages. Before implementation, verify whether they are tracked. If they
are untracked/generated, remove them from the working tree. The lesson source
should remain `.qmd` files.

Recommended addition:

7. `index.qmd` — Linear Algebra study path overview and readiness checklist.

Update `docs/_quarto.yml` so the Linear Algebra sidebar starts with the new
index page if `index.qmd` is added. Update `docs/lessons/index.qmd` so the
Linear Algebra card links to `linear-algebra/index.qmd` instead of the first
content page.

## Overall pedagogical goals

The Linear Algebra module should help students move from single-number algebra
to structured reasoning about vectors, matrices, spaces, systems, and
transformations.

By the end of the path, a student should be able to say:

> Linear algebra studies vectors and the transformations that move them. A
> vector stores several numbers at once, a matrix describes a rule for combining
> or transforming vectors, and systems of linear equations ask which vectors
> satisfy several conditions at the same time.

Students should repeatedly practice these habits:

- Track dimensions and shapes before calculating.
- Interpret vectors geometrically and numerically.
- Read matrix-vector products as combinations of columns.
- Connect systems of equations to intersections and matrix notation.
- Explain what a transformation does to basis vectors.
- Use row operations as legal equation-preserving moves.
- Check whether an answer makes sense from units, shape, and geometry.
- Use NumPy and SymPy to compute and verify, not to skip understanding.

## Prerequisites to reinforce throughout

The lessons should review prerequisite ideas in context instead of assuming
students remember everything perfectly:

- coordinate plane and ordered pairs;
- basic algebraic equations;
- systems of two equations;
- graphing lines;
- arithmetic with negatives and fractions;
- square roots and distance formula;
- function notation;
- basic Python lists and arrays;
- interpreting tables of numbers;
- simple trigonometry for optional rotations.

Whenever a prerequisite appears, include a short reminder box. For example, in
vectors, remind students that the distance formula is a form of the Pythagorean
theorem. In systems, remind students that replacing one equation by a sum of two
equations can preserve the solution set.

## Global lesson standards

Each Linear Algebra lesson should follow the repository lesson standards.

Use this structure for every `.qmd` page:

1. YAML front matter with `title`, `description`, and usually:

   ```yaml
   execute:
     echo: false
   ```

2. A short introduction explaining why the topic matters.
3. Learning objectives written as student-facing action statements.
4. Concept sections with definitions, intuition, formulas, diagrams, and common
   pitfalls.
5. Worked examples with step-by-step reasoning.
6. Practice exercises with answers or collapsed solutions.
7. A topic-specific interactive checkpoint or guessing game before the Python
   appendix.
8. A final section named exactly:

   ```text
   Using this lesson with edumath and SymPy
   ```

   Use visible code blocks with `#| echo: true` in this final section. NumPy may
   also appear in this section because it is central to linear algebra
   computation, but keep the section title consistent with the project standard.

Do not call these pages notebooks in navigation or lesson prose unless a page is
specifically about notebook usage.

## Code visibility guidelines

In the main lesson body:

- hide helper code with `execute: echo: false`;
- show vectors, matrices, plots, tables, row-reduction steps, and conclusions;
- avoid raw setup code unless the code itself is the teaching target.

In the final `Using this lesson with edumath and SymPy` appendix:

- show visible Python examples with `#| echo: true`;
- use `edumath.linear_algebra` helpers when available;
- use NumPy for numeric arrays and matrix products;
- use SymPy for exact arithmetic, row reduction, determinants, eigenvalues, and
  symbolic verification;
- explain how to interpret the computational output.

## Shared interaction plan

Create a reusable static checkpoint include:

```text
docs/lessons/linear-algebra/_includes/linear-algebra-checkpoint.qmd
```

The include should use browser-native JavaScript, similar to the Algebra,
Calculus, Differential Equations, and Discrete Mathematics checkpoint patterns,
so published HTML remains interactive without a live Python kernel.

Potential topic keys:

- `vectors`
- `matrices`
- `matrix-operations`
- `systems-and-elimination`
- `linear-transformations`
- `eigenvalues-eigenvectors`
- `linear-algebra-cumulative-review`

The include should support flexible question types:

- multiple choice;
- numeric answer;
- vector or matrix entry selection;
- shape/dimension checks;
- guess a dot product;
- guess a matrix-vector product;
- classify a system as one solution, no solution, or infinitely many;
- identify a transformation from a matrix;
- identify whether a vector is an eigenvector.

Use one JSON configuration block per lesson, for example:

```html
<script
  type="application/json"
  class="edu-math-linear-algebra-checkpoint-config"
>
  {
    "topic": "vectors",
    "title": "Vectors checkpoint",
    "defaultTotal": 4
  }
</script>
```

Then include the shared fragment:

```qmd
{{< include _includes/linear-algebra-checkpoint.qmd >}}
```

### Checkpoint game principles

Each guessing game should teach the lesson topic, not merely decorate the page.
Good linear-algebra guessing games include:

- guess the vector norm;
- guess whether two vectors are perpendicular;
- guess matrix shape;
- guess whether a product is defined;
- guess a matrix-vector product entry;
- guess the row operation needed next;
- guess whether a system is inconsistent, dependent, or independent;
- guess the geometric action of a 2-by-2 matrix;
- guess whether a vector is an eigenvector of a matrix;
- guess the eigenvalue from `A v = lambda v`.

Feedback should be explanatory and supportive. For example, after a wrong shape
answer, explain exactly which inner dimensions must match.

## Online computation options

The main computational appendix should use `edumath`, NumPy, and SymPy. Linear
algebra also benefits from browser-side visual tools.

Potential online libraries and tools:

- **PyScript/Pyodide + SymPy**: lets students run exact matrix calculations, row
  reduction, determinants, and eigenvalues in the browser.
- **NumPy in Pyodide**: useful for numeric vectors, matrix products, and quick
  experimentation.
- **Math.js**: useful for lightweight browser matrix arithmetic and numeric
  exercises.
- **D3.js or SVG-only JavaScript**: useful for future interactive vector and
  transformation visualizations.
- **Plotly.js**: useful for interactive 2D or 3D vector plots if the project
  later chooses richer visuals.

Do not add heavy JavaScript dependencies automatically. Prefer static
browser-native JavaScript for checkpoints. Propose PyScript or visualization
libraries only for optional future enhancements.

## Proposed `edumath` package support

The current package contains `src/edumath/linear_algebra/`. At inspection time,
most modules were empty except `concepts.py`, which includes numeric helpers:

- `dot_product`
- `vector_norm`
- `matrix_vector_product`
- `solve_linear_system`

These helpers are useful and should remain available for compatibility. However,
lesson work may benefit from adding concept metadata, validators, exercises,
quizzes, and plotting helpers.

### Organization note

Because `concepts.py` currently contains computational helpers, implementation
has two reasonable options:

1. Keep the existing helper functions in `concepts.py` and add concept metadata
   there as well.
2. Move computational helpers to a new `operations.py` module and re-export them
   from `concepts.py` and `__init__.py` for backward compatibility.

Prefer the smallest safe change. Do not break existing imports such as:

```python
from edumath.linear_algebra.concepts import matrix_vector_product
```

### `src/edumath/linear_algebra/concepts.py`

Add concept metadata similar to other branches:

- `VECTORS`
- `MATRICES`
- `MATRIX_OPERATIONS`
- `SYSTEMS_AND_ELIMINATION`
- `LINEAR_TRANSFORMATIONS`
- `EIGENVALUES_EIGENVECTORS`
- `LINEAR_ALGEBRA_PATH`

Each concept should include:

- title;
- slug;
- short description;
- prerequisites;
- measurable learning goals;
- tags or common mistakes.

Expected path order:

```text
vectors -> matrices -> matrix-operations -> systems-and-elimination -> linear-transformations -> eigenvalues-eigenvectors
```

### `src/edumath/linear_algebra/operations.py` or additions to `concepts.py`

Consider adding small, well-tested helpers:

- `vector_add(left, right)`;
- `scalar_multiply(scalar, vector_or_matrix)`;
- `matrix_shape(matrix)`;
- `can_multiply(left_shape, right_shape)`;
- `matrix_product(left, right)`;
- `identity_matrix(size)`;
- `determinant_2x2(matrix)`;
- `inverse_2x2(matrix)`;
- `row_echelon_steps(matrix, values=None)` for pedagogical row-reduction steps,
  only if the API can remain simple;
- `eigenvalues_2x2(matrix)` for small exact/numeric examples.

Avoid creating a full replacement for NumPy or SymPy. The `edumath` layer should
make examples easier to teach.

### `src/edumath/linear_algebra/exercises.py`

Add deterministic exercise builders:

- `vector_norm_exercise(seed=...)`;
- `dot_product_exercise(seed=...)`;
- `matrix_shape_exercise(seed=...)`;
- `matrix_vector_product_exercise(seed=...)`;
- `linear_system_exercise(seed=...)`;
- `transformation_classification_exercise(seed=...)`;
- `eigenvector_check_exercise(seed=...)`.

Each exercise should include prompt, expected answer, hints, explanation, tags,
and validators where useful.

### `src/edumath/linear_algebra/validators.py`

Add small checkers:

- `validate_vector_answer(received, expected, tolerance=...)`;
- `validate_matrix_answer(received, expected, tolerance=...)`;
- `validate_scalar_answer(received, expected, tolerance=...)`;
- `validate_solution_vector(received, matrix, values, tolerance=...)`;
- `validate_eigenpair(matrix, vector, eigenvalue, tolerance=...)`;
- `validate_shape_answer(received, expected)`.

Validators should accept common student formats when practical, such as Python
lists, tuples, NumPy arrays, and comma-separated strings.

### `src/edumath/linear_algebra/plots.py`

Add lightweight plotting-scene helpers using existing core plot primitives:

- `vector_scene(vectors, labels=None)`;
- `vector_addition_scene(left, right)`;
- `matrix_transformation_scene(matrix, vectors=None)`;
- `basis_transformation_scene(matrix)`;
- `system_lines_scene(matrix, values)` for 2-by-2 systems;
- `eigenvector_scene(matrix, vector)`.

For 2D lessons, scenes should make geometry visible. Keep them Matplotlib-based
and testable. Do not add a heavy plotting dependency.

### `src/edumath/linear_algebra/quizzes.py`

Add quiz-question builders:

- vector norm question;
- dot product/perpendicular question;
- matrix shape question;
- product-defined question;
- matrix-vector product question;
- system classification question;
- transformation action question;
- eigenvalue/eigenvector question;
- cumulative linear algebra diagnostic quiz.

### Tests

Add `tests/test_linear_algebra_helpers.py` covering:

- existing helper behavior;
- any new operations;
- deterministic exercise generation;
- validators accepting correct and rejecting incorrect answers;
- concept path slugs;
- plotting scene render or scene-data shape;
- quiz builder structure.

Run the full test suite if any shared helpers are changed.

## Documentation implementation phases

### Phase 1 — Planning and structure

1. Replace `PLAN.md` with this plan.
2. Inspect all current linear-algebra pages and source helpers.
3. Decide whether to add `index.qmd` immediately.
4. Remove generated `.quarto_ipynb*` artifacts if they are untracked.
5. Create the shared checkpoint include.
6. Add sidebar entry for the new index page if created.
7. Update the Linear Algebra card in `docs/lessons/index.qmd`.

### Phase 2 — Source helper additions

1. Implement only `edumath` helpers needed by the lesson content.
2. Export the small public API from `src/edumath/linear_algebra/__init__.py`.
3. Preserve existing imports from `src/edumath/linear_algebra/concepts.py`.
4. Add tests before relying on helpers in docs.
5. Run:

   ```bash
   poetry run pytest tests/test_linear_algebra_helpers.py
   ```

6. Run broader tests if helpers touch shared modules:

   ```bash
   poetry run pytest
   ```

### Phase 3 — Lesson writing

Write the lessons in this order:

1. `index.qmd`
2. `vectors.qmd`
3. `matrices.qmd`
4. `matrix-operations.qmd`
5. `systems-and-elimination.qmd`
6. `linear-transformations.qmd`
7. `eigenvalues-eigenvectors.qmd`

This order builds from vector objects, to matrix objects, to operations, to
systems, to transformations, to special directions.

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
especially `docs/.quarto/quarto-session-temp*`, `.quarto-tmp/`, and unwanted
`*.quarto_ipynb*` artifacts.

## Lesson plan: `index.qmd`

### Purpose

Create a friendly overview page that explains what linear algebra is, why it
matters, and how the lesson sequence fits together.

### Front matter

```yaml
---
title: Linear Algebra Study Path
description:
  A guided path through vectors, matrices, systems, transformations, and
  eigenvectors.
execute:
  echo: false
---
```

### Content outline

1. **Opening intuition**

   - Algebra often studies one number at a time.
   - Linear algebra studies lists of numbers and rules that transform them.
   - Vectors can represent positions, directions, data points, or unknowns.
   - Matrices can represent systems, transformations, or organized data.

2. **Why linear algebra matters**

   - solving systems of equations;
   - computer graphics;
   - data science and machine learning;
   - optimization;
   - networks;
   - differential equations;
   - quantum mechanics and engineering models.

3. **Prerequisite checklist**

   - coordinate plane;
   - systems of equations;
   - basic algebra;
   - square roots and distance;
   - function notation;
   - Python lists or arrays.

4. **The study path**

   - vectors: multi-number objects;
   - matrices: rectangular arrays;
   - operations: addition, products, shape checks;
   - systems: solving `A x = b`;
   - transformations: matrices as functions;
   - eigenvalues/eigenvectors: directions preserved by transformations.

5. **How to study**

   - draw small 2D examples;
   - track shape before multiplying;
   - say what each row or column means;
   - compute by hand first;
   - verify with NumPy or SymPy;
   - interpret results geometrically.

6. **Readiness checkpoint game**

   - topic key `linear-algebra-cumulative-review`;
   - ask students to classify prompts as vector, matrix, system, transformation,
     or eigenvector ideas.

7. **Using this lesson with edumath and SymPy**
   - show `dot_product`, `vector_norm`, `matrix_vector_product`;
   - show NumPy arrays;
   - show SymPy Matrix exact arithmetic;
   - explain numeric versus exact computation.

### Practice ideas

- Identify whether each object is a scalar, vector, matrix, or system.
- Match a real-world scenario to a linear-algebra object.
- Explain why matrix shape matters before multiplying.

## Lesson plan: `vectors.qmd`

### Purpose

Teach vectors as ordered lists of numbers with both geometric and data
interpretations. Build comfort with addition, scalar multiplication, norms, dot
products, and perpendicularity.

### Main learning objectives

Students should be able to:

- interpret vectors as arrows, positions, displacements, or data rows;
- add and subtract vectors component by component;
- multiply a vector by a scalar;
- compute vector norm in 2D and 3D;
- compute dot products;
- interpret dot products geometrically;
- recognize perpendicular vectors from dot product zero.

### Content outline

1. **Motivation: one object, many numbers**

   - A vector stores multiple related numbers.
   - Examples: movement, velocity, color, data record, unknown variables.

2. **Coordinate and arrow interpretations**

   - `[3,4]` as a point;
   - `[3,4]` as an arrow from origin;
   - `[3,4]` as a displacement.

3. **Vector addition**

   - Component-wise rule.
   - Geometric tip-to-tail interpretation.

4. **Scalar multiplication**

   - Stretch, shrink, reverse.
   - Negative scalars flip direction.

5. **Norm/length**

   - `||v|| = sqrt(v_1^2 + ... + v_n^2)`.
   - Connect to distance formula.

6. **Dot product**

   - Formula `u dot v = sum u_i v_i`.
   - Perpendicularity when dot product is zero.
   - Optional projection intuition.

7. **Worked examples**

   - Add `[2, -1] + [3, 4]`.
   - Compute `||[6,8]||`.
   - Compute `[1,2] dot [3,4]`.
   - Check whether `[1,0]` and `[0,1]` are perpendicular.

8. **Practice exercises**

   - Addition and scalar multiplication.
   - Norms.
   - Dot products.
   - Geometric interpretation.

9. **Guessing game**

   - Topic key: `vectors`.
   - Game: "Vector quick check." Guess norm, dot product, or perpendicularity.

10. **Using this lesson with edumath and SymPy**
    - Show `dot_product`, `vector_norm`.
    - Show NumPy arrays.
    - Show SymPy Matrix dot products and exact square roots.

### Common pitfalls to address

- Treating a vector like a single number.
- Adding vectors with different dimensions.
- Forgetting square roots in norms.
- Thinking dot product produces another vector.
- Forgetting that dot product zero means perpendicular only for nonzero vectors.

## Lesson plan: `matrices.qmd`

### Purpose

Teach matrices as rectangular arrays with shape, entries, rows, columns, and
multiple meanings: data tables, coefficient arrays, and transformation rules.

### Main learning objectives

Students should be able to:

- identify rows, columns, entries, and shape;
- write matrix entries using row-column notation;
- recognize row vectors and column vectors;
- identify zero and identity matrices;
- explain why shape matters;
- connect matrices to data, systems, and transformations.

### Content outline

1. **Motivation: organized numbers**

   - Matrices organize many related numbers.
   - Examples: data table, image pixels, system coefficients, transformations.

2. **Rows and columns**

   - Shape is rows by columns.
   - Entry notation `a_ij` means row `i`, column `j`.

3. **Matrix equality**

   - Same shape and same corresponding entries.

4. **Special matrices**

   - Zero matrix.
   - Identity matrix.
   - Diagonal matrix.
   - Square matrix.
   - Column vectors as `n x 1` matrices.

5. **Shape as a safety check**

   - Students should say shape before performing operations.

6. **Worked examples**

   - Find the shape of a matrix.
   - Identify a specific entry.
   - Write a 2-by-2 identity matrix.
   - Interpret a matrix as a data table.

7. **Practice exercises**

   - Shape checks.
   - Entry identification.
   - Special matrix recognition.
   - Data interpretation.

8. **Guessing game**

   - Topic key: `matrices`.
   - Game: "Shape detective." Guess shape, entry, or special matrix type.

9. **Using this lesson with edumath and SymPy**
   - Show `matrix_shape` if implemented.
   - Show NumPy `.shape`.
   - Show SymPy `Matrix` and indexing.

### Common pitfalls to address

- Reversing rows and columns.
- Thinking all matrices must be square.
- Confusing entry `a_ij` with `a_ji`.
- Treating row vectors and column vectors as interchangeable.
- Forgetting identity matrix size.

## Lesson plan: `matrix-operations.qmd`

### Purpose

Teach matrix addition, scalar multiplication, matrix-vector products, matrix
products, identity matrices, and dimension compatibility.

### Main learning objectives

Students should be able to:

- add matrices with the same shape;
- multiply matrices by scalars;
- decide whether products are defined;
- compute matrix-vector products;
- interpret matrix-vector products as combinations of columns;
- multiply small matrices;
- use identity matrices correctly.

### Content outline

1. **Motivation: operations with shape rules**

   - Matrix operations are not arbitrary; dimensions control what is legal.

2. **Addition and subtraction**

   - Same shape required.
   - Component-wise calculation.

3. **Scalar multiplication**

   - Multiply every entry.

4. **Matrix-vector products**

   - Row-dot-vector calculation.
   - Column-combination interpretation.

5. **Matrix-matrix products**

   - Inner dimensions must match.
   - Product shape: `(m x n)(n x p) = m x p`.

6. **Identity matrix**

   - Leaves compatible vectors or matrices unchanged.

7. **Worked examples**

   - Add two 2-by-2 matrices.
   - Compute scalar multiple.
   - Compute `[[2,0],[0,3]] [5,4]`.
   - Decide whether a 2-by-3 matrix can multiply a length-2 vector.
   - Compute a small 2-by-2 matrix product.

8. **Practice exercises**

   - Shape compatibility.
   - Matrix addition.
   - Matrix-vector products.
   - Matrix products.

9. **Guessing game**

   - Topic key: `matrix-operations`.
   - Game: "Product defined?" or "Guess the missing entry."

10. **Using this lesson with edumath and SymPy**
    - Show `matrix_vector_product`.
    - Show NumPy `@` operator.
    - Show SymPy exact matrix products.

### Common pitfalls to address

- Adding matrices with different shapes.
- Multiplying entry-by-entry when a matrix product is requested.
- Forgetting that matrix multiplication is usually not commutative.
- Reversing product shape.
- Forgetting to check inner dimensions.

## Lesson plan: `systems-and-elimination.qmd`

### Purpose

Teach linear systems through equations, augmented matrices, row operations,
elimination, matrix notation `A x = b`, and solution classification.

### Main learning objectives

Students should be able to:

- write a system as `A x = b`;
- build an augmented matrix;
- use row operations to simplify a system;
- solve small systems by elimination;
- identify one solution, no solution, or infinitely many solutions;
- interpret systems geometrically in two variables;
- verify a solution by substitution.

### Content outline

1. **Motivation: many conditions at once**

   - A system asks for values satisfying every equation simultaneously.

2. **Matrix form**

   - Coefficient matrix `A`;
   - unknown vector `x`;
   - right-hand side vector `b`.

3. **Augmented matrices**

   - Store coefficients and constants compactly.

4. **Legal row operations**

   - Swap rows.
   - Multiply a row by a nonzero constant.
   - Add a multiple of one row to another row.

5. **Elimination**

   - Use row operations to create zeros.
   - Back-substitute.

6. **Solution types**

   - One solution: independent equations.
   - No solution: contradiction such as `0 = 5`.
   - Infinitely many solutions: free variable or repeated condition.

7. **Geometry**

   - In two variables: lines intersect, parallel lines, same line.
   - In three variables: planes.

8. **Worked examples**

   - Solve `x+y=5`, `x-y=1`.
   - Show an inconsistent system.
   - Show a dependent system.
   - Verify a solution vector.

9. **Practice exercises**

   - Convert to matrix form.
   - Perform one row operation.
   - Solve 2-by-2 systems.
   - Classify solution type.

10. **Guessing game**

    - Topic key: `systems-and-elimination`.
    - Game: "System classifier." Guess one solution, no solution, or infinitely
      many from equations or reduced rows.

11. **Using this lesson with edumath and SymPy**
    - Show `solve_linear_system` for numeric systems.
    - Show SymPy `Matrix.rref()` for exact row reduction.
    - Show substitution verification.

### Common pitfalls to address

- Changing one equation without applying a legal row operation.
- Losing a sign during elimination.
- Confusing no solution with infinitely many solutions.
- Forgetting to check the solution in original equations.
- Treating row operations as changing the solution set instead of preserving it.

## Lesson plan: `linear-transformations.qmd`

### Purpose

Teach matrices as functions that transform vectors. Emphasize basis vectors,
geometry, linearity, and common transformations such as scaling, reflection,
projection, shear, and rotation.

### Main learning objectives

Students should be able to:

- interpret a matrix as a transformation;
- explain what linearity means;
- compute images of vectors under a matrix;
- predict transformations from columns of a matrix;
- identify scaling, reflection, projection, shear, and rotation matrices;
- understand why basis vectors determine a linear transformation.

### Content outline

1. **Motivation: matrices move vectors**

   - A 2-by-2 matrix takes 2D vectors to 2D vectors.
   - This is the foundation of graphics, rotations, projections, and coordinate
     changes.

2. **Function viewpoint**

   - `T(v)=A v`.
   - Input vector, output vector.

3. **Linearity**

   - `T(u+v)=T(u)+T(v)`.
   - `T(cu)=cT(u)`.
   - Linear transformations preserve the origin.

4. **Basis vector interpretation**

   - Columns of `A` show where standard basis vectors go.
   - Every vector is a combination of basis vectors.

5. **Common transformations**

   - Scaling.
   - Reflection.
   - Projection.
   - Shear.
   - Rotation, optional with simple angles.

6. **Worked examples**

   - Interpret `[[2,0],[0,2]]`.
   - Interpret `[[1,0],[0,0]]`.
   - Compute image of `[3,4]` under a matrix.
   - Use columns to describe transformation geometry.

7. **Practice exercises**

   - Matrix-vector images.
   - Identify transformations.
   - Check linearity from a rule.
   - Predict basis-vector images.

8. **Guessing game**

   - Topic key: `linear-transformations`.
   - Game: "What does this matrix do?" Guess scaling, projection, reflection,
     shear, or rotation.

9. **Using this lesson with edumath and SymPy**
   - Show `matrix_vector_product`.
   - Show transformation plotting helper if implemented.
   - Show SymPy exact matrix actions.

### Common pitfalls to address

- Confusing matrix entries with output coordinates directly.
- Forgetting that columns are images of basis vectors.
- Thinking every function is linear.
- Calling a translation linear even though it moves the origin.
- Mixing up projection and reflection.

## Lesson plan: `eigenvalues-eigenvectors.qmd`

### Purpose

Introduce eigenvalues and eigenvectors as special directions preserved by a
matrix transformation. Keep the lesson conceptual and computationally gentle.

### Main learning objectives

Students should be able to:

- explain eigenvectors as nonzero vectors whose direction is preserved;
- explain eigenvalues as scale factors;
- check whether a proposed vector is an eigenvector;
- find simple eigenpairs by inspection for diagonal or triangular matrices;
- compute characteristic polynomial for a 2-by-2 matrix at an introductory
  level;
- connect eigenvalues to repeated transformations and dynamic systems.

### Content outline

1. **Motivation: special directions**

   - Most vectors rotate or change direction under a matrix.
   - Eigenvectors stay on their own line.

2. **Definition**

   - `A v = lambda v`.
   - `v` must be nonzero.
   - `lambda` is a scalar.

3. **Geometric meaning**

   - Positive eigenvalue: stretch/shrink same direction.
   - Negative eigenvalue: flip direction.
   - Zero eigenvalue: collapse to zero vector.

4. **Checking an eigenpair**

   - Multiply `A v`.
   - Compare to `lambda v`.

5. **Diagonal matrices**

   - Eigenvalues appear on the diagonal.
   - Standard basis vectors are eigenvectors.

6. **Characteristic equation**

   - For small 2-by-2 matrices, eigenvalues solve `det(A - lambda I)=0`.
   - Keep algebra gentle.

7. **Repeated transformations**

   - If `A v = lambda v`, then `A^2 v = lambda^2 v`.
   - This explains long-run behavior.

8. **Worked examples**

   - Check `A v = 3v`.
   - Find eigenpairs for a diagonal matrix.
   - Compute eigenvalues of a simple 2-by-2 matrix.
   - Interpret a negative eigenvalue.

9. **Practice exercises**

   - Identify eigenvalue from `A v = lambda v`.
   - Check a proposed eigenvector.
   - Find eigenvalues of a diagonal matrix.
   - Explain why the zero vector is not called an eigenvector.

10. **Guessing game**

    - Topic key: `eigenvalues-eigenvectors`.
    - Game: "Eigenpair check." Given `A`, `v`, and candidates for `lambda`,
      guess whether the vector is an eigenvector and identify the eigenvalue.

11. **Using this lesson with edumath and SymPy**
    - Show `validate_eigenpair` if implemented.
    - Show NumPy `np.linalg.eig` for numeric eigenvalues.
    - Show SymPy `Matrix.eigenvals()` and `Matrix.eigenvects()` for exact
      examples.

### Common pitfalls to address

- Forgetting the eigenvector must be nonzero.
- Thinking every vector is an eigenvector.
- Confusing eigenvalue with determinant.
- Forgetting that negative eigenvalues reverse direction.
- Treating approximate numeric eigenvectors as exact without checking.

## Optional future lesson: `orthogonality-and-projections.qmd`

If the module needs additional depth later, add an orthogonality/projections
lesson after matrix operations or after transformations.

Possible topics:

- unit vectors;
- orthogonal and orthonormal vectors;
- projections;
- least squares intuition;
- Gram-Schmidt overview.

This would support statistics, optimization, and machine learning preparation.

## Suggested references for lesson authors

Use these as conceptual references while writing. Avoid copying text.

- Gilbert Strang, _Introduction to Linear Algebra_.
- David C. Lay, _Linear Algebra and Its Applications_.
- Jim Hefferon, _Linear Algebra_ (open text).
- 3Blue1Brown, _Essence of Linear Algebra_.
- MIT OpenCourseWare linear algebra materials.
- Khan Academy linear algebra refreshers for beginner explanations.

## Acceptance checklist

Before considering the plan implemented, verify the following.

### Content completeness

- [ ] `index.qmd` exists and is linked in `docs/_quarto.yml`.
- [ ] `docs/lessons/index.qmd` points to `linear-algebra/index.qmd`.
- [ ] Generated `.quarto_ipynb*` artifacts are removed or ignored.
- [ ] Every lesson has YAML front matter with title, description, and execution
      settings.
- [ ] Every lesson begins with motivation and learning objectives.
- [ ] Every lesson contains definitions, intuition, formulas or diagrams, and
      common pitfalls.
- [ ] Every lesson has at least two worked examples.
- [ ] Every lesson has practice exercises with answers or collapsed solutions.
- [ ] Every lesson has a topic-specific checkpoint or guessing game.
- [ ] Every lesson ends with `Using this lesson with edumath and SymPy`.
- [ ] Visible code appears primarily in the final appendix.

### Pedagogy

- [ ] Lessons are written for students with low confidence and limited prior
      exposure.
- [ ] Dimension and shape checks are explained before operations.
- [ ] Geometry and computation are connected throughout.
- [ ] Examples include both numeric calculation and interpretation.
- [ ] Common mistakes are explicitly named.
- [ ] Guessing games provide explanatory feedback.

### Package support

- [ ] Any new `edumath` helper has tests.
- [ ] Public API additions are exported intentionally.
- [ ] Existing public imports from `edumath.linear_algebra.concepts` remain
      compatible.
- [ ] Helpers are reusable across lessons.
- [ ] Heavy dependencies are not added without a clear project decision.

### Validation

- [ ] `poetry run pre-commit run --files <changed files>` passes.
- [ ] `poetry run pytest` passes if source files changed.
- [ ] `quarto render <changed qmd files> --no-execute` passes.
- [ ] Generated Quarto scratch/session files are removed before finishing.
