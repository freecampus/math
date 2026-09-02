#!/usr/bin/env python3
"""Build deterministic Jupyter/Colab notebooks from canonical QMD lessons."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fcmath.validation import load_structured_data

CATALOG = ROOT / "docs/courses/_catalog.yml"
CODE_FENCE = re.compile(r"^```\{python\}\s*$")
GENERATOR_VERSION = 3
DEPENDENCY_SPECS = {
    "matplotlib": "matplotlib>=3.8,<4",
    "networkx": "networkx>=3.2,<4",
    "numpy": "numpy>=1.26,<3",
    "pandas": "pandas>=2.1,<4",
    "scipy": "scipy>=1.11,<2",
    "statsmodels": "statsmodels>=0.14,<1",
    "sympy": "sympy>=1.12,<2",
}
_LEGACY_CHECKPOINT_CACHE: dict[Path, dict[str, list[dict[str, Any]]]] = {}


def source_items(catalog: dict[str, Any]) -> list[tuple[Path, str, list[str]]]:
    items: list[tuple[Path, str, list[str]]] = []
    seen: set[str] = set()
    for course in catalog["courses"]:
        for unit in course["units"]:
            for item in [*unit["lessons"], *unit["challenges"]]:
                dependencies = list(item.get("computational_dependencies", []))
                items.append((ROOT / "docs" / item["file"], item["id"], dependencies))
                seen.add(item["id"])
            for assessment_id in unit.get("assessment_ids", []):
                assessment = next(
                    value
                    for value in catalog["assessments"]
                    if value["id"] == assessment_id
                )
                items.append((ROOT / "docs" / assessment["file"], assessment["id"], []))
                seen.add(assessment["id"])
    for assessment in catalog.get("assessments", []):
        if assessment["id"] not in seen:
            items.append((ROOT / "docs" / assessment["file"], assessment["id"], []))
    return items


def build_notebook(
    source: Path, item_id: str, dependencies: list[str]
) -> dict[str, Any]:
    text = source.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(text)
    title = scalar_field(front_matter, "title", source.stem.replace("-", " ").title())
    description = scalar_field(front_matter, "description", "")
    has_interactive_quiz = "<fc-quiz" in body
    body = replace_quizzes(body, source)
    body = replace_legacy_checkpoints(body, source)
    body = re.sub(
        r"\{\{<\s*include\s+.*?>\}\}",
        "\n> **Notebook interaction:** Use the surrounding questions as static "
        "practice; website-only controls are omitted.\n",
        body,
    )
    body = re.sub(
        r"<script\b[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE
    )
    body = re.sub(
        r"<div\b[^>]*class=\"quiz-shell[^>]*>.*?</div>",
        "",
        body,
        flags=re.DOTALL | re.IGNORECASE,
    )

    cells: list[dict[str, Any]] = []
    source_relative = source.relative_to(ROOT / "docs")
    source_label = source_relative.as_posix()
    web_url = (
        "https://freecampus.github.io/math/"
        + source_relative.with_suffix(".html").as_posix()
    )
    introduction = (
        f"# {title}\n\n{description}\n\n"
        f"> Canonical lesson: [{source_label}]({web_url})\n"
    )
    cells.append(markdown_cell(introduction))
    distribution = (
        "freecampus-math[notebook]" if has_interactive_quiz else "freecampus-math"
    )
    declared_dependencies = dependency_specs(dependencies)
    setup_dependencies = [distribution, *declared_dependencies]
    required_imports = sorted(
        {
            "fcmath",
            *(name for name in dependencies if name != "fcmath"),
            *({"ipywidgets"} if has_interactive_quiz else set()),
        }
    )
    dependency_arguments = ", ".join(repr(value) for value in setup_dependencies)
    import_arguments = ", ".join(repr(value) for value in required_imports)
    setup_source = (
        "# Generated dependency setup for Colab/Jupyter.\n"
        "# An existing contributor/CI environment is left unchanged.\n"
        "import importlib.util\n"
        "import subprocess\n"
        "import sys\n\n"
        f"_required_modules = ({import_arguments},)\n"
        "if any(\n"
        "    importlib.util.find_spec(name) is None for name in _required_modules\n"
        "):\n"
        "    subprocess.run(\n"
        '        [sys.executable, "-m", "pip", "install", "-q", '
        f"{dependency_arguments}],\n"
        "        check=True,\n"
        "    )\n"
    )
    cells.append(
        code_cell(
            setup_source,
            metadata={"tags": ["fcmath-dependency-setup"]},
        )
    )
    cells.extend(parse_body_cells(body))
    for index, cell in enumerate(cells):
        identity = f"{item_id}:{index}:{''.join(cell['source'])}"
        cell["id"] = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:12]
    revision = git_revision()
    source_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    input_hash = source_input_hash(source, text)
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.10"},
            "colab": {"name": f"{item_id}.ipynb", "provenance": []},
            "fcmath": {
                "generator_version": GENERATOR_VERSION,
                "item_id": item_id,
                "canonical_source": source.relative_to(ROOT).as_posix(),
                "source_revision": revision,
                "source_sha256": source_hash,
                "input_sha256": input_hash,
                "dependencies": setup_dependencies,
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def split_front_matter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unclosed QMD front matter")
    return text[4:end], text[end + 5 :]


def scalar_field(front_matter: str, key: str, default: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", front_matter)
    return match.group(1).strip() if match else default


def replace_quizzes(body: str, source: Path) -> str:
    pattern = re.compile(
        r"<fc-quiz\s+data-source=\"([^\"]+)\"[^>]*>.*?</fc-quiz>", re.DOTALL
    )

    def replacement(match: re.Match[str]) -> str:
        quiz_path = (source.parent / match.group(1)).resolve()
        bank = load_structured_data(quiz_path)
        parts = [
            f"## {bank['title']}",
            "Try each question before opening its solution.",
        ]
        for index, question in enumerate(bank["questions"], start=1):
            parts.append(f"### {index}. {question['prompt']}")
            for option in question.get("options", []):
                parts.append(f"- [ ] {option['text']}")
            parts.append(
                "<details><summary>Solution</summary>\n\n"
                f"{question['explanation']}\n\n</details>"
            )
        serialized = repr(json.dumps(bank, ensure_ascii=False))
        parts.extend(
            (
                "### Interactive notebook version",
                "The widget below uses the same question data and mathematical "
                "validation policy as the website. The static questions and "
                "solutions above remain available if widgets cannot load.",
                "```{python}\n"
                "#| echo: true\n"
                "import json as _json\n\n"
                "from fcmath.quizzes import quiz_from_mapping\n"
                "from fcmath.quizzes.notebook import NotebookQuiz\n\n"
                f"_quiz_data = _json.loads({serialized})\n"
                "NotebookQuiz(quiz_from_mapping(_quiz_data)).display()\n"
                "```",
            )
        )
        return "\n\n".join(parts)

    return pattern.sub(replacement, body)


def replace_legacy_checkpoints(body: str, source: Path) -> str:
    """Compile existing topic generators to deterministic notebook practice."""

    include_pattern = re.compile(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}")
    config_pattern = re.compile(
        r'<script\s+type="application/json"\s+class="[^"]+-config">\s*'
        r"(\{.*?\})\s*</script>",
        flags=re.DOTALL,
    )

    def replacement(match: re.Match[str]) -> str:
        include_path = (source.parent / match.group(1)).resolve()
        if not include_path.is_file() or (
            "checkpoint" not in include_path.name
            and include_path.name != "guessing-game.qmd"
        ):
            return match.group(0)
        configs = config_pattern.findall(body[: match.start()])
        if not configs:
            raise ValueError(f"{source}: checkpoint include has no JSON configuration")
        config = json.loads(configs[-1])
        topic = str(config.get("topic", ""))
        title = str(config.get("title", "Notebook checkpoint"))
        banks = legacy_checkpoint_banks(include_path)
        if topic not in banks:
            raise ValueError(
                f"{source}: topic {topic!r} is missing from {include_path.name}"
            )
        parts = [
            f"### {title}: notebook-safe question pool",
            "The website samples this pool dynamically. This deterministic notebook "
            "edition preserves every question generator for the selected topic. Try "
            "each item before opening its solution.",
        ]
        for index, question in enumerate(banks[topic], start=1):
            parts.append(f"#### {index}. {question['prompt']}")
            if question.get("stimulus"):
                parts.append(f"**Given:** {question['stimulus']}")
            parts.extend(f"- [ ] {option}" for option in question["options"])
            parts.append(
                "<details><summary>Answer and explanation</summary>\n\n"
                f"**Answer:** {question['answer']}\n\n"
                f"{question['explanation']}\n\n</details>"
            )
        return "\n\n".join(parts)

    return include_pattern.sub(replacement, body)


def legacy_checkpoint_banks(path: Path) -> dict[str, list[dict[str, Any]]]:
    """Evaluate trusted repository checkpoint generators in a DOM-free Node shim."""

    cached = _LEGACY_CHECKPOINT_CACHE.get(path)
    if cached is not None:
        return cached
    source = path.read_text(encoding="utf-8")
    script_match = re.search(r"<script>\s*(.*?)\s*</script>", source, re.DOTALL)
    if script_match is None:
        raise ValueError(f"{path}: checkpoint script is missing")
    javascript = script_match.group(1)
    marker = "})();"
    position = javascript.rfind(marker)
    if position < 0:
        raise ValueError(f"{path}: checkpoint closure is missing")
    export = r"""
    const sourceBanks = typeof QUESTION_BANKS !== "undefined" ? QUESTION_BANKS : BANKS;
    globalThis.__fcmathCheckpointBanks = Object.fromEntries(
      Object.entries(sourceBanks).map(([topic, factories]) => [
        topic,
        factories.map((factory) => {
          const item = factory();
          const label = (value) => value
            && typeof value === "object"
            && "label" in value
            ? String(value.label) : String(value);
          const stimulus = item.stimulus && item.stimulus.attributes?.["aria-label"]
            ? item.stimulus.attributes["aria-label"]
            : textOf(item.stimulus);
          return {
            prompt: String(item.prompt),
            stimulus,
            answer: label(item.answer),
            options: item.options.map(label),
            explanation: String(item.explanation),
          };
        }),
      ]),
    );
"""
    instrumented = javascript[:position] + export + javascript[position:]
    shim = r"""
class StaticNode {
  constructor(tag) { this.tag = tag; this.children = []; this.attributes = {}; }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  append(...children) { this.children.push(...children); }
  appendChild(child) { this.children.push(child); return child; }
  addEventListener() {}
  querySelectorAll() { return []; }
}
function textOf(value) {
  if (value === null || value === undefined) return "";
  if (["string", "number", "boolean"].includes(typeof value)) return String(value);
  if (Array.isArray(value)) return value.map(textOf).filter(Boolean).join(" ");
  return (value.children || []).map(textOf).filter(Boolean).join(" ");
}
globalThis.document = {
  querySelectorAll: () => [],
  createElement: (tag) => new StaticNode(tag),
  createElementNS: (_namespace, tag) => new StaticNode(tag),
};
let seed = 20260902;
Math.random = () => {
  seed = (1664525 * seed + 1013904223) >>> 0;
  return seed / 4294967296;
};
"""
    completed = subprocess.run(
        [
            "node",
            "-e",
            shim
            + instrumented
            + "\nconsole.log(JSON.stringify(__fcmathCheckpointBanks));",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise ValueError(
            f"could not compile notebook checkpoint {path}: {completed.stderr.strip()}"
        )
    data = json.loads(completed.stdout)
    result = cast(dict[str, list[dict[str, Any]]], data)
    _LEGACY_CHECKPOINT_CACHE[path] = result
    return result


def source_input_hash(source: Path, text: str) -> str:
    """Hash a QMD source together with local quiz and include dependencies."""

    inputs = [(source.relative_to(ROOT).as_posix(), text)]
    references = [
        *re.findall(r'data-source="([^"]+)"', text),
        *re.findall(r"\{\{<\s*include\s+([^\s>]+)\s*>\}\}", text),
    ]
    for reference in sorted(set(references)):
        dependency = (source.parent / reference).resolve()
        if dependency.is_file():
            inputs.append(
                (
                    dependency.relative_to(ROOT).as_posix(),
                    dependency.read_text(encoding="utf-8"),
                )
            )
    payload = "\n".join(f"{name}\0{content}" for name, content in sorted(inputs))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_body_cells(body: str) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    markdown: list[str] = []
    code: list[str] = []
    in_code = False
    code_metadata: dict[str, Any] = {}

    def flush_markdown() -> None:
        if any(line.strip() for line in markdown):
            cells.append(markdown_cell("\n".join(markdown).strip() + "\n"))
        markdown.clear()

    def flush_code() -> None:
        if any(line.strip() for line in code):
            source = "\n".join(
                line for line in code if not line.startswith("#| output:")
            )
            metadata = dict(code_metadata)
            if any(
                marker in source.lower() for marker in ("your turn", "exercise", "todo")
            ):
                metadata["tags"] = ["learner-exercise"]
            cells.append(code_cell(source.strip() + "\n", metadata=metadata))
        code.clear()
        code_metadata.clear()

    for line in body.splitlines():
        if not in_code and CODE_FENCE.match(line):
            flush_markdown()
            in_code = True
            continue
        if in_code and line == "```":
            flush_code()
            in_code = False
            continue
        if in_code:
            if line.strip() == "#| echo: false":
                code_metadata["jupyter"] = {"source_hidden": True}
            elif line.strip() not in {"#| echo: true"}:
                code.append(line)
        else:
            markdown.append(line)
    if in_code:
        raise ValueError("unclosed Python code fence")
    flush_markdown()
    return cells


def markdown_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code_cell(source: str, *, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": metadata or {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def dependency_specs(dependencies: list[str]) -> list[str]:
    """Resolve catalog dependency names to the tested notebook ranges."""

    unknown = set(dependencies) - {"fcmath", *DEPENDENCY_SPECS}
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ValueError(f"unknown computational dependency: {names}")
    return [DEPENDENCY_SPECS[name] for name in dependencies if name != "fcmath"]


def git_revision() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def notebook_path(source: Path, output_root: Path) -> Path:
    relative = source.relative_to(ROOT / "docs").with_suffix(".ipynb")
    return output_root / relative


def render_all(output_root: Path) -> list[Path]:
    catalog = load_structured_data(CATALOG)
    paths = []
    for source, item_id, dependencies in source_items(catalog):
        target = notebook_path(source, output_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        notebook = build_notebook(source, item_id, dependencies)
        target.write_text(
            json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        paths.append(target)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "notebooks")
    args = parser.parse_args()
    if args.check:
        cache = ROOT / ".cache"
        cache.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as temporary:
            generated_root = Path(temporary)
            generated = render_all(generated_root)
            stale = []
            for generated_path in generated:
                relative = generated_path.relative_to(generated_root)
                existing = args.output / relative
                if (
                    not existing.is_file()
                    or existing.read_bytes() != generated_path.read_bytes()
                ):
                    stale.append(relative)
            if stale:
                print(
                    "Generated notebooks are stale:\n"
                    + "\n".join(f"- {path}" for path in stale),
                    file=sys.stderr,
                )
                return 1
        return 0
    generated = render_all(args.output)
    print(f"Generated {len(generated)} notebooks in {args.output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
