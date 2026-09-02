(() => {
  "use strict";

  const TYPES = new Set([
    "single-choice",
    "multiple-select",
    "numeric",
    "symbolic",
    "solution-set",
    "interval",
    "python-output",
  ]);

  class FreeCampusQuiz extends HTMLElement {
    constructor() {
      super();
      this.bank = null;
      this.index = 0;
      this.results = new Map();
    }

    async connectedCallback() {
      if (this.dataset.ready) return;
      this.dataset.ready = "true";
      this.setAttribute("aria-busy", "true");
      try {
        const response = await fetch(
          new URL(this.dataset.source, document.baseURI),
        );
        if (!response.ok)
          throw new Error(`Quiz data returned ${response.status}.`);
        const bank = await response.json();
        this.validateBank(bank);
        this.bank = bank;
        this.render();
      } catch (error) {
        this.innerHTML = `<div class="callout callout-warning"><p>The interactive quiz could not load. ${escapeHtml(
          error.message,
        )}</p></div>`;
      } finally {
        this.removeAttribute("aria-busy");
      }
    }

    validateBank(bank) {
      if (
        bank?.schema_version !== 1 ||
        !bank.id ||
        !Array.isArray(bank.questions)
      ) {
        throw new Error("The quiz data does not match schema version 1.");
      }
      const ids = new Set();
      bank.questions.forEach((question) => {
        if (!question.id || ids.has(question.id) || !TYPES.has(question.type)) {
          throw new Error(
            "The quiz contains an invalid or duplicate question.",
          );
        }
        if (
          !question.prompt ||
          !question.explanation ||
          !question.outcome_id ||
          !question.validation?.mode
        ) {
          throw new Error(
            `Question ${question.id} is missing required learning metadata.`,
          );
        }
        ids.add(question.id);
      });
    }

    render() {
      const question = this.bank.questions[this.index];
      const prior = this.results.get(question.id);
      this.innerHTML = `
        <section class="fc-quiz" aria-labelledby="fc-quiz-title-${cssId(
          this.bank.id,
        )}">
          <header>
            <p class="quiz-eyebrow">${escapeHtml(
              this.bank.purpose.replaceAll("-", " "),
            )}</p>
            <h2 id="fc-quiz-title-${cssId(this.bank.id)}">${escapeHtml(
              this.bank.title,
            )}</h2>
            <p><strong>Question ${this.index + 1} of ${
              this.bank.questions.length
            }</strong></p>
            <progress max="${this.bank.questions.length}" value="${
              this.index + 1
            }">${this.index + 1}/${this.bank.questions.length}</progress>
          </header>
          <form novalidate>
            <fieldset>
              <legend>${question.prompt}</legend>
              ${this.answerMarkup(question)}
            </fieldset>
            ${
              question.hint
                ? `<details class="quiz-hint"><summary>Hint</summary><p>${question.hint}</p></details>`
                : ""
            }
            <div class="quiz-controls">
              <button type="submit" class="btn btn-primary">Check answer</button>
              <button type="button" class="btn btn-secondary" data-move="-1" ${
                this.index === 0 ? "disabled" : ""
              }>Previous</button>
              <button type="button" class="btn btn-secondary" data-move="1" ${
                this.index === this.bank.questions.length - 1 ? "disabled" : ""
              }>Next</button>
              <button type="button" class="btn btn-link" data-reset>Reset quiz</button>
            </div>
          </form>
          <div class="quiz-feedback" role="status" aria-live="polite">${
            prior ? this.feedbackMarkup(prior, question) : ""
          }</div>
          <p class="quiz-score">Answered ${this.results.size} of ${
            this.bank.questions.length
          }; correct ${
            [...this.results.values()].filter((result) => result.correct).length
          }.</p>
        </section>`;
      this.querySelector("form").addEventListener("submit", (event) =>
        this.check(event, question),
      );
      this.querySelectorAll("[data-move]").forEach((button) =>
        button.addEventListener("click", () => {
          this.index += Number(button.dataset.move);
          this.render();
        }),
      );
      this.querySelector("[data-reset]").addEventListener("click", () => {
        this.index = 0;
        this.results.clear();
        this.render();
      });
      if (window.MathJax?.typesetPromise) window.MathJax.typesetPromise([this]);
    }

    answerMarkup(question) {
      if (question.options) {
        const inputType =
          question.type === "multiple-select" ? "checkbox" : "radio";
        return `<div class="quiz-options">${question.options
          .map(
            (option) => `
          <label><input type="${inputType}" name="answer" value="${escapeHtml(
            option.id,
          )}"> <span>${option.text}</span></label>`,
          )
          .join("")}
          <label><input type="${inputType}" name="answer" value="__not_sure__"> <span>I am not sure yet</span></label>
        </div>`;
      }
      const instructions =
        question.type === "symbolic"
          ? "Use * for multiplication and ^ for powers; for example, 3*x^2."
          : "Enter one answer.";
      return `<label class="quiz-text-answer"><span>${instructions}</span><input name="answer" type="text" autocomplete="off" maxlength="256" required></label>`;
    }

    check(event, question) {
      event.preventDefault();
      const form = event.currentTarget;
      const selected = [
        ...form.querySelectorAll('input[name="answer"]:checked'),
      ].map((input) => input.value);
      let received;
      if (question.options)
        received = question.type === "multiple-select" ? selected : selected[0];
      else received = form.elements.answer.value;
      if (
        received === undefined ||
        received === "" ||
        (Array.isArray(received) && !received.length)
      ) {
        this.querySelector(".quiz-feedback").textContent =
          "Choose or enter an answer first.";
        return;
      }
      const result = this.validate(question, received);
      this.results.set(question.id, result);
      this.render();
      if (this.results.size === this.bank.questions.length) {
        this.dispatchEvent(
          new CustomEvent("fcmath:quiz-complete", {
            bubbles: true,
            detail: {
              id: this.bank.id,
              correct: [...this.results.values()].filter((item) => item.correct)
                .length,
              total: this.results.size,
            },
          }),
        );
      }
    }

    validate(question, received) {
      if (
        received === "__not_sure__" ||
        (Array.isArray(received) && received.includes("__not_sure__"))
      ) {
        return {
          correct: false,
          message:
            "Use the explanation to identify the earliest idea to review.",
        };
      }
      const mode = question.validation.mode;
      if (mode === "exact" || mode === "normalized-output") {
        const normalize = (value) => String(value).trim().replace(/\s+/g, " ");
        return {
          correct: normalize(received) === normalize(question.answer),
          message: "",
        };
      }
      if (mode === "set-equality") {
        const left = new Set(received);
        const right = new Set(question.answer);
        return {
          correct:
            left.size === right.size &&
            [...left].every((value) => right.has(value)),
          message: "",
        };
      }
      if (mode === "numeric") {
        try {
          const value = safeNumeric(stripUnits(received, question.validation));
          const expected = safeNumeric(question.answer);
          const absolute = Number(question.validation.absolute_tolerance);
          const relative = Number(question.validation.relative_tolerance);
          const scale = Math.max(Math.abs(value), Math.abs(expected), 1);
          return {
            correct:
              Math.abs(value - expected) <=
              Math.max(absolute, relative * scale),
            message: "",
          };
        } catch (error) {
          return { correct: false, message: error.message };
        }
      }
      if (mode === "symbolic-equivalence") {
        try {
          const variables =
            question.variables ||
            (question.variable ? [question.variable] : []);
          const equivalent = symbolicEquivalent(
            received,
            question.answer,
            variables,
          );
          const correct =
            equivalent &&
            requestedForm(
              received,
              question.validation.algebraic_form || "any",
              variables,
            );
          const message =
            equivalent && !correct
              ? `The expression is equivalent, but it is not in the requested ${question.validation.algebraic_form} form.`
              : "";
          return { correct, message };
        } catch (error) {
          return { correct: false, message: error.message };
        }
      }
      if (mode === "solution-set" || mode === "interval") {
        try {
          const variables =
            question.variables ||
            (question.variable ? [question.variable] : []);
          return {
            correct: solutionSetEquivalent(
              received,
              question.answer,
              variables,
            ),
            message: "",
          };
        } catch (error) {
          return { correct: false, message: error.message };
        }
      }
      return {
        correct: false,
        message: "Use the notebook version for this answer type.",
      };
    }

    feedbackMarkup(result, question) {
      const heading = result.correct ? "Correct." : "Not yet.";
      return `<div class="${
        result.correct ? "is-correct" : "is-incorrect"
      }"><p><strong>${heading}</strong> ${escapeHtml(
        result.message || "",
      )}</p><p>${question.explanation}</p></div>`;
    }
  }

  const SAFE_IDENTIFIERS = new Set([
    "pi",
    "e",
    "E",
    "sin",
    "cos",
    "tan",
    "asin",
    "acos",
    "atan",
    "sec",
    "csc",
    "cot",
    "sinh",
    "cosh",
    "tanh",
    "sqrt",
    "exp",
    "log",
    "ln",
    "abs",
  ]);

  function safeMathSource(value, variables = []) {
    const source = String(value).trim();
    if (
      !source ||
      source.length > 256 ||
      !/^[A-Za-z0-9+\-*/^().,!%\s]+$/.test(source) ||
      /__|[\[\]{}'";:=]/.test(source)
    ) {
      throw new Error("Use only standard mathematical expression syntax.");
    }
    const allowed = new Set([...SAFE_IDENTIFIERS, ...variables]);
    const identifiers = source.match(/[A-Za-z][A-Za-z0-9]*/g) || [];
    if (identifiers.some((name) => !allowed.has(name))) {
      throw new Error(
        "The expression contains an undeclared variable or function.",
      );
    }
    return source;
  }

  function safeNumeric(value) {
    const source = safeMathSource(value);
    if (!window.math)
      throw new Error(
        "The mathematical checker is unavailable; try the notebook version.",
      );
    const result = window.math.evaluate(source);
    const numeric = typeof result === "number" ? result : Number(result);
    if (!Number.isFinite(numeric))
      throw new Error("Enter a finite numeric value.");
    return numeric;
  }

  function symbolicEquivalent(received, expected, variables = []) {
    if (!window.math)
      throw new Error(
        "The symbolic checker is unavailable; try the notebook version.",
      );
    const left = safeMathSource(received, variables);
    const right = safeMathSource(expected, variables);
    const difference = window.math.simplify(`(${left})-(${right})`).toString();
    return difference === "0";
  }

  function requestedForm(value, form, variables) {
    if (form === "any") return true;
    if (!window.math)
      throw new Error(
        "The mathematical checker is unavailable; try the notebook version.",
      );
    const node = window.math.parse(safeMathSource(value, variables));
    if (form === "factored") {
      return !(node.isOperatorNode && ["+", "-"].includes(node.op));
    }
    if (form === "expanded") {
      let nestedSum = false;
      node.traverse((child, _path, parent) => {
        if (
          parent?.isOperatorNode &&
          ["*", "^"].includes(parent.op) &&
          child.isOperatorNode &&
          ["+", "-"].includes(child.op)
        )
          nestedSum = true;
      });
      return !nestedSum;
    }
    throw new Error("The requested algebraic form is unsupported.");
  }

  function stripUnits(value, validation) {
    const source = String(value).trim();
    const unit = validation.units;
    if (!unit) return source;
    const suffix = ` ${unit}`;
    if (source.endsWith(suffix)) return source.slice(0, -suffix.length).trim();
    if (validation.units_required)
      throw new Error(`Include the required unit ${unit}.`);
    return source;
  }

  function solutionSetEquivalent(received, expected, variables) {
    const left = parseSolutionSet(received, variables);
    const right = parseSolutionSet(expected, variables);
    if (left.kind !== right.kind) return false;
    if (left.kind === "all" || left.kind === "empty") return true;
    if (left.kind === "finite") {
      return unorderedEquivalent(left.values, right.values, (a, b) =>
        symbolicEquivalent(a, b, variables),
      );
    }
    return unorderedEquivalent(
      left.intervals,
      right.intervals,
      (a, b) =>
        a.leftOpen === b.leftOpen &&
        a.rightOpen === b.rightOpen &&
        endpointEquivalent(a.left, b.left, variables) &&
        endpointEquivalent(a.right, b.right, variables),
    );
  }

  function parseSolutionSet(value, variables) {
    if (Array.isArray(value))
      return { kind: "finite", values: value.map(String) };
    const source = String(value).trim().replaceAll("∞", "oo");
    if (["empty", "emptyset", "∅", "{}"].includes(source))
      return { kind: "empty" };
    if (["R", "Reals", "real", "all real numbers", "(-oo,oo)"].includes(source))
      return { kind: "all" };
    if (source.startsWith("{") && source.endsWith("}")) {
      const body = source.slice(1, -1).trim();
      if (!body) return { kind: "empty" };
      const values = body
        .split(",")
        .map((item) => safeMathSource(item, variables));
      return { kind: "finite", values };
    }
    const parts = source.split(/\s*(?:U|∪)\s*/);
    const intervals = parts.map((part) => {
      const match = part.match(/^(\[|\()\s*(.*?)\s*,\s*(.*?)\s*(\]|\))$/);
      if (!match)
        throw new Error(
          "Use finite-set or interval notation, such as {1, 2} or [0, 1). ",
        );
      return {
        leftOpen: match[1] === "(",
        left: safeEndpoint(match[2], variables),
        right: safeEndpoint(match[3], variables),
        rightOpen: match[4] === ")",
      };
    });
    return { kind: "intervals", intervals };
  }

  function safeEndpoint(value, variables) {
    const normalized = String(value).trim();
    if (["-oo", "-inf", "-infinity"].includes(normalized)) return "-oo";
    if (
      ["oo", "+oo", "inf", "+inf", "infinity", "+infinity"].includes(normalized)
    )
      return "oo";
    return safeMathSource(normalized, variables);
  }

  function endpointEquivalent(left, right, variables) {
    if (left === "oo" || left === "-oo" || right === "oo" || right === "-oo")
      return left === right;
    return symbolicEquivalent(left, right, variables);
  }

  function unorderedEquivalent(left, right, predicate) {
    if (left.length !== right.length) return false;
    const remaining = [...right];
    return left.every((item) => {
      const index = remaining.findIndex((candidate) =>
        predicate(item, candidate),
      );
      if (index < 0) return false;
      remaining.splice(index, 1);
      return true;
    });
  }

  function escapeHtml(value) {
    return String(value).replace(
      /[&<>'"]/g,
      (character) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          "'": "&#39;",
          '"': "&quot;",
        })[character],
    );
  }

  function cssId(value) {
    return String(value).replace(/[^a-zA-Z0-9_-]/g, "-");
  }

  customElements.define("fc-quiz", FreeCampusQuiz);
})();
