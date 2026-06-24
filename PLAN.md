# PLAN: Discrete Mathematics Lessons

Target directory: `docs/lessons/discrete-math/`

This plan describes how to rebuild the Discrete Mathematics lesson sequence into
a complete, beginner-friendly preparation module. The current pages are short
starter lessons. The goal is to write self-contained study material for learners
who may know algebra and basic programming but are new to proof, logic, sets,
relations, recurrence, induction, and graphs.

Discrete mathematics should feel concrete before it feels formal. Each lesson
should connect symbols to everyday examples, computation, proof habits, and
small interactive checkpoints.

## Current lesson files

Current pages in `docs/lessons/discrete-math/`:

1. `logic.qmd`
2. `sets.qmd`
3. `functions-relations.qmd`
4. `sequences.qmd`
5. `induction.qmd`
6. `graphs.qmd`

Also present during inspection:

- `logic.quarto_ipynb`
- `sets.quarto_ipynb`

These appear to be generated Quarto notebook artifacts rather than the intended
source pages. Before implementation, verify whether they are tracked. If they
are untracked/generated, remove them from the working tree. The lesson source
should remain `.qmd` files.

Recommended addition:

7. `index.qmd` — Discrete Mathematics study path overview and readiness
   checklist.

Update `docs/_quarto.yml` so the Discrete Mathematics sidebar starts with the
new index page if `index.qmd` is added. Update `docs/lessons/index.qmd` so the
Discrete Mathematics card links to `discrete-math/index.qmd` instead of the
first content page.

## Overall pedagogical goals

The Discrete Mathematics module should help students move from calculation to
precise reasoning.

By the end of the path, a student should be able to say:

> Discrete mathematics studies objects that are separate or countable: truth
> values, sets, relations, sequences, proofs, and networks. I can use precise
> definitions, examples, counterexamples, and simple algorithms to reason about
> finite and countable structures.

Students should repeatedly practice these habits:

- State exactly what the objects are.
- Check definitions before guessing.
- Use examples to understand a pattern.
- Use counterexamples to disprove false claims.
- Translate between words, symbols, tables, diagrams, and code.
- Explain why an answer is true, not only what the answer is.
- Distinguish a statement, its converse, its inverse, and its contrapositive.
- Check whether a rule is a function, a relation, an equivalence relation, or a
  graph property.

## Prerequisites to reinforce throughout

The lessons should review prerequisite ideas in context instead of assuming
students remember everything perfectly:

- basic algebraic notation;
- function notation;
- ordered pairs;
- simple equations and inequalities;
- exponents and sums;
- reading tables;
- basic Python lists, sets, dictionaries, loops, and conditionals;
- careful English reading;
- basic proof vocabulary such as assume, therefore, and contradiction.

Whenever a prerequisite appears, include a short reminder box. For example, in
induction, remind students that `k+1` means "the next integer after `k`," not a
separate unrelated variable.

## Global lesson standards

Each Discrete Mathematics lesson should follow the repository lesson standards.

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

   Use visible code blocks with `#| echo: true` in this final section.

Do not call these pages notebooks in navigation or lesson prose unless a page is
specifically about notebook usage.

## Code visibility guidelines

In the main lesson body:

- hide helper code with `execute: echo: false`;
- show tables, diagrams, truth tables, set calculations, graphs, and
  conclusions;
- avoid raw setup code unless the code itself is the teaching target.

In the final `Using this lesson with edumath and SymPy` appendix:

- show visible Python examples with `#| echo: true`;
- use `edumath.discrete_math` helpers when available;
- use SymPy for logic simplification, set notation, summations, recurrence
  checking, and symbolic verification when appropriate;
- use Python standard-library examples when they are clearer than SymPy.

SymPy is useful for symbolic logic, sets, summations, and recurrence checking,
but it is not a replacement for learning definitions and proof structure.

## Shared interaction plan

Create a reusable static checkpoint include:

```text
docs/lessons/discrete-math/_includes/discrete-math-checkpoint.qmd
```

The include should use browser-native JavaScript, similar to the Algebra,
Calculus, and Differential Equations checkpoint patterns, so published HTML
remains interactive without a live Python kernel.

Potential topic keys:

- `logic`
- `sets`
- `functions-relations`
- `sequences`
- `induction`
- `graphs`
- `discrete-math-cumulative-review`

The include should support flexible question types:

- multiple choice;
- true/false;
- match a definition to an example;
- choose a counterexample;
- guess the next sequence term;
- classify a relation property;
- identify a graph property;
- choose the correct induction step;
- evaluate a small truth table row.

Use one JSON configuration block per lesson, for example:

```html
<script type="application/json" class="edu-math-discrete-checkpoint-config">
  {
    "topic": "logic",
    "title": "Logic checkpoint",
    "defaultTotal": 4
  }
</script>
```

Then include the shared fragment:

```qmd
{{< include _includes/discrete-math-checkpoint.qmd >}}
```

### Checkpoint game principles

Each guessing game should teach the lesson topic, not merely decorate the page.
Good discrete-math guessing games include:

- guess the truth value of a compound proposition;
- choose the row that makes an implication false;
- guess a set union, intersection, complement, or difference;
- classify a relation as reflexive, symmetric, transitive, function, or not;
- guess the next term or closed form of a sequence;
- choose the missing line in an induction proof;
- classify a graph by degree, path, cycle, connectedness, or directedness;
- choose a counterexample to a false statement.

Feedback should be explanatory and friendly. It should say why the answer is
correct or why a common wrong answer is tempting.

## Online computation options

The main computational appendix should use Python and SymPy where helpful.
Discrete mathematics also benefits from lightweight browser-side tools.

Potential online libraries and tools:

- **PyScript/Pyodide + SymPy**: lets students run Python and SymPy in the
  browser. Good for truth tables, sets, summations, recurrence checks, and graph
  algorithms on small examples.
- **Math.js**: useful for evaluating numeric expressions, simple Boolean
  expressions, and sequence rules in browser activities.
- **Nerdamer**: useful for symbolic algebra and recurrence/summation checking in
  simple browser exercises.
- **Algebrite**: useful for lightweight symbolic manipulation.
- **Cytoscape.js**: useful for future interactive graph visualizations.
- **D3.js**: useful for custom set diagrams, graph diagrams, and interactive
  finite structures.

Do not add heavy JavaScript dependencies automatically. Prefer static
browser-native JavaScript for checkpoints. Propose PyScript or graph libraries
only for optional future enhancements.

## Proposed `edumath` package support

The current package contains `src/edumath/discrete_math/`, but most modules are
empty except `logic.py`, which includes `truth_table` and `implies`. Add small,
reusable helpers only when they directly improve pedagogy.

### `src/edumath/discrete_math/concepts.py`

Add concept metadata similar to other branches:

- `LOGIC`
- `SETS`
- `FUNCTIONS_RELATIONS`
- `SEQUENCES`
- `INDUCTION`
- `GRAPHS`
- `DISCRETE_MATH_PATH`

Each concept should include:

- title;
- slug;
- short description;
- prerequisites;
- measurable learning goals;
- common mistakes or tags.

Expected path order:

```text
logic -> sets -> functions-relations -> sequences -> induction -> graphs
```

### `src/edumath/discrete_math/logic.py`

Keep existing helpers and consider adding:

- `not_`, `and_`, `or_`, `xor`, `iff`;
- `contrapositive_truth_table()` or a generic expression truth-table helper;
- `truth_table_rows(variables, expression)` for simple expression strings;
- `is_tautology(rows)`;
- `is_contradiction(rows)`;
- `is_equivalent(function_a, function_b, variables)`.

Keep names clear and avoid overriding Python keywords directly. For example, use
`and_` instead of `and`.

### `src/edumath/discrete_math/sets.py` or `exercises.py`

There is no `sets.py` currently. Consider either adding a small `sets.py` module
or keeping set helpers in `exercises.py` and `validators.py`.

Potential helpers:

- `set_operation_table(a, b)` returning union, intersection, difference, and
  symmetric difference;
- `venn_region_counts(a, b, universe=None)`;
- `power_set(iterable)` for small sets;
- `cartesian_product(a, b)`;
- `is_subset_answer(received, expected)` validator.

### `src/edumath/discrete_math/exercises.py`

Add deterministic exercise builders:

- `truth_table_exercise(seed=...)`;
- `set_operation_exercise(seed=...)`;
- `relation_classification_exercise(seed=...)`;
- `sequence_next_term_exercise(seed=...)`;
- `induction_step_exercise(seed=...)`;
- `graph_degree_exercise(seed=...)`.

Each exercise should include prompt, expected answer, hints, explanation, tags,
and validators where useful.

### `src/edumath/discrete_math/validators.py`

Add small checkers:

- `validate_truth_value(received, expected)`;
- `validate_set_answer(received, expected)`;
- `validate_ordered_pairs(received, expected)`;
- `validate_sequence_terms(received, expected, tolerance=...)`;
- `validate_relation_properties(received, expected)`;
- `validate_graph_degree_sequence(received, expected)`.

Validators should accept natural student formats when practical, such as Python
sets, lists, tuples, and simple comma-separated strings.

### `src/edumath/discrete_math/plots.py`

Add lightweight plotting or scene helpers:

- `venn_two_set_scene(a, b, universe=None)` or a simple data structure for Venn
  diagrams;
- `relation_arrow_scene(domain, codomain, pairs)`;
- `sequence_points_scene(terms)`;
- `finite_graph_scene(vertices, edges, directed=False)`.

Prefer small reusable scene data and Matplotlib drawings. Do not add NetworkX as
a dependency unless a clear need is established. If NetworkX-like functionality
is useful, implement tiny finite-graph helpers for lesson examples first.

### `src/edumath/discrete_math/quizzes.py`

Add quiz-question builders:

- truth table row question;
- implication false-case question;
- set operation question;
- relation/function classification question;
- sequence pattern question;
- induction proof structure question;
- graph degree/path question;
- cumulative discrete-math diagnostic quiz.

### Optional `src/edumath/discrete_math/relations.py`

If relation logic becomes substantial, add a dedicated module with:

- `is_function(pairs)`;
- `domain(pairs)`;
- `range_(pairs)`;
- `is_reflexive(pairs, universe)`;
- `is_symmetric(pairs)`;
- `is_transitive(pairs)`;
- `compose_relations(r, s)`.

### Optional `src/edumath/discrete_math/graphs.py`

If graph helpers become substantial, add a dedicated module with:

- `degree(vertices, edges, vertex)`;
- `degree_sequence(vertices, edges)`;
- `neighbors(vertices, edges, vertex)`;
- `is_path(vertices, edges, walk)`;
- `is_connected(vertices, edges)` for tiny undirected graphs;
- `has_cycle(vertices, edges)` for tiny examples.

Keep APIs intentionally small and testable.

### Tests

Add `tests/test_discrete_math_helpers.py` covering:

- existing and new logic helpers;
- deterministic exercise generation;
- validators accepting correct and rejecting incorrect answers;
- concept path slugs;
- relation classification helpers if added;
- graph degree/path helpers if added;
- plotting scene render or scene-data shape;
- quiz builder structure.

Run the full test suite if any shared helpers are changed.

## Documentation implementation phases

### Phase 1 — Planning and structure

1. Replace `PLAN.md` with this plan.
2. Inspect all current discrete-math pages and source helpers.
3. Decide whether to add `index.qmd` immediately.
4. Remove generated `.quarto_ipynb*` artifacts if they are untracked.
5. Create the shared checkpoint include.
6. Add sidebar entry for the new index page if created.
7. Update the Discrete Mathematics card in `docs/lessons/index.qmd`.

### Phase 2 — Source helper additions

1. Implement only `edumath` helpers needed by the lesson content.
2. Export the small public API from `src/edumath/discrete_math/__init__.py`.
3. Add tests before relying on helpers in docs.
4. Run:

   ```bash
   poetry run pytest tests/test_discrete_math_helpers.py
   ```

5. Run broader tests if helpers touch shared modules:

   ```bash
   poetry run pytest
   ```

### Phase 3 — Lesson writing

Write the lessons in this order:

1. `index.qmd`
2. `logic.qmd`
3. `sets.qmd`
4. `functions-relations.qmd`
5. `sequences.qmd`
6. `induction.qmd`
7. `graphs.qmd`

This order builds from truth values, to collections, to mappings, to ordered
patterns, to proof, to network structures.

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

Create a friendly overview page that explains what discrete mathematics is, why
it matters, and how the lesson sequence fits together.

### Front matter

```yaml
---
title: Discrete Mathematics Study Path
description:
  A guided path through logic, sets, relations, sequences, proofs, and graphs.
execute:
  echo: false
---
```

### Content outline

1. **Opening intuition**

   - Continuous math studies smooth change.
   - Discrete math studies separate objects: truth values, elements, pairs,
     integers, steps, and nodes.
   - It supports computer science, algorithms, data structures, databases,
     proofs, networks, and probability.

2. **What makes discrete math different**

   - Definitions matter more than long formulas.
   - Counterexamples are powerful.
   - Many questions are yes/no or classification questions.
   - Proof and algorithmic thinking appear often.

3. **Prerequisite checklist**

   - basic algebra;
   - functions;
   - tables;
   - simple Python;
   - careful reading;
   - willingness to explain reasoning.

4. **The study path**

   - logic: truth and implication;
   - sets: membership and operations;
   - functions and relations: pairs and structure;
   - sequences: ordered patterns and recursion;
   - induction: proof over infinitely many integers;
   - graphs: vertices, edges, paths, and networks.

5. **How to study**

   - write definitions in your own words;
   - make tiny examples;
   - search for counterexamples;
   - draw diagrams;
   - check with code;
   - explain why, not only what.

6. **Readiness checkpoint game**

   - topic key `discrete-math-cumulative-review`;
   - ask students to classify prompts as logic, set, relation, sequence,
     induction, or graph ideas.

7. **Using this lesson with edumath and SymPy**
   - show `truth_table` and `implies`;
   - show Python set operations;
   - show SymPy logic simplification or symbolic summation;
   - explain that code checks examples but does not replace proof.

### Practice ideas

- Identify which discrete-math topic best fits a scenario.
- Decide whether a statement is true, false, or not precise enough.
- Give a tiny example of a set, relation, sequence, and graph.

## Lesson plan: `logic.qmd`

### Purpose

Teach propositions, truth values, logical connectives, implication, equivalence,
and truth tables as foundations for proof and programming.

### Main learning objectives

Students should be able to:

- identify propositions;
- use `not`, `and`, `or`, implication, and biconditional;
- build and read truth tables;
- identify when `p -> q` is false;
- distinguish converse and contrapositive;
- recognize tautologies and contradictions;
- connect logic to if-statements and proof structure.

### Content outline

1. **Motivation: precision in statements**

   - A proposition is a statement that is true or false.
   - Questions, commands, and vague sentences are not propositions.

2. **Truth values**

   - Define true and false.
   - Use examples from math and everyday language.

3. **Connectives**

   - `not p`;
   - `p and q`;
   - `p or q` inclusive meaning;
   - `p -> q` implication;
   - `p <-> q` if and only if.

4. **Implication carefully**

   - `p -> q` is false only when `p` is true and `q` is false.
   - Explain why this feels strange at first.
   - Connect to promises: if the condition happens, the result must happen.

5. **Truth tables**

   - Show how to list all combinations.
   - Work through `p -> q`.
   - Work through `(p -> q) <-> (~q -> ~p)` to show contrapositive equivalence.

6. **Converse, inverse, contrapositive**

   - Statement: `p -> q`.
   - Converse: `q -> p`.
   - Inverse: `~p -> ~q`.
   - Contrapositive: `~q -> ~p`.

7. **Tautology and contradiction**

   - Tautology always true.
   - Contradiction always false.

8. **Worked examples**

   - Build a truth table for `p and not q`.
   - Decide whether a conditional and its converse are equivalent.
   - Translate a programming `if` statement into implication language.

9. **Practice exercises**

   - Identify propositions.
   - Complete truth table rows.
   - Find when an implication is false.
   - Write converse and contrapositive.

10. **Guessing game**

    - Topic key: `logic`.
    - Game: "Truth value challenge." Given truth values for `p` and `q`, guess
      the truth value of a compound statement.

11. **Using this lesson with edumath and SymPy**
    - Show `truth_table(("p", "q"), implies)`.
    - Show SymPy Boolean expressions with `Implies`, `Equivalent`, `And`, `Or`,
      `Not`.
    - Show how to check a tautology.

### Common pitfalls to address

- Treating `or` as exclusive when math usually uses inclusive `or`.
- Thinking an implication is false whenever the conclusion is false.
- Confusing converse with contrapositive.
- Forgetting to include all truth-value combinations in a truth table.
- Calling vague sentences propositions.

## Lesson plan: `sets.qmd`

### Purpose

Teach sets as collections of distinct objects, including membership, subsets,
common operations, complements, Cartesian products, and Venn-diagram reasoning.

### Main learning objectives

Students should be able to:

- define membership and non-membership;
- distinguish an element from a subset;
- compute union, intersection, difference, complement, and symmetric difference;
- determine whether one set is a subset of another;
- list a small power set;
- compute a Cartesian product;
- connect sets to probability events and database filters.

### Content outline

1. **Motivation: collections without duplicates**

   - A set is a collection where order and repetition do not matter.
   - `{1,2,3}` is the same set as `{3,2,1}`.

2. **Membership and notation**

   - `x in A`;
   - `x notin A`;
   - roster notation;
   - set-builder notation in beginner-friendly form.

3. **Subsets**

   - `A subset B` means every element of `A` is in `B`.
   - Distinguish `2 in A` from `{2} subset A`.

4. **Operations**

   - union;
   - intersection;
   - difference;
   - complement relative to a universe;
   - symmetric difference.

5. **Power sets**

   - A power set is the set of all subsets.
   - For a set with `n` elements, the power set has `2^n` subsets.

6. **Cartesian products**

   - Ordered pairs from two sets.
   - `A x B` differs from `B x A`.

7. **Venn diagram intuition**

   - Use regions: only A, only B, both, neither.

8. **Worked examples**

   - Compute operations for `A={1,2,3}` and `B={3,4}`.
   - List the power set of `{a,b}`.
   - Compute `{1,2} x {x,y}`.

9. **Practice exercises**

   - Determine membership/subset truth values.
   - Compute set operations.
   - Draw or describe Venn regions.
   - Count power-set elements.

10. **Guessing game**

    - Topic key: `sets`.
    - Game: "Set operation guesser." Given two small sets, guess union,
      intersection, difference, or Cartesian product.

11. **Using this lesson with edumath and SymPy**
    - Show Python set operators: `|`, `&`, `-`, `^`.
    - Show SymPy `FiniteSet` operations.
    - Show optional `edumath` set helpers if implemented.

### Common pitfalls to address

- Confusing element and subset notation.
- Forgetting that sets ignore repeated elements.
- Thinking `A-B` equals `B-A`.
- Forgetting the universe when computing complements.
- Confusing Cartesian product ordered pairs with ordinary multiplication.

## Lesson plan: `functions-relations.qmd`

### Purpose

Teach relations as sets of ordered pairs and functions as special relations.
Introduce domain, codomain, range, inverse relations, composition, and relation
properties.

### Main learning objectives

Students should be able to:

- define a relation as a set of ordered pairs;
- identify domain, codomain, and range;
- decide whether a relation is a function;
- explain why each input can have only one output in a function;
- classify simple relations as reflexive, symmetric, antisymmetric, or
  transitive;
- recognize equivalence relation basics;
- compose small relations or functions.

### Content outline

1. **Motivation: structured pairs**

   - Relations describe connections: person-to-course, number-to-square,
     city-to-road, input-to-output.

2. **Ordered pairs**

   - `(a,b)` is not the same as `(b,a)` unless `a=b`.
   - The first coordinate often represents input.

3. **Relations**

   - A relation from `A` to `B` is a subset of `A x B`.
   - Examples with small finite sets.

4. **Functions**

   - A function assigns each input exactly one output.
   - A relation can fail by missing an input or giving an input two outputs,
     depending on the stated domain.

5. **Domain, codomain, range**

   - Domain: allowed inputs.
   - Codomain: allowed target outputs.
   - Range/image: outputs actually used.

6. **Relation properties**

   - Reflexive: every element relates to itself.
   - Symmetric: if `aRb`, then `bRa`.
   - Antisymmetric: if both directions happen, then the elements are equal.
   - Transitive: if `aRb` and `bRc`, then `aRc`.

7. **Equivalence relations**

   - Reflexive + symmetric + transitive.
   - Example: same remainder modulo `n`.

8. **Worked examples**

   - Decide whether `{(1,2),(1,3)}` is a function.
   - Find domain and range of a finite relation.
   - Classify equality or divisibility on a small set.

9. **Practice exercises**

   - Function or not?
   - Domain/range identification.
   - Relation property classification.
   - Give a counterexample for transitivity.

10. **Guessing game**

    - Topic key: `functions-relations`.
    - Game: "Function or relation?" Given pairs, guess whether it is a function
      and explain which input causes trouble if not.

11. **Using this lesson with edumath and SymPy**
    - Use Python tuples and sets to represent relations.
    - Use `edumath` relation helpers if implemented.
    - Use SymPy or Python to test small relation properties by exhaustive
      checking.

### Common pitfalls to address

- Forgetting ordered pairs have order.
- Saying a relation is not a function because two inputs share an output.
- Confusing codomain and range.
- Checking relation properties on only one example pair.
- Assuming symmetric and antisymmetric are opposites; they are not.

## Lesson plan: `sequences.qmd`

### Purpose

Teach sequences as ordered lists generated by explicit or recursive rules.
Connect arithmetic and geometric sequences to functions on integers, summations,
recurrence, and algorithmic thinking.

### Main learning objectives

Students should be able to:

- define a sequence as a function from integers to values;
- compute terms from explicit formulas;
- compute terms from recursive definitions;
- recognize arithmetic and geometric sequences;
- write simple closed forms;
- compute finite sums;
- connect recurrence to loops and repeated processes.

### Content outline

1. **Motivation: patterns with positions**

   - A sequence is not just a set because order matters.
   - `2, 4, 8` differs from `8, 4, 2`.

2. **Notation**

   - `a_n` means the term at position `n`.
   - Clarify whether indexing starts at `0` or `1`.

3. **Explicit rules**

   - Formula directly gives `a_n`.
   - Example: `a_n = 3n + 2`.

4. **Recursive rules**

   - Rule gives next term from previous term(s).
   - Example: `a_1=2`, `a_{n+1}=a_n+3`.

5. **Arithmetic sequences**

   - Add a common difference.
   - Closed form `a_n = a_1 + (n-1)d`.

6. **Geometric sequences**

   - Multiply by a common ratio.
   - Closed form `a_n = a_1 r^{n-1}`.

7. **Finite sums**

   - Sigma notation.
   - Arithmetic and geometric sum intuition.

8. **Worked examples**

   - Find next terms.
   - Convert a recursive arithmetic rule to closed form.
   - Compute a small finite sum.
   - Interpret repeated percentage growth as geometric.

9. **Practice exercises**

   - Identify arithmetic, geometric, or neither.
   - Compute terms from explicit and recursive rules.
   - Write a recurrence for a word problem.
   - Evaluate a finite sum.

10. **Guessing game**

    - Topic key: `sequences`.
    - Game: "Next term or rule?" Given a sequence, guess the next term and
      classify the pattern.

11. **Using this lesson with edumath and SymPy**
    - Use Python list comprehensions for terms.
    - Use SymPy `summation` for finite sums.
    - Use `edumath` sequence exercise helpers if implemented.

### Common pitfalls to address

- Confusing term value with term number.
- Assuming every sequence starts at `n=1`.
- Treating an unordered set as a sequence.
- Using an arithmetic formula for a geometric sequence.
- Forgetting the initial condition in a recurrence.

## Lesson plan: `induction.qmd`

### Purpose

Teach mathematical induction as a proof technique for statements indexed by
integers. Emphasize the structure and meaning of the proof before algebraic
complexity.

### Main learning objectives

Students should be able to:

- identify statements suitable for induction;
- write a base case;
- state an induction hypothesis;
- prove an induction step;
- explain the chain-of-dominoes intuition;
- use induction for sums, divisibility, and inequalities;
- recognize common proof gaps.

### Content outline

1. **Motivation: infinitely many checks**

   - You cannot verify every positive integer one at a time.
   - Induction proves the first case and the rule that truth passes forward.

2. **Domino intuition**

   - Base case knocks over the first domino.
   - Induction step proves each domino knocks over the next.

3. **Proof structure**

   - State the proposition `P(n)`.
   - Base case.
   - Induction hypothesis: assume `P(k)`.
   - Induction step: prove `P(k+1)`.
   - Conclusion.

4. **Worked example 1: sum formula**

   - Prove `1+2+...+n = n(n+1)/2`.
   - Show exactly where the induction hypothesis is used.

5. **Worked example 2: divisibility**

   - Prove a simple statement such as `3` divides `4^n-1` for `n>=1`.

6. **Worked example 3: inequality or sequence**

   - Keep algebra gentle.
   - Focus on proof logic.

7. **Common proof templates**

   - Sum statements.
   - Divisibility statements.
   - Recursive sequence statements.

8. **Practice exercises**

   - Identify `P(n)`.
   - Fill a missing base case.
   - Identify the induction hypothesis.
   - Complete a small induction step.
   - Find the flaw in a bad induction proof.

9. **Guessing game**

   - Topic key: `induction`.
   - Game: "Missing proof step." Students choose the correct induction
     hypothesis or the next algebraic line.

10. **Using this lesson with edumath and SymPy**
    - Use SymPy to verify the first several cases of a formula.
    - Use SymPy simplification to check algebra in the induction step.
    - Explain that checking examples is not a proof, but it builds confidence.

### Common pitfalls to address

- Proving only examples and calling it induction.
- Forgetting the base case.
- Assuming what must be proved for `k+1`.
- Not using the induction hypothesis.
- Confusing `k` and `k+1`.
- Writing algebra without explaining the logical structure.

## Lesson plan: `graphs.qmd`

### Purpose

Introduce graph theory as the study of vertices and edges. Teach terminology,
small graph properties, paths, cycles, degrees, connectedness, directed graphs,
and real network models.

### Main learning objectives

Students should be able to:

- define vertices and edges;
- distinguish directed and undirected graphs;
- compute vertex degrees;
- identify paths, walks, trails, and cycles at an introductory level;
- determine whether a small graph is connected;
- represent a graph with an edge list or adjacency list;
- connect graph models to real-world networks.

### Content outline

1. **Motivation: networks everywhere**

   - roads between cities;
   - friendships;
   - web links;
   - prerequisites;
   - computer networks;
   - dependency graphs.

2. **Definitions**

   - Vertex/node.
   - Edge/link.
   - Directed vs undirected.
   - Simple graph vs graph with loops or repeated edges.

3. **Representations**

   - Drawing.
   - Edge list.
   - Adjacency list.
   - Adjacency matrix, optional and gentle.

4. **Degree**

   - Number of incident edges in an undirected graph.
   - In-degree and out-degree for directed graphs.

5. **Walks, paths, trails, cycles**

   - Keep definitions beginner-friendly.
   - Emphasize repeated vertices/edges differences.

6. **Connectedness**

   - A graph is connected if every vertex can be reached from every other
     vertex.

7. **Worked examples**

   - Compute degrees from an edge list.
   - Decide whether a graph is connected.
   - Identify a path and a cycle.
   - Translate a small real scenario into a graph.

8. **Practice exercises**

   - Count vertices and edges.
   - Compute degrees.
   - Find neighbors.
   - Decide whether a proposed walk is a path.
   - Determine connectedness.

9. **Guessing game**

   - Topic key: `graphs`.
   - Game: "Graph property challenge." Given a tiny edge list, guess degree,
     connectedness, whether a sequence is a path, or whether a cycle exists.

10. **Using this lesson with edumath and SymPy**
    - Use Python dictionaries or sets for adjacency lists.
    - Use `edumath` graph helpers if implemented.
    - Mention that NetworkX is a powerful external graph library, but avoid
      adding it as a dependency unless the project chooses to support advanced
      graph work.

### Common pitfalls to address

- Confusing a graph of a function with a graph theory network.
- Counting directed edges as if they were undirected.
- Double-counting edges when computing degree.
- Thinking a path can repeat vertices.
- Forgetting isolated vertices when checking connectedness.

## Optional future lesson: `counting-and-combinatorics.qmd`

The current site has probability lessons that include counting. If the Discrete
Mathematics module later needs a dedicated counting lesson, add it after sets or
sequences.

Possible topics:

- product rule;
- sum rule;
- permutations;
- combinations;
- binomial coefficients;
- pigeonhole principle;
- inclusion-exclusion.

This would support probability, algorithms, and graph counting.

## Suggested references for lesson authors

Use these as conceptual references while writing. Avoid copying text.

- Oscar Levin, _Discrete Mathematics: An Open Introduction_.
- Kenneth Rosen, _Discrete Mathematics and Its Applications_.
- Susanna Epp, _Discrete Mathematics with Applications_.
- MIT OpenCourseWare discrete mathematics materials.
- OpenStax or other open resources for logic, sets, and proof foundations.

## Acceptance checklist

Before considering the plan implemented, verify the following.

### Content completeness

- [ ] `index.qmd` exists and is linked in `docs/_quarto.yml`.
- [ ] `docs/lessons/index.qmd` points to `discrete-math/index.qmd`.
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
- [ ] Definitions are explained with examples and nonexamples.
- [ ] Proof-related lessons explain logic before algebra.
- [ ] Counterexamples are used to disprove false claims.
- [ ] Common mistakes are explicitly named.
- [ ] Guessing games provide explanatory feedback.

### Package support

- [ ] Any new `edumath` helper has tests.
- [ ] Public API additions are exported intentionally.
- [ ] Helpers are reusable across lessons.
- [ ] Heavy dependencies such as NetworkX or D3 are not added without a clear
      project decision.

### Validation

- [ ] `poetry run pre-commit run --files <changed files>` passes.
- [ ] `poetry run pytest` passes if source files changed.
- [ ] `quarto render <changed qmd files> --no-execute` passes.
- [ ] Generated Quarto scratch/session files are removed before finishing.
