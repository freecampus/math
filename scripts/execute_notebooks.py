#!/usr/bin/env python3
"""Execute representative or complete generated notebook suites."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def representatives() -> list[Path]:
    catalog = json.loads((ROOT / "docs/courses/_catalog.yml").read_text())
    paths: list[Path] = []
    for course in catalog["courses"]:
        items = [
            item
            for unit in course["units"]
            for item in [*unit["lessons"], *unit["challenges"]]
        ]
        if items:
            paths.append(
                ROOT / "notebooks" / Path(items[0]["file"]).with_suffix(".ipynb")
            )
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all", action="store_true", help="execute every generated notebook"
    )
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    paths = (
        sorted((ROOT / "notebooks").rglob("*.ipynb")) if args.all else representatives()
    )
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as temporary:
        execution_root = Path(temporary)
        for path in paths:
            print(f"Executing {path.relative_to(ROOT)}")
            execution_copy = execution_root / path.name
            shutil.copy2(path, execution_copy)
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "nbconvert",
                    "--to",
                    "notebook",
                    "--execute",
                    str(execution_copy),
                    "--output",
                    str(execution_copy),
                    f"--ExecutePreprocessor.timeout={args.timeout}",
                ],
                cwd=ROOT,
                check=False,
            )
            if completed.returncode:
                return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
